from django.shortcuts import render, get_object_or_404
from .models import Quiz


# Create your views here.
def pathways(request):
    # Past attempts aren"t stored yet, placeholder
    context = {}
    context["bank_score"] = 50
    context["pensions_score"] = 50
    context["taxes_score"] = 50
    context["loans_score"] = 50
    context["budget_score"] = 50

    return render(request, "pathways_home.html", context)


def bank(request):
    context = {}
    context["quizzes"] = Quiz.objects.filter(pathway = "BANK")

    return render(request, "pathway.html", context)


def pensions(request):
    context = {}
    context["quizzes"] = Quiz.objects.filter(pathway = "PENSION")

    return render(request, "pathway.html", context)


def taxes(request):
    context = {}
    context["quizzes"] = Quiz.objects.filter(pathway = "TAX")

    return render(request, "pathway.html", context)


def loans(request):
    context = {}
    context["quizzes"] = Quiz.objects.filter(pathway = "LOANS")

    return render(request, "pathway.html", context)


def budget(request):
    context = {}
    context["quizzes"] = Quiz.objects.filter(pathway = "BUDGET")

    return render(request, "pathway.html", context)


def quiz(request, qid):
    current_quiz = get_object_or_404(Quiz, id = qid)
    context = {}
    context["quiz"] = current_quiz

    return render(request, "quiz.html", context)
