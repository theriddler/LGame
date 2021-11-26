# L Game
# Developed by Hunter Riddle & Max Lim Scrimali - 2021

from enum import Enum
import numpy as np
from colorama import Fore, Back, Style
from colorama import init as colorama_init
import tkinter as tk
from tkinter import *

colorama_init()

class Piece(Enum):
	coin = -1
	space = 0
	p1 = 1
	p2 = 2

	def __str__(self):
		if(self.value == -1):
			return 'coin'
		if(self.value == 0):
			return 'space'
		if(self.value == 1):
			return 'p1'
		if(self.value == 2):
			return 'p2'

def callback(event):
	print("clicked at", event.x, event.y)
	return



class GameBoard(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.canvas = tk.Canvas(self, width=420, height=420, borderwidth=5, highlightthickness=0)
		self.canvas.pack(side="top", fill="both", expand="false")
		self.board = [[Piece.coin, Piece.p1, Piece.p1, Piece.space], \
					[Piece.space, Piece.p2, Piece.p1, Piece.space], \
					[Piece.space, Piece.p2, Piece.p1, Piece.space], \
					[Piece.space, Piece.p2, Piece.p2, Piece.coin]]

		self.player_turn = 1
		self.p1_placed = 0
		self.p2_placed = 0

		self.piece_count = {}

	def _create_circle(self, x, y, r, **kwargs):
		return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

	tk.Canvas.create_circle = _create_circle

	def printBoard(self, array):
		cellwidth = 105
		cellheight = 105

		self.square = {}

		self.p1Locs = []
		self.p2Locs = []
		self.spaceLocs = []
		self.coinLocs = []

		for row in range(4):
			for column in range(4):
				x1 = column*cellwidth
				y1 = row*cellheight
				x2 = x1 + cellwidth - 5
				y2 = y1 + cellheight - 5
				self.printPiece(self.board[row][column], row, column, x1, y1, x2, y2)


	def printPiece(self, pieceType, row, column, x1, y1, x2, y2):

		# Coin
		if(pieceType == Piece.coin):
			self.square[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#ffffff", tags="rect", outline="")
			self.square[row,column] = self.canvas.create_circle((x2+x1)/2 ,(y2+y1)/2,40, fill="#000000", tags="rect", outline="")
			self.coinLocs.append([(x1,y1),(x2,y2)])

		# Space
		if(pieceType == Piece.space):
			self.square[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#ffffff", tags="rect", outline="")
			self.spaceLocs.append([(x1,y1),(x2,y2)])

		# Player 1
		if(pieceType == Piece.p1):
			self.square[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#ff0000", tags="rect", outline="")
			self.p1Locs.append([(x1,y1),(x2,y2)])

		# Player 2
		if(pieceType == Piece.p2):
			self.square[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#0000ff", tags="rect", outline="")
			self.p2Locs.append([(x1,y1),(x2,y2)])


	def howManyPieces(self, piece_type):
		# Count p1 placed
		self.piece_count[str(piece_type)] = 0

		for row in range(4):
			for column in range(4):
				if(self.board[row][column] == piece_type):
					self.piece_count[str(piece_type)] += 1

		return self.piece_count[str(piece_type)]

	def clearPieces(self, piece_type):
		for row in range(4):
			for column in range(4):
				if(self.board[row][column] == piece_type):
					self.placePiece(Piece.space, row, column)


	# Mouse Click Event Handler
	def mouseClick(self, event):
		xLocClick = event.x
		yLocClick = event.y
		print(event.x, event.y)

	# --- Player 1's Turn  -------------------------------------------------------- 
		if(self.player_turn == 1):

			# Count p1 placed
			p1_count = self.howManyPieces(Piece.p1)

			# Placing pieces 1-3
			if(p1_count < 3):
				array_column = self.mouseClickToArrayNotation(xLocClick)
				array_row = self.mouseClickToArrayNotation(yLocClick)

				if(self.board[array_row][array_column] == Piece.space):
					self.placePiece(Piece.p1, array_row, array_column)

			# Placing final piece (4)
			elif(p1_count == 3):
				array_column = self.mouseClickToArrayNotation(xLocClick)
				array_row = self.mouseClickToArrayNotation(yLocClick)

				if(self.board[array_row][array_column] == Piece.space):
					self.placePiece(Piece.p1, array_row, array_column)
				

			# All pieces are placed on the board (4 total)
			else:

				# Check if is legal L
				if(self.isLegalL(Piece.p1)):
					self.player_turn = -1
					pass

				# Check if user has clicked inside P1
				for location in self.p1Locs:
					if(xLocClick in range(location[0][0], location[1][0]) and yLocClick in range(location[0][1], location[1][1])):

						# Clear all pieces of P1
						self.clearPieces(Piece.p1)
						print(str(self.player_turn) +'p1' + str(location[0]) + str(location[1]))
						break



	# --- Player 1's (coin) Turn -------------------------------------------------------- 
		elif(self.player_turn == -1):
			coin_count = self.howManyPieces(Piece.coin)


			if(coin_count == 2):

				# If player has selected a coin location
				for location in self.coinLocs:
					if(xLocClick in range(location[0][0], location[1][0]) and yLocClick in range(location[0][1], location[1][1])):
						array_column = self.mouseClickToArrayNotation(xLocClick)
						array_row = self.mouseClickToArrayNotation(yLocClick)

						if(self.board[array_row][array_column] == Piece.space):
							self.placePiece(Piece.p1, array_row, array_column)

						print(str(self.player_turn) +'coin')

						# self.player_turn = 2



	# 	# Player 2's Turn
	# 	elif(self.player_turn == 2):
	# 		for location in self.p2Locs:
	# 			if(xLocClick in range(location[0][0], location[1][0]) and yLocClick in range(location[0][1], location[1][1])):
	# 				print(str(self.player_turn) +'p2')
	# 				self.player_turn = -2



	# 	# Player 2's Turn (coin variation)
	# 	elif(self.player_turn == -2):
	# 		for location in self.coinLocs:
	# 			if(xLocClick in range(location[0][0], location[1][0]) and yLocClick in range(location[0][1], location[1][1])):
	# 				print(str(self.player_turn) + 'coin')
	# 				self.player_turn = 1

	def isLegalL(self, piece_type):
		return False

		for row in range(4):
			for column in range(4):
				if(self.board[row][column] == Piece.p1):
					self.p1_placed += 1


	def placePiece(self, piece_type, row, column):
		self.board[row][column] = piece_type
		self.printBoard(self.board)


	def mouseClickToArrayNotation(self, n):
		if(n in range(0, 100)):
			return 0
		elif(n in range(105,205)):
			return 1
		elif(n in range(210, 310)):
			return 2
		elif(n in range(315, 420)):
			return 3








if __name__ == "__main__":
    app = GameBoard()
    app.printBoard(app.board)
    app.bind_all("<Button-1>", app.mouseClick)
    app.wm_title("L Game")
    app.minsize(420,450)
    app.maxsize(420,450)
    app.mainloop()
