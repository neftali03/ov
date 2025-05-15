from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def faq_view(request):
    """Render the FAQ page with preset questions and answers."""
    faqs = [
        {
            "question": "¿Cómo inicio una evaluación?",
            "answer": "Ve a la sección de Orientación y haz clic en 'Iniciar'.",
        },
        {
            "question": "¿Puedo modificar mis respuestas?",
            "answer": "No. En caso de error, deberá contactar "
            "al administrador del test.",
        },
        {
            "question": "¿Qué pasa si cierro sesión durante una evaluación?",
            "answer": "Deberá iniciar de nuevo su test vocacional.",
        },
        {
            "question": "¿Cuánto tiempo me tomará el test vocacional?",
            "answer": "El test tiene una duración máxima de una hora.",
        },
        {
            "question": "¿El test vocacional tiene límite de tiempo?",
            "answer": "No, el test no tiene límite de tiempo, pero te recomendamos "
            "hacer tu evaluación en un ambiente cómodo y sin distracciones.",
        },
        {
            "question": "¿A quién debo contactar si tengo algún problema?",
            "answer": "Si tienes algún problema, puedes escribir "
            "al administrador del test: 'neftalihrramos@gmail.com'.",
        },
    ]
    return render(
        request,
        template_name="core/frequently_asked_questions/frequently_asked_questions.html",
        context={"faqs": faqs},
    )
