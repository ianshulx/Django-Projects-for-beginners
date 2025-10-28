from django.shortcuts import render,redirect

# Create your views here.
def user_request(request):
    return render(request,"simple_quiz_app/index.html")



def submit_form(request):
    if request.method == 'POST':
        # Get submitted answers
        answers = {f'q{i}': request.POST.get(f'q{i}') for i in range(1, 11)}

        # Correct answers
        correct_answers = {
            'q1': 'Central Processing Unit',
            'q2': 'RAM',
            'q3': 'Stack',
            'q4': 'O(log n)',
            'q5': 'Network Layer',
            'q6': 'HTML',
            'q7': 'Structured Query Language',
            'q8': 'Quick Sort',
            'q9': 'Bit',
            'q10': 'Software that manages computer hardware',
        }

        # Calculate score
        score = sum(
            1 for key in correct_answers if answers.get(key) == correct_answers[key]
        )
        total = len(correct_answers)

        return render(request, 'simple_quiz_app/answer.html', {
            'answers': answers,
            'correct_answers': correct_answers,
            'score': score,
            'total': total,
        })

    return redirect('user_request')


