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

class GameBoard(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title("L Game")
		self.bind_all("<Button-1>", self.mouseClick)
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
		self.firstMove = True
		self.p1hasMoved = False
		self.p2hasMoved = False


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

		print(str(piece_type),  " - Cleared")


	# Mouse Click Event Handler
	def mouseClick(self, event):
		xLocClick = event.x
		yLocClick = event.y
		print(event.x, event.y)



	# --- Player 1's Turn  --------------------------------------------------------
		if(self.player_turn == 1):

			if(not self.p1hasMoved):
				self.temp_p1_locs = self.p1Locs
				self.p1hasMoved = True

			# Check if user has clicked inside P1
			for location in self.p1Locs:
				if(xLocClick in range(location[0][0], location[1][0]) and yLocClick in range(location[0][1], location[1][1])):

					self.clearPieces(Piece.p1)
					self.firstMove = False
					return

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
			elif(p1_count == 4):

				# Check if user has clicked inside P1
				if(self.firstMove):
					# Clear all pieces of P1 and break out of mouseClick()
					self.clearPieces(Piece.p1)
					self.firstMove = False
					return

				# Check if is legal L
				elif(self.isLegalL(Piece.p1)):
					self.player_turn = -1
					self.firstMove = True
					self.hasMoved = False
					print("P1 - LEGAL L PLACED")

				elif(not self.isLegalL(Piece.p1)):
					print("ILLEGAL MOVE")
					self.clearPieces(Piece.p1)


	# --- Player 1's (coin) Turn --------------------------------------------------------
		elif(self.player_turn == -1):
			coin_count = self.howManyPieces(Piece.coin)

			#  All coins are on board (user to select removal)
			if(coin_count == 2):

				# Get correct self.board[row][column]
				array_row = self.mouseClickToArrayNotation(yLocClick)
				array_column = self.mouseClickToArrayNotation(xLocClick)

				# If selected a valid 'coin'
				if(self.board[array_row][array_column] == Piece.coin):
					self.placePiece(Piece.space, array_row, array_column)


			# User has removed a coin
			if(coin_count == 1):
				array_row = self.mouseClickToArrayNotation(yLocClick)
				array_column = self.mouseClickToArrayNotation(xLocClick)

				# If selected a valid 'coin'
				if(self.board[array_row][array_column] == Piece.space):
					self.placePiece(Piece.coin, array_row, array_column)
					self.player_turn = 2

						# debug
					print("P1 - COIN PLACED")
					return



	# --- Player 2 Turn  --------------------------------------------------------
		if(self.player_turn == 2):

			if(not self.p2hasMoved):
				self.temp_p2_locs = self.p2Locs
				self.p2hasMoved = True

			for location in self.p2Locs:
				if(xLocClick in range(location[0][0], location[1][0]) and yLocClick in range(location[0][1], location[1][1])):

					self.clearPieces(Piece.p2)
					self.firstMove = False
					print("P2 - Cleared")
					return


			# Count p1 placed
			p2_count = self.howManyPieces(Piece.p2)

			# Placing pieces 1-3
			if(p2_count < 3):
				array_column = self.mouseClickToArrayNotation(xLocClick)
				array_row = self.mouseClickToArrayNotation(yLocClick)

				if(self.board[array_row][array_column] == Piece.space):
					self.placePiece(Piece.p2, array_row, array_column)

			# Placing final piece (4)
			elif(p2_count == 3):
				array_column = self.mouseClickToArrayNotation(xLocClick)
				array_row = self.mouseClickToArrayNotation(yLocClick)

				if(self.board[array_row][array_column] == Piece.space):
					self.placePiece(Piece.p2, array_row, array_column)


			# All pieces are placed on the board (4 total)
			elif(p2_count == 4):

				# Check if user has clicked inside P1
				if(self.firstMove):

					# Clear all pieces of P1 and break out of mouseClick()
					self.clearPieces(Piece.p2)
					self.firstMove = False
					return

				# Check if is legal L
				elif(self.isLegalL(Piece.p2)):
					self.player_turn = -2
					self.firstMove = True
					self.hasMoved = False
					print("P2 - LEGAL L PLACED")

				elif(not self.isLegalL(Piece.p2)):
					print("ILLEGAL MOVE")
					self.clearPieces(Piece.p2)



	# --- Player 2 (coin) Turn --------------------------------------------------------
		elif(self.player_turn == -2):
			coin_count = self.howManyPieces(Piece.coin)

			#  All coins are on board (user to select removal)
			if(coin_count == 2):

				# Get correct self.board[row][column]
				array_row = self.mouseClickToArrayNotation(yLocClick)
				array_column = self.mouseClickToArrayNotation(xLocClick)

				# If selected a valid 'coin'
				if(self.board[array_row][array_column] == Piece.coin):
					self.placePiece(Piece.space, array_row, array_column)


			# User has removed a coin
			if(coin_count == 1):
				array_row = self.mouseClickToArrayNotation(yLocClick)
				array_column = self.mouseClickToArrayNotation(xLocClick)

				# If selected a valid 'coin'
				if(self.board[array_row][array_column] == Piece.space):
					self.placePiece(Piece.coin, array_row, array_column)
					self.player_turn = 1

						# debug
					print("P2 - COIN PLACED")
					return



	def isLegalL(self, piece_type):

		# Create list of player locations
		locations = []
		main_body = []

		for row in range(4):
			for column in range(4):
				if(self.board[row][column] == piece_type):
					locations.append((row, column))

		print(locations)

		# Create set of 3 locations that share an equal value {L1, L2, L3}
		for L in range(4):

			L1 = L
			L2 = (L+1)%4
			L3 = (L+2)%4

			# If X of 0, 1, 2 are equal
			if(locations[L1][0] == locations[L2][0] and locations[L2][0] == locations[L3][0]):

				# Sort by Y VALUE (coz X is equal)
				main_body = [locations[L1], locations[L2], locations[L3]]
				main_body.sort(key = lambda x: x[1])
				break

			# If Y of 0, 1, 2 are equal
			if(locations[L1][1] == locations[L2][1] and locations[L2][1] == locations[L3][1]):

				# Sort by X VALUE (coz Y is equal)
				main_body = [locations[L1], locations[L2], locations[L3]]
				main_body.sort(key = lambda x: x[0])
				break

		# Return false if no main_body is found
		if(main_body == []):
			return False
		print(main_body)

		# Determine excluded location {L4}
		for L in locations:
			if(L not in main_body):
				L4 = L
				print(L)

		# Check {L4} is legal relative to {L1, L2, L3}
		L1 = main_body[0]
		L2 = main_body[1]
		L3 = main_body[2]

		if(L2[0] == L4[0] or L2[1] == L4[1]):
			return False

		if(L4[0] != L3[0] and L4[0] != L1[0] and L4[1] != L3[1] and L4[1] != L1[1]):
			return False

		if(self.p1hasMoved):
			if(self.temp_p1_locs == self.p1Locs):
				return False

		if(self.p2hasMoved):
			if(self.temp_p2_locs == self.p2Locs):
				return False

		return True


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
    # app.minsize(420,450)
    # app.maxsize(420,450)
    app.mainloop()
