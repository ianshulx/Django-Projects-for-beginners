from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    if 'board' not in request.session:
        request.session['board'] = ['' ] * 9
        request.session['current_player'] = 'X'
    
    board = request.session['board']
    current_player = request.session['current_player']
    winner = check_winner(board)
    
    context = {
        'board': board,
        'current_player': current_player,
        'winner': winner,
        'draw': '' not in board and not winner,
    }
    return render(request, 'game/index.html', context)

@csrf_exempt
def make_move(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        position = data.get('position')
        
        board = request.session['board']
        current_player = request.session['current_player']
        
        if board[position] == '' and not check_winner(board):
            board[position] = current_player
            request.session['board'] = board
            request.session['current_player'] = 'O' if current_player == 'X' else 'X'
        
        winner = check_winner(board)
        return JsonResponse({
            'board': board,
            'current_player': request.session['current_player'],
            'winner': winner,
            'draw': '' not in board and not winner,
        })

@csrf_exempt
def reset_game(request):
    request.session['board'] = ['' ] * 9
    request.session['current_player'] = 'X'
    return JsonResponse({'status': 'ok'})

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]
    return None