from django.test import TestCase, Client
from django.urls import reverse
from .models import *


# Set up a valid quiz
def create_quiz():
    q = Quiz(name="Test Quiz",
             description="A quiz to test with",
             pathway="LOANS")
    q.save()
    q.full_clean()

    return q


# Tests for MCQs
class MultipleChoiceTest(TestCase):
    # Test two can't be at same position
    def test_unique_position(self):
        quiz = create_quiz()

        kwargs = {"title": "MCQ",
                  "quiz": quiz,
                  "position": 1,
                  "points": 25
                  }

        q = MultipleChoice(**kwargs)
        q.save()

        q = MultipleChoice(**kwargs)
        q.save()

        with self.assertRaises(ValidationError):
            q.full_clean()

    # A question can't have 2 correct answers
    def test_one_correct_answer(self):
        quiz = create_quiz()

        question = MultipleChoice(title="MCQ",
                                  quiz=quiz,
                                  position=1,
                                  points=25)
        question.save()

        a = MultipleChoiceOptions(text="Option A",
                                  correct=True,
                                  question=question)
        a.save()

        b = MultipleChoiceOptions(text="Option B",
                                  correct=True,
                                  question=question)
        b.save()

        with self.assertRaises(ValidationError):
            a.full_clean()

        with self.assertRaises(ValidationError):
            b.full_clean()

    # Test a valid question
    def test_valid(self):
        quiz = create_quiz()

        question = MultipleChoice(title="MCQ",
                                  quiz=quiz,
                                  position=1,
                                  points=25)
        question.save()

        a = MultipleChoiceOptions(text="Option A",
                                  correct=True,
                                  question=question)
        a.save()

        b = MultipleChoiceOptions(text="Option B",
                                  correct=False,
                                  question=question)
        b.save()

        question.full_clean()
        a.full_clean()
        b.full_clean()


# Tests for FIBs
class FillInBlankTest(TestCase):
    # Test two can't be at same position
    def test_unique_position(self):
        quiz = create_quiz()

        kwargs = {"title": "FIB",
                  "quiz": quiz,
                  "position": 1
                  }

        q = FillInBlank(**kwargs)
        q.save()

        q = FillInBlank(**kwargs)
        q.save()

        with self.assertRaises(ValidationError):
            q.full_clean()

    # Test that sentence can't be empty
    def test_empty_sentence(self):
        quiz = create_quiz()

        question = FillInBlank(title="FIB",
                               quiz=quiz,
                               position=1)
        question.save()

        a = FillInBlankSentence(before=None,
                                blank=None,
                                after=None,
                                question=question,
                                points=25)
        a.save()

        b = FillInBlankSentence(before="",
                                blank="",
                                after="",
                                question=question,
                                points=25)
        b.save()

        with self.assertRaises(ValidationError):
            a.full_clean()

        with self.assertRaises(ValidationError):
            b.full_clean()

    # Test valid
    def test_valid(self):
        quiz = create_quiz()

        question = FillInBlank(title="FIB",
                               quiz=quiz,
                               position=1)
        question.save()

        a = FillInBlankSentence(before=None,
                                blank="Blank",
                                after=" and after",
                                question=question,
                                points=25)
        a.save()

        b = FillInBlankSentence(before="Before ",
                                blank="blank",
                                after=" after",
                                question=question,
                                points=25)
        b.save()

        question.full_clean()
        a.full_clean()
        b.full_clean()


# Tests for info sections
class InformationTest(TestCase):
    # Test two can't be at same position
    def test_unique_position(self):
        quiz = create_quiz()

        kwargs = {"title": "INF",
                  "quiz": quiz,
                  "position": 1,
                  "content": "Information section"
                  }

        i = Information(**kwargs)
        i.save()

        i = Information(**kwargs)
        i.save()

        with self.assertRaises(ValidationError):
            i.full_clean()

    # Test valid
    def test_valid(self):
        quiz = create_quiz()

        i = Information(title="INF",
                        quiz=quiz,
                        position=1,
                        content="Information section")
        i.save()
        i.full_clean()


class AttemptTest(TestCase):
    def setUp(self):
        self.user = ExtendedUser.objects.create(username='testuser', password='testpassword')
        self.quiz = Quiz.objects.create(name='Test Quiz', description='A quiz for testing', pathway='LOANS')

    # Test attempt creation
    def test_attempt_creation(self):
        attempt = Attempt.objects.create(user=self.user, quiz=self.quiz)
        self.assertEqual(Attempt.objects.count(), 1)
        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.quiz, self.quiz)
        self.assertEqual(attempt.completed, False)
        self.assertEqual(attempt.quiz_open, True)


class MultipleChoiceResponseTest(TestCase):
    def setUp(self):
        self.user = ExtendedUser.objects.create(username='testuser', password='testpassword')
        self.quiz = Quiz.objects.create(name='Test Quiz', description='A quiz for testing', pathway='LOANS')
        self.attempt = Attempt.objects.create(user=self.user, quiz=self.quiz)
        self.question = MultipleChoice.objects.create(title="MCQ", quiz=self.quiz, position=1, points=25)
        self.option = MultipleChoiceOptions.objects.create(text="Option A", correct=True, question=self.question)
        self.points_awarded = PointsAwarded.objects.create(user=self.user, points=10)

    # Test multiple choice response creation
    def test_multiple_choice_response_creation(self):
        mc_response = MultipleChoiceResponse.objects.create(attempt=self.attempt, answer=self.option,
                                                            points_awarded=self.points_awarded)
        self.assertEqual(MultipleChoiceResponse.objects.count(), 1)
        self.assertEqual(mc_response.attempt, self.attempt)
        self.assertEqual(mc_response.answer, self.option)
        self.assertEqual(mc_response.points_awarded, self.points_awarded)


class FillInBlankAnswerTest(TestCase):
    def setUp(self):
        self.user = ExtendedUser.objects.create(username='testuser', password='testpassword')
        self.quiz = Quiz.objects.create(name='Test Quiz', description='A quiz for testing', pathway='LOANS')
        self.question = FillInBlank.objects.create(title="FIB", quiz=self.quiz, position=1)
        self.sentence = FillInBlankSentence.objects.create(before="Before", blank="Blank", after="After",
                                                           question=self.question, points=25)
        self.attempt = Attempt.objects.create(user=self.user, quiz=self.quiz)
        self.response = FillInBlankReponse.objects.create(attempt=self.attempt)
        self.points_awarded = PointsAwarded.objects.create(user=self.user, points=10)

    # Test fill in blank answer creation
    def test_fill_in_blank_answer_creation(self):
        fib_answer = FillInBlankAnswer.objects.create(response=self.response, blank="Blank",
                                                      points_awarded=self.points_awarded, sentence=self.sentence)
        self.assertEqual(FillInBlankAnswer.objects.count(), 1)
        self.assertEqual(fib_answer.response, self.response)
        self.assertEqual(fib_answer.blank, "Blank")
        self.assertEqual(fib_answer.points_awarded, self.points_awarded)
        self.assertEqual(fib_answer.sentence, self.sentence)


class PathwaysViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.pathways_url = reverse(
            'pathways-home')

    # Test GET request for pathways view
    def test_pathways_GET(self):
        response = self.client.get(self.pathways_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pathways_home.html')


class QuizViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.quiz = Quiz.objects.create(name='Test Quiz', description='A quiz for testing', pathway='LOANS')
        self.quiz_url = reverse('quiz-views-quiz', args=[self.quiz.id])

    # Test GET request for quiz view
    def test_quiz_GET(self):
        response = self.client.get(self.quiz_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz.html')
