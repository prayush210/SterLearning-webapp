from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext
from app_user.models import ExtendedUser, PointsAwarded


# Verifies that no two sections share the same positions
def check_unique_pos(self):
    quiz = self.quiz
    pos = self.position

    mcq = MultipleChoice.objects.filter(quiz = quiz, position = pos)
    fib = FillInBlank.objects.filter(quiz = quiz, position = pos)
    inf = Information.objects.filter(quiz = quiz, position = pos)

    if mcq.count() != 0:
        if self.__class__ != MultipleChoice or mcq.count() != 1:
            raise ValidationError(gettext("SectionAlreadyAtPosition"))

    if fib.count() != 0:
        if self.__class__ != FillInBlank or fib.count() != 1:
            raise ValidationError(gettext("SectionAlreadyAtPosition"))

    if inf.count() != 0:
        if self.__class__ != Information or inf.count() != 1:
            raise ValidationError(gettext("SectionAlreadyAtPosition"))

# Quiz model - stores which pathway the quiz is in and its name.
class Quiz(models.Model):
    class Pathways(models.TextChoices):
        LOANS = "LOANS", gettext("LoansPathway")
        BUDGET = "BUDGET", gettext("BudgetingPathway")
        BANK = "BANK", gettext("BankAccountsPathway")
        TAX = "TAX", gettext("TaxesPathway")
        PENSION = "PENSION", gettext("PensionsPathway")

    name = models.CharField(max_length = 100)
    description = models.TextField()
    pathway = models.CharField(choices = Pathways.choices, max_length = 7)


# Abstract class for a section within a quiz containing a title and position.
class QuizSection(models.Model):
    title = models.CharField(max_length = 100)
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)
    position = models.IntegerField()

    class Meta:
        abstract = True


# Multiple choice question, stores points awarded for correct answer.
class MultipleChoice(QuizSection):
    points = models.IntegerField()

    def clean(self):
        check_unique_pos(self)


# Option for a MCQ. Relates to one MultipleChoice instance.
class MultipleChoiceOptions(models.Model):
    text = models.CharField(max_length = 100)
    correct = models.BooleanField()
    question = models.ForeignKey(MultipleChoice, on_delete = models.CASCADE)

    def clean(self):
        question = self.question
        correct = 0

        for option in MultipleChoiceOptions.objects.filter(question = question):
            if option.correct:
                correct += 1

        if correct > 1:
            raise ValidationError("TooManyCorrectAnswers")

# Model for fill in the blank questions. No additional fields needed.
class FillInBlank(QuizSection):
    def clean(self):
        check_unique_pos(self)


# A setence within a fill in the blank question. Blank can be at the start or
# end and is optional. Related to one FillInBlank.
class FillInBlankSentence(models.Model):
    before = models.CharField(null = True, blank = True, max_length = 100)
    blank = models.CharField(null = True, blank = True, max_length = 100)
    after = models.CharField(null = True, blank = True, max_length = 100)
    question = models.ForeignKey(FillInBlank, on_delete = models.CASCADE)
    points = models.IntegerField()

    def clean(self):
        before = True
        blank = True
        after = True

        if self.before is None or self.before == "":
            before = False

        if self.blank is None or self.blank == "":
            blank = False

        if self.after is None or self.after == "":
            after = False

        if before is False and blank is False and after is False:
            raise ValidationError("SentenceEmpty")


# Model for an information screen that can be put in a quiz to give user info.
class Information(QuizSection):
    content = models.TextField()
    image = models.ImageField(null = True, blank = True, upload_to = 'images/quizzes/info_sections')

    def clean(self):
        check_unique_pos(self)


# Model for a user's attempt at a quiz
class Attempt(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete = models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)
    completed = models.BooleanField(default = False)
    quiz_open = models.BooleanField(default = True)


# Model to represent a user's answer to a MCQ
class MultipleChoiceResponse(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete = models.CASCADE)
    answer = models.ForeignKey(MultipleChoiceOptions, on_delete = models.CASCADE)
    points_awarded = models.ForeignKey(PointsAwarded, on_delete = models.CASCADE)


# Model to represent a user's answer to a FIB
class FillInBlankReponse(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete = models.CASCADE)


# Model to link a user's FIB answer to the corresponding sentence
class FillInBlankAnswer(models.Model):
    response = models.ForeignKey(FillInBlankReponse, on_delete = models.CASCADE)
    blank = models.CharField(null = True, blank = True, max_length = 100)
    points_awarded = models.ForeignKey(PointsAwarded, on_delete = models.CASCADE)
    sentence = models.ForeignKey(FillInBlankSentence, on_delete = models.CASCADE)
