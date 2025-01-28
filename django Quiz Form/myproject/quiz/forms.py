from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='What is your name?', max_length=100)

class QuizForm(forms.Form):
    QUESTIONS = {
        1: {
            'label': "Who is known as the father of Computer?", 
            'choices': [('a', 'Alan Turing'), ('b', 'Charles Babbage'), ('c', 'John von Neumann'), ('d', 'Ada Lovelace')]
        },
        2: {
            'label': "Who is the author of 'Pride and Prejudice'?", 
            'choices': [('a', 'Emily Brontë'), ('b', 'Charles Dickens'), ('c', 'Jane Austen'), ('d', 'Mark Twain')]
        },
        3: {
            'label': "What character have both Robert Downey Jr. and Benedict Cumberbatch played?", 
            'choices': [('a', 'Iron Man'), ('b', 'Sherlock Holmes'), ('c', 'Dr. Strange'), ('d', 'James Bond')]
        },
        4: {
            'label': "Which planet in the Milky Way is the hottest?", 
            'choices': [('a', 'Venus'), ('b', 'Mars'), ('c', 'Saturn'), ('d', 'Jupiter')]
        },
        5: {
            'label': "What city is known as The Eternal City?", 
            'choices': [('a', 'Athens'), ('b', 'Rome'), ('c', 'Paris'), ('d', 'Cairo')]
        },
        6: {
            'label': "Who discovered that the earth revolves around the sun?", 
            'choices': [('a', 'Galileo Galilei'), ('b', 'Isaac Newton'), ('c', 'Nicolaus Copernicus'), ('d', 'Johannes Kepler')]
        },
        7: {
            'label': "What sports car company manufactures the 911?", 
            'choices': [('a', 'Ferrari'), ('b', 'Lamborgini'), ('c', 'Porsche'), ('d', 'Buggati')]
        },
        8: {
            'label': "Which planet has the most moons?", 
            'choices': [('a', 'Venus'), ('b', 'Mars'), ('c', 'Saturn'), ('d', 'Jupiter')]
        },
        9: {
            'label': "How many bones do we have in an ear?", 
            'choices': [('a', '2'), ('b', '3'), ('c', '4'), ('d', '5')]
        },
        10: {
            'label': "What software company is headquartered in Redmond, Washington?", 
            'choices': [('a', 'Apple'), ('b', 'Google'), ('c', 'Microsoft'), ('d', 'Amazon')]
        }
    }

    def __init__(self, *args, current_question=None, **kwargs):
        super().__init__(*args, **kwargs)
        if current_question and current_question in self.QUESTIONS:
            question_data = self.QUESTIONS[current_question]
            self.fields[f'q{current_question}'] = forms.ChoiceField(
                label=question_data['label'],
                choices=question_data['choices'],
                widget=forms.RadioSelect
            )
