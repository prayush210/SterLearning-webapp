import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from app_streaming.consumers import get_section
from app_quiz.models import Quiz, MultipleChoice, MultipleChoiceOptions, FillInBlank, FillInBlankSentence, Information, \
    Attempt
from django.test import TestCase, AsyncClient
from channels.testing import WebsocketCommunicator
from app_streaming.consumers import QuizConsumer


class GetSectionTest(TestCase):

    def setUp(self):

        self.quiz = Quiz.objects.create(name='Test Quiz')

        self.mcq = MultipleChoice.objects.create(quiz=self.quiz, title='MCQ Question', position=1, points=10)
        MultipleChoiceOptions.objects.create(question=self.mcq, text='Option 1', correct=True)
        MultipleChoiceOptions.objects.create(question=self.mcq, text='Option 2', correct=False)

        self.fib = FillInBlank.objects.create(quiz=self.quiz, title='FIB Question', position=2)
        FillInBlankSentence.objects.create(question=self.fib, before='Before', blank='Blank', after='After', points=5)

        self.inf = Information.objects.create(quiz=self.quiz, title='Information', content='Content', position=3)

    # Test retrieving a multiple choice section
    def test_get_section_mcq(self):
        section = get_section(self.quiz, 1)
        self.assertEqual(section['section_type'], 'mcq')
        self.assertEqual(section['section']['title'], self.mcq.title)
        self.assertEqual(len(section['section']['options']), 2)

    # Test retrieving a fill in the blank section
    def test_get_section_fib(self):
        section = get_section(self.quiz, 2)
        self.assertEqual(section['section_type'], 'fib')
        self.assertEqual(section['section']['title'], self.fib.title)
        self.assertEqual(len(section['section']['sentences']), 1)

    # Test retrieving an information section
    def test_get_section_inf(self):
        section = get_section(self.quiz, 3)
        self.assertEqual(section['section_type'], 'inf')
        self.assertEqual(section['section']['title'], self.inf.title)

    # Test retrieving an end section
    def test_get_section_end(self):
        section = get_section(self.quiz, 4)
        self.assertEqual(section['section_type'], 'end')


class QuizConsumerTest(TestCase):

    # Create user asynchronously
    @database_sync_to_async
    def create_user(self):
        return get_user_model().objects.create_user(username='testuser', password='testpassword')

    # Create quiz asynchronously
    @database_sync_to_async
    def create_quiz(self):

        return Quiz.objects.create(name='Test Quiz')

    # Connect to the websocket
    async def connect(self):

        self.user = await self.create_user()

        self.quiz = await self.create_quiz()

        self.client = AsyncClient()

        await sync_to_async(self.client.login)(username='testuser', password='testpassword')

        self.communicator = WebsocketCommunicator(QuizConsumer.as_asgi(), "/ws/quiz/")

        self.communicator.scope['user'] = self.user

        connected, _ = await self.communicator.connect()
        assert connected

        _ = await self.communicator.receive_from()

    #  Test disconnecting from the websocket
    async def test_disconnect(self):
        await self.connect()

        await self.communicator.send_to(json.dumps({"type": "start", "qid": self.quiz.id}))

        _ = await self.communicator.receive_from()

        await self.communicator.disconnect()

        attempt = await sync_to_async(Attempt.objects.get)(user=self.user)
        self.assertFalse(attempt.quiz_open)

    # Test retrieving data from websocket
    async def test_receive(self):
        await self.connect()

        await self.communicator.send_to(json.dumps({"type": "start", "qid": self.quiz.id}))

        response = await self.communicator.receive_from()
        data = json.loads(response)

        self.assertEqual(data, {"type": "first_section", "section_type": "end", "section": {}})

        await self.communicator.disconnect()
