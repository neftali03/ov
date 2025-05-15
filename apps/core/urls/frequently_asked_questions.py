from django.urls import path

from apps.core.views import frequently_asked_questions

faq_patterns = [
    path("faq", frequently_asked_questions.faq_view, name="faq"),
]
