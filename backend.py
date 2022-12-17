from flask import *
import json
import chess
from random import choice

def filter_moves_on_piece(moves, square):
    moves = [str(m) for m in moves]
    return json.dumps({'moves': [m[-2:] for m in moves if m[:2] == square]})

# create the app
app = Flask(__name__)


# start the board
board = chess.Board()

@app.route('/', methods=['POST', 'GET'])
def homepage():
    with open('website/index.html', 'r') as f:
        return f.read()

@app.route('/moves/<square>')
def get_moves(square):
    legal_moves = board.legal_moves
    return filter_moves_on_piece(legal_moves, square)

@app.route('/state')
def state():
    return json.dumps({'board': str(str(board).replace(" ", "")).replace("\n", "")})

@app.route('/move/<squareStart>/<squareEnd>')
def make_move(squareStart, squareEnd):
    board.push(chess.Move.from_uci(f"{squareStart.lower()}{squareEnd.lower()}"))
    wins = {'wins': choice(["Good move!", "Are you sure?", "lol", "plays in oregon", "i'm impressed", "why", "ouch", "william sucks", "only in ohio"])}
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            wins['wins'] = "black wins"
        else:
            wins['wins'] = "white wins"
    return wins

@app.route('/assets/<path:path>')
def get_assets(path):
    with open(f'website/assets/{path}', 'rb') as f:
        return f.read()

if __name__ == '__main__':
    app.run()
