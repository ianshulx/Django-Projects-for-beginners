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
            current_question = request.session.get('current_question', 1)
            score = request.session.get('score', 0)
            name = request.session.get('name', '')

            # Ensure the session data is valid
            correct_answers = {
                'q1': 'b', 'q2': 'c', 'q3': 'b', 'q4': 'a', 'q5': 'b',
                'q6': 'c', 'q7': 'c', 'q8': 'c', 'q9': 'b', 'q10': 'c'
            }
            total_questions = len(correct_answers)
            
            # Prevent invalid current_question values
            if current_question > total_questions:
                return redirect('quiz')  # Restart the quiz if the session state is invalid

            form = QuizForm(request.POST, current_question=current_question)
            if form.is_valid():
                user_answer = form.cleaned_data.get(f'q{current_question}')
                correct_answer = correct_answers.get(f'q{current_question}')
                
                if user_answer == correct_answer:
                    score += 1
                request.session['score'] = score

                if current_question < total_questions:
                    request.session['current_question'] = current_question + 1
                    return redirect('quiz')
                else:
                    # Quiz is complete
                    percentage = (score / total_questions) * 100

                    # Save result in the database
                    QuizResult.objects.create(
                        name=name,
                        score=score,
                        total_questions=total_questions
                    )

                    # Render result page
                    response = render(request, 'quiz1/result.html', {
                        'name': name,
                        'score': score,
                        'percentage': percentage,
                        'total_questions': total_questions
                    })

                    # Clear only quiz-related session data
                    request.session.pop('name', None)
                    request.session.pop('current_question', None)
                    request.session.pop('score', None)
                    return response

    # Handle GET requests
    else:
        name = request.session.get('name', '')
        if name:
            # Continue quiz
            current_question = request.session.get('current_question', 1)
            score = request.session.get('score', 0)
            total_questions = 10  # Replace with `len(correct_answers)` if dynamic

            # Prevent invalid question numbers
            if current_question > total_questions:
                return redirect('quiz')  # Restart quiz if out of range

            form = QuizForm(current_question=current_question)
            return render(request, 'quiz1/quiz.html', {
                'form': form,
                'name': name,
                'current_question': current_question,
                'score': score
            })
        else:
            # Show name form
            form = NameForm()
            return render(request, 'quiz1/name.html', {'form': form})
