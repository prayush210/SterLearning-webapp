import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from app_quiz.models import *
from asgiref.sync import async_to_sync


# Retrieves question at specified position in a given quiz.
def get_section(quiz, pos):
    result = {}

    mcq = MultipleChoice.objects.filter(quiz=quiz)
    fib = FillInBlank.objects.filter(quiz=quiz)
    inf = Information.objects.filter(quiz=quiz)

    section = {}

    if mcq.filter(position=pos).count() == 1:
        q = mcq.get(position=pos)
        section["sid"] = q.id
        section["title"] = q.title
        section["position"] = pos

        options = []
        for option in MultipleChoiceOptions.objects.filter(question=q):
            options.append({"id": option.id,
                            "text": option.text})

        section["options"] = options
        result["section_type"] = "mcq"

    elif fib.filter(position=pos).count() == 1:
        q = fib.get(position=pos)
        section["sid"] = q.id
        section["title"] = q.title
        section["position"] = pos

        sentences = []
        for sentence in FillInBlankSentence.objects.filter(question=q):
            blank = False

            if sentence.blank:
                blank = True

            # There can be any number of sentences, not all will have a blank.
            # The blank word can also be at any point in the sentence.
            sentences.append({"id": sentence.id,
                              "before": sentence.before,
                              "blank": blank,
                              "after": sentence.after})

        section["sentences"] = sentences
        result["section_type"] = "fib"

    elif inf.filter(position=pos).count() == 1:
        i = inf.get(position=pos)
        section["sid"] = i.id
        section["title"] = i.title
        section["position"] = pos
        section["content"] = i.content
        section["image"] = "NO_IMAGE"

        if i.image:
            section["image"] = i.image.url

        result["section_type"] = "inf"

    else:
        result["section_type"] = "end"

    result["section"] = section

    return result


# Handles all quiz-related WebSocket activity.
class QuizConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope["user"]  # for later use

        self.send(text_data=json.dumps(
            {
                "type": "connected"
            }
        ))

    def disconnect(self, close_code):
        self.attempt.quiz_open = False
        self.attempt.save()

    def receive(self, text_data):
        data = json.loads(text_data)
        result = None

        # Client has submitted an answer for validation.
        if data["type"] == "answer":
            if data["section_type"] == "mcq":
                qid = data["question_id"]
                sid = data["selected_id"]

                question = get_object_or_404(MultipleChoice, id=qid)
                selected = get_object_or_404(MultipleChoiceOptions, id=sid)
                points = 0

                if selected.correct:
                    points = question.points
                    self.send(json.dumps(
                        {
                            "type": "validated_mcq_answer",
                            "correct": True,
                            "awarded": question.points
                        }
                    ))
                else:
                    self.send(json.dumps(
                        {
                            "type": "validated_mcq_answer",
                            "correct": False,
                            "awarded": 0
                        }
                    ))

                awarded = PointsAwarded(user=self.user,
                                        points=points)
                awarded.save()

                response = MultipleChoiceResponse(attempt=self.attempt,
                                                  answer=selected,
                                                  points_awarded=awarded)
                response.save()
            elif data["section_type"] == "fib":
                total = 0
                correct = []
                response = FillInBlankReponse(attempt=self.attempt)
                response.save()

                for sentence in data["sentences"]:
                    sid = sentence["id"]
                    blank = sentence["blank"]
                    points = 0

                    s = get_object_or_404(FillInBlankSentence, id=sid)
                    if blank.lower() == s.blank.lower():
                        total += s.points
                        points = s.points
                        correct.append(sid)

                    awarded = PointsAwarded(user=self.user,
                                            points=points)
                    awarded.save()

                    answer = FillInBlankAnswer(response=response,
                                               blank=blank,
                                               points_awarded=awarded,
                                               sentence=s)
                    answer.save()

                self.send(json.dumps(
                    {
                        "type": "validated_fib_answer",
                        "correct": correct,
                        "awarded": total
                    }
                ))

        # Client ready for next question.
        elif data["type"] == "next":
            qid = data["qid"]
            quiz = get_object_or_404(Quiz, id=qid)
            position = data["position"]
            result = get_section(quiz, position + 1)

            # No more questions, tell client & close WebSocket.
            if result["section_type"] == "end":
                self.send(json.dumps(
                    {
                        "type": "end_quiz"
                    }
                ))
                attempt = self.attempt

                attempt.completed = True
                attempt.quiz_open = False
                attempt.save()

                self.close()
            else:
                self.send(json.dumps(
                    {
                        "type": "next_section",
                        "section_type": result["section_type"],
                        "section": result["section"]
                    }
                ))

        # Client ready for first question.    
        elif data["type"] == "start":
            qid = data["qid"]
            quiz = get_object_or_404(Quiz, id=qid)
            result = get_section(quiz, 1)

            print(self.user)
            attempt = Attempt(user=self.user,
                              quiz=quiz,
                              completed=False,
                              quiz_open=True)
            attempt.save()

            self.attempt = attempt

            self.send(json.dumps(
                {
                    "type": "first_section",
                    "section_type": result["section_type"],
                    "section": result["section"]
                }
            ))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'public_room'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({ 'message': event['message'] , 'id' : event['id'], 'target' : event['target'] }))
