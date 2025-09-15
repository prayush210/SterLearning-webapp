"""
URL configuration for SterLearning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_quiz import views as quiz_views
from app_user import views as user_views
from app_tools import views as tools_views

# These are the URL patterns specific to the 5 pathways.
# learn/ is stripped from the start of the URL in the main pattern.
pathway_patterns =[
    path("", quiz_views.pathways, name="pathways-home"),
    path("bank-accounts/", quiz_views.bank),
    path("pensions/", quiz_views.pensions),
    path("taxes/", quiz_views.taxes),
    path("loans/", quiz_views.loans),
    path("budgeting/", quiz_views.budget),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("learn/", include(pathway_patterns)),
    path("quiz/<int:qid>/", quiz_views.quiz, name="quiz-views-quiz"),
    path("shop/", user_views.shop, name="shop"),
    path("accounts/", include("app_user.urls")),
    path("tools/", tools_views.mortgage, name="mortgage-calculator"),
    path("", include("app_pages.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
