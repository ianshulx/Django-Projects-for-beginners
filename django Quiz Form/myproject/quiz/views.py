from django.shortcuts import render, redirect
from .forms import NameForm, QuizForm
from .models import QuizResult

def quiz_view(request):
    # Handle POST requests
    if request.method == 'POST':
        # Check if the user is entering their name
        if 'name' not in request.session:
            form = NameForm(request.POST)
            if form.is_valid():
                # Save the user's name in the session
                name = form.cleaned_data['name']
                request.session['name'] = name
                request.session['current_question'] = 1  # Initialize current question
                request.session['score'] = 0  # Initialize score
                return redirect('quiz')  # Redirect to the quiz page
        else:
            # Handle quiz answers
            form = QuizForm(request.POST, current_question=request.session.get('current_question'))
            if form.is_valid():
                current_question = request.session.get('current_question', 1)
                score = request.session.get('score', 0)

                # Correct answers for the quiz
                correct_answers = {
                    'q1': 'b', 'q2': 'c', 'q3': 'b', 'q4': 'a', 'q5': 'b',
                    'q6': 'c', 'q7': 'c', 'q8': 'c', 'q9': 'b', 'q10': 'c'
                }

                user_answer = form.cleaned_data.get(f'q{current_question}')
                correct_answer = correct_answers.get(f'q{current_question}')
                if user_answer == correct_answer:
                    score += 1
                request.session['score'] = score

                if current_question < len(correct_answers):
                    request.session['current_question'] = current_question + 1
                    return redirect('quiz')
                else:
                    # Quiz is complete
                    name = request.session['name']
                    total_questions = len(correct_answers)
                    percentage = (score / total_questions) * 100

                    # Save result in the database
                    QuizResult.objects.create(
                        name=name,
                        score=score,
                        total_questions=total_questions
                    )

                    # Render result page
                    response = render(request, 'quiz/result.html', {
                        'name': name,
                        'score': score,
                        'percentage': percentage,
                        'total_questions': total_questions
                    })

                    # Clear session data
                    request.session.flush()
                    return response

    # Handle GET requests
    else:
        if 'name' in request.session:
            # Continue quiz
            current_question = request.session.get('current_question', 1)
            form = QuizForm(current_question=current_question)
            name = request.session.get('name', '')
            return render(request, 'quiz/quiz.html', {'form': form, 'name': name})
        else:
            # Show name form
            form = NameForm()
            return render(request, 'quiz/name.html', {'form': form})
