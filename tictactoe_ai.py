#!/usr/bin/python
from fltk import *
import copy
import random

#x is 1, o is -1


class Game:
	player = 1
	board = [['', '', ''] for _ in range(3)] #board[row][col]
	end = False

def find3(board, lastplayer, lastmove=None):
	if lastmove == None:
		return False
	else:
		r, c = lastmove
		
		#look for rows
		if board[r]==[lastplayer, lastplayer, lastplayer]:
			return True
		#look for columns
		if (board[0][c], board[1][c], board[2][c]) == (lastplayer, lastplayer, lastplayer):
			return True
		#look for diagonals
		diags = ([board[i][j] for i, j in ((0,0),(1,1),(2,2))],[board[i][j] for i, j in ((0,2),(1,1),(2,0))])
		if diags[0] == [lastplayer,lastplayer,lastplayer] or diags[1] == [lastplayer,lastplayer,lastplayer]:
			return True
		else:
			return False

def showlabel(wid):
	r, c = wid.pos
	if wid.label() == None and Game.end == False:
		if Game.player == 1:
			wid.label('x')
		elif Game.player == -1:
			wid.label('o')
		else:
			raise Error
		Game.board[r][c] = Game.player
		if find3(Game.board, Game.player, wid.pos) == True:
			Game.end = True
			if Game.player == 1:
				winner = 'x'
			elif Game.player == -1:
				winner = 'o'
			fl_message(winner+' wins!')
		else:
			draw = True
			for but in butarray:
				if but.label() == None:
					draw = False
			if draw == True:
				Game.end = True
				fl_message('Draw!')
#		print ai_eval(copy.deepcopy(Game.board), Game.player, wid.pos)	
		Game.player *= -1
		if Game.player == -1:
			nr, nc = choose_move(Game.board, Game.player, wid.pos)
			showlabel(butarray[nr*3+nc])
			butarray[nr*3+nc].redraw()
	
def legals(board):
	empty = []
	for row in range(3):
		for col in range(3):
			if board[row][col] == '':
				empty.append((row,col))
	return empty

def ai_eval(board, lastplayer, lastmove):
	#returns (value, bestmoves)
	#no lastmove on first move; remember to account for
	if find3(board, lastplayer, lastmove):
		return (lastplayer*(len(legals(board))+1), None)
	else:
		#player 1 tries to max, player -1 tries to min
		tomove = lastplayer*-1
		if tomove == 1:
			best = -99
			bestmoves = []
			for move in legals(board):
				r, c = move
				nboard = copy.deepcopy(board)
				nboard[r][c] = tomove
				x = ai_eval(nboard, tomove, move)[0]
				if x > best:
					best = x
					bestmoves = [move]
				elif x == best:
					bestmoves.append(move)
			if best != -99:
				return (best, bestmoves)
		elif tomove == -1:
			best = 99
			bestmoves = []
			for move in legals(board):
				r, c = move
				nboard = copy.deepcopy(board)
				nboard[r][c] = tomove
				x = ai_eval(nboard, tomove, move)[0]
				if x < best:
					best = x
					bestmoves = [move]
				elif x == best:
					bestmoves.append(move)
			if best != 99:
				return (best, bestmoves)
		return (0, None)
	


def choose_move(board, tomove, lastmove):
	moves = ai_eval(board, tomove*-1, lastmove)[1]
	if moves != None:
		return random.choice(moves)
	else:
		return (0,0)

cwidth = 50  #cell width
cheight = 50 #cell height

w = Fl_Window(600,50,3*cwidth+15,3*cheight+15, 'Tictactoe')
w.begin()

butarray=[]

for row in range(3):
	for col in range(3):
		butarray.append(Fl_Button((cwidth*col+5),(cheight*row+5),cwidth, cheight))
		butarray[-1].pos = (row, col)
		butarray[-1].callback(showlabel)

w.end()

Fl.scheme('gtk+')
w.show()
Fl.run()


