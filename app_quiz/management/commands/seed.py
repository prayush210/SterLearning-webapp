import json
import os

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile

from app_quiz.models import (Quiz, MultipleChoice, MultipleChoiceOptions,
    FillInBlank, FillInBlankSentence, Information)
from app_user.models import Avatar, Decoration


# Define a custom management command for Django
class Command(BaseCommand):
    """Django command to load data from JSON files into the Quiz model."""

    help = 'Load data from JSON files into the Quiz model'

    def handle(self, *args, **options):
        """Handle the command."""

        # Define the paths to the JSON files
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        calc_tax_quiz_json = os.path.join(
            base_dir, 'json_pathways/tax_data/calc_tax_data.json')
        payslip_reading_quiz_json = os.path.join(
            base_dir, 'json_pathways/tax_data/payslip_reading_data.json')
        diff_in_partfull_quiz_json = os.path.join(
            base_dir, 'json_pathways/tax_data/diff_in_partfull_data.json')
        budget_paycheck_quiz_json = os.path.join(
            base_dir, 'json_pathways/budget_data/budget_paycheck_data.json')
        rent_bills_quiz_json = os.path.join(
            base_dir, 'json_pathways/budget_data/rent_bills_data.json')
        save_money_quiz_json = os.path.join(
            base_dir, 'json_pathways/budget_data/save_money_data.json')
        retiring_quiz_json = os.path.join(
            base_dir, 'json_pathways/pension_data/retiring_data.json')
        state_workplace_quiz_json = os.path.join(
            base_dir, 'json_pathways/pension_data/state_workplace_data.json')
        what_is_pension_quiz_json = os.path.join(
            base_dir, 'json_pathways/pension_data/what_is_pension_data.json')

        # Load Calculating Taxes Quiz data
        with open(calc_tax_quiz_json, 'r', encoding='utf8') as f:
            calc_tax_quiz_data = json.load(f)

        # Load Payslip Reading Quiz data
        with open(payslip_reading_quiz_json, 'r', encoding='utf8') as f:
            payslip_reading_quiz_data = json.load(f)

        # Load Differences in Part-time and Full-time Pay Quiz data
        with open(diff_in_partfull_quiz_json, 'r', encoding='utf8') as f:
            diff_in_partfull_quiz_data = json.load(f)

        # Load Budget Paycheck Quiz data
        with open(budget_paycheck_quiz_json, 'r', encoding='utf8') as f:
            budget_paycheck_quiz_data = json.load(f)

        # Load Rent Bills Quiz data
        with open(rent_bills_quiz_json, 'r', encoding='utf8') as f:
            rent_bills_quiz_data = json.load(f)

        # Load Save Money Quiz data
        with open(save_money_quiz_json, 'r', encoding='utf8') as f:
            save_money_quiz_data = json.load(f)

        # Load Retiring Quiz data
        with open(retiring_quiz_json, 'r', encoding='utf8') as f:
            retiring_quiz_json = json.load(f)

        # Load State Workplace Quiz data
        with open(state_workplace_quiz_json, 'r', encoding='utf8') as f:
            state_workplace_quiz_json = json.load(f)

        # Load What is a Pension Quiz data
        with open(what_is_pension_quiz_json, 'r', encoding='utf8') as f:
            what_is_pension_quiz_json = json.load(f)

        # Delete existing data
        Quiz.objects.all().delete()
        MultipleChoice.objects.all().delete()
        MultipleChoiceOptions.objects.all().delete()
        FillInBlank.objects.all().delete()
        FillInBlankSentence.objects.all().delete()
        Information.objects.all().delete()
        Avatar.objects.all().delete()
        Decoration.objects.all().delete()

        # Seed data for each quiz
        self.seed_quiz_data(calc_tax_quiz_data)
        self.stdout.write(
            self.style.SUCCESS('Data for Calculating Taxes Quiz loaded successfully!'))

        self.seed_quiz_data(payslip_reading_quiz_data)
        self.stdout.write(self.style.SUCCESS('Data for Payslip Reading Quiz loaded successfully!'))

        self.seed_quiz_data(diff_in_partfull_quiz_data)
        self.stdout.write(
            self.style.SUCCESS(
                'Data for Differences in Part-time and Full-time Pay Quiz loaded successfully!'))

        self.seed_quiz_data(budget_paycheck_quiz_data)
        self.stdout.write(self.style.SUCCESS('Data for Budget Paycheck Quiz loaded successfully!'))

        self.seed_quiz_data(rent_bills_quiz_data)
        self.stdout.write(self.style.SUCCESS('Data for Rent Bills Quiz loaded successfully!'))

        self.seed_quiz_data(save_money_quiz_data)
        self.stdout.write(self.style.SUCCESS('Data for Save Money Quiz loaded successfully!'))

        self.seed_quiz_data(retiring_quiz_json)
        self.stdout.write(self.style.SUCCESS('Data for Retiring Quiz loaded successfully!'))

        self.seed_quiz_data(state_workplace_quiz_json)
        self.stdout.write(self.style.SUCCESS('Data for State Workplace Quiz loaded successfully!'))

        self.seed_quiz_data(what_is_pension_quiz_json)
        self.stdout.write(self.style.SUCCESS(
            'Data for What is a Pension Quiz loaded successfully!'))

        # Seed all the profile avatars and decorations
        avatar = Avatar(name = 'Cat',
                        image = ImageFile(open('sample_data/icon-avatar-cat.png', 'rb'),
                                        name='icon-avatar-cat.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Dog',
                        image = ImageFile(open('sample_data/icon-avatar-dog.png', 'rb'),
                                        name='icon-avatar-dog.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Duck',
                        image = ImageFile(open('sample_data/icon-avatar-duck.png', 'rb'),
                                        name='icon-avatar-duck.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Lily',
                        image = ImageFile(open('sample_data/icon-avatar-lily.png', 'rb'),
                                        name='icon-avatar-lily.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Snail',
                        image = ImageFile(open('sample_data/icon-avatar-snail.png', 'rb'),
                                        name='icon-avatar-snail.png'))
        avatar.save()
        avatar.full_clean()

        avatar = Avatar(name = 'Default',
                        image = ImageFile(open('sample_data/Placeholder image.png', 'rb'),
                                          name='Placeholder image.png'))

        decoration = Decoration(name = 'Crown',
                                image = ImageFile(open('sample_data/icon-hat-crown.png', 'rb'),
                                        name='icon-hat-crown.png'))
        decoration.save()
        decoration.full_clean()

        decoration = Decoration(name = 'Propellor Hat',
                                image = ImageFile(open('sample_data/icon-hat-propellor.png', 'rb'),
                                        name='icon-hat-propellor.png'))
        decoration.save()
        decoration.full_clean()

        decoration = Decoration(name = 'Wizard Hat',
                                image = ImageFile(open('sample_data/icon-hat-wizard.png', 'rb'),
                                        name='icon-hat-wizard.png'))
        decoration.save()
        decoration.full_clean()

    def seed_quiz_data(self, quiz_data):
        """Seeds data for a single quiz."""

        quiz = Quiz.objects.create(
            name=quiz_data['name'],
            description=quiz_data['description'],
            pathway=quiz_data['pathway']
        )

        # Loop through each section in the quiz data
        for section_data in quiz_data['sections']:
            # Check if the section is a question section or an info section
            if 'questions' in section_data:
                # Loop through each question in the section
                for question_data in section_data['questions']:
                    if question_data['type'] == 'Multiple Choice':
                        # Create a new MultipleChoice question
                        question = MultipleChoice.objects.create(
                            title=question_data['question'],  # Used 'question' from JSON as 'title'
                            quiz=quiz,
                            position=question_data['position'],
                            points=question_data['points']
                        )

                        # Loop through each option for the question
                        for option_text in question_data['options']:
                            # Check if the option is the correct answer
                            correct = option_text == question_data['correct_option']
                            # Create a new MultipleChoiceOptions object for the option
                            MultipleChoiceOptions.objects.create(
                                text=option_text,
                                correct=correct,
                                question=question
                            )
                    elif question_data['type'] == 'Fill in the Blank':
                        # Create a new FillInBlank question
                        question = FillInBlank.objects.create(
                            title=question_data['question'],  # Used 'question' from JSON as 'title'
                            quiz=quiz,
                            position=question_data['position']
                        )

                        # Create a new FillInBlankSentence object for the question
                        FillInBlankSentence.objects.create(
                            before=question_data['before'],
                            blank=question_data['blank'],
                            after=question_data['after'],
                            question=question,
                            points=question_data['points']
                        )
            elif 'info' in section_data:
                # Loop through each info in the section
                for info_data in section_data['info']:
                    # Create a new Information object
                    Information.objects.create(
                        title=info_data['title'],
                        content=info_data['content'],
                        quiz=quiz,
                        position=info_data['position']
                    )
