import pygame
import os
'''
b_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
b_king = pygame.image.load(os.path.join("img", "black_king.png"))
b_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("img", "black_rook.png"))

w_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("img", "white_king.png"))
w_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

B = []
W = []

for img in b:
    B.append(pygame.transform.scale(img, (55, 55)))

for img in w:
    W.append(pygame.transform.scale(img, (55, 55)))
'''

class Piece:
    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False

    def isSelected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.valid_moves(board)

    def draw(self, win):
        '''if self.color == "w":
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]'''

        x = self.col * 57 + 260
        y = self.row * 57 + 165

        if self.selected:
            pygame.draw.rect(win, (0, 255, 0), (x, y, 57, 57), 4)
        if self.color == "w":
            pygame.draw.circle(win,(200,0,0),(x+26,y+26),15)
        else:
            pygame.draw.circle(win,(0,0,200),(x+26,y+26),15)

        '''if self.selected and self.color == color:  # Remove false to draw dots
            moves = self.move_list

            for move in moves:
                x = 33 + round(self.startX + (move[0] * self.rect[2] / 8))
                y = 33 + round(self.startY + (move[1] * self.rect[3] / 8))
                pygame.draw.circle(win, (255, 0, 0), (x, y), 10)'''

    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def __str__(self):
        return str(self.col) + " " + str(self.row)
    
    def add_valid_move(self,board,x,y):
        if x >=0 and x < 5 and y >= 0 and y < 5:
            if board[x][y] == 0:
                self.move_list.append((x,y))
    def valid_moves(self, board):
        y = self.col
        x = self.row

        self.move_list = []
        self.add_valid_move(board,x+1,y)
        self.add_valid_move(board,x-1,y)
        self.add_valid_move(board,x,y+1)
        self.add_valid_move(board,x,y-1)
        if (self.row + self.col) % 2 == 0:
            self.add_valid_move(board,x+1,y+1)
            self.add_valid_move(board,x+1,y-1)
            self.add_valid_move(board,x-1,y+1)
            self.add_valid_move(board,x-1,y-1)

