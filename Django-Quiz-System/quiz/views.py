from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Choice

def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'home.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        score = 0
        questions = quiz.questions.all()
        
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                if choice.is_correct:
                    score += 1
        
        return render(request, 'result.html', {
            'quiz': quiz,
            'score': score,
            'total': questions.count(),
        })
    
    return render(request, 'quiz.html', {'quiz': quiz})
