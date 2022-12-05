from piece import Piece
import time
import pygame


class Board:
    rect = (260,165,280,280)
    startX = rect[0]
    startY = rect[1]
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.ready = False

        self.last = None

        self.copy = True

        self.board = [[0 for x in range(cols)] for _ in range(rows)]

        self.board[0][0] = Piece(0, 0, "b")
        self.board[0][1] = Piece(0, 1, "b")
        self.board[0][2] = Piece(0, 2, "b")
        self.board[0][3] = Piece(0, 3, "b")
        self.board[0][4] = Piece(0, 4, "b")

        self.board[1][0] = Piece(1, 0, "b")
        self.board[1][4] = Piece(1, 4, "b")

        self.board[2][0] = Piece(2, 0, "b")
        self.board[2][4] = Piece(2, 4, "w")
        
        self.board[3][0] = Piece(3, 0, "w")
        self.board[3][4] = Piece(3, 4, "w")
        
        self.board[4][0] = Piece(4, 0, "w")
        self.board[4][1] = Piece(4, 1, "w")
        self.board[4][2] = Piece(4, 2, "w")
        self.board[4][3] = Piece(4, 3, "w")
        self.board[4][4] = Piece(4, 4, "w")

        self.p1Name = "Player 1"
        self.p2Name = "Player 2"

        self.turn = "w"

        self.time1 = 900
        self.time2 = 900

        self.storedTime1 = 0
        self.storedTime2 = 0

        self.winner = None

        self.startTime = time.time()

    def update_moves(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)
                    

    def draw(self, win, color):
        if self.last and color == self.turn:
            y, x = self.last[0]
            y1, x1 = self.last[1]

            xx = x * 57 + 260
            yy = y * 57 + 165
            pygame.draw.circle(win, (0,255,0), (xx+26, yy+26), 24, 4)
            xx1 = x1 * 57 + 260
            yy1 = y1 * 57 + 165
            pygame.draw.circle(win, (0,255,0), (xx1 + 26, yy1 + 26), 24, 4)

        #s = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win)
                    #if self.board[i][j].isSelected:
                    #    s = (i, j)


    '''def get_danger_moves(self, color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        for move in self.board[i][j].move_list:
                            danger_moves.append(move)

        return danger_moves

    def is_checked(self, color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].king and self.board[i][j].color == color:
                        king_pos = (j, i)

        if king_pos in danger_moves:
            return True

        return False'''

    def printb(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    print('0',end = " ")
                else:
                    print(self.board[i][j].color,end=" ")
            print()

    def select(self, col, row, color):
        changed = False
        prev = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        prev = (i, j)

        # if piece
        if self.board[row][col] == 0 and prev!=(-1,-1):
            moves = self.board[prev[0]][prev[1]].move_list
            if (row,col) in moves:
                print("move")
                changed = self.move(prev, (row, col), color)

        else:
            if prev == (-1,-1):
                self.reset_selected()
                if self.board[row][col] != 0 and self.board[row][col].color == color:
                    self.board[row][col].selected = True
                    ml = self.board[row][col].move_list
                    print("chose", row, '-',col)
                    print(ml)

        if changed:
            if self.turn == "w":
                self.turn = "b"
                self.reset_selected()
            else:
                self.turn = "w"
                self.reset_selected()

    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_mate(self, color):
        winner = True
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if color == "w":
                        if self.board[i][j].color == "b":
                            winner = False
                    if color == "b":
                        if self.board[i][j].color == "w":
                            winner = False

        return winner

    def move(self, start, end, color):
        changed = True
        nBoard = self.board[:]

        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard
        print("begin ganh")
        self.ganh(end,color)
        
        self.reset_selected()

        self.update_moves()

        self.last = [start, end]
        if self.turn == "w":
            self.storedTime1 += (time.time() - self.startTime)
        else:
            self.storedTime2 += (time.time() - self.startTime)
        self.startTime = time.time()

        return changed

    def valid(self,x,y,color):
        if x >=0 and x < 5 and y >= 0 and y < 5:
            if self.board[x][y]!= 0:
                if color == "w":
                    if self.board[x][y].color=="b":
                        return True
                if color == "b":
                    if self.board[x][y].color=="w":
                        return True
        return False
    
    def change_color(self,x,y,color):
        self.board[x][y] = Piece(x, y, color)
    
    def ganh(self,end,color):
        gl = []
        gl.append(end)
        print("ganh loop")
        while gl != []:
            x,y = gl.pop()
            print("do ganh")
            if self.valid(x-1,y,color) and self.valid(x+1,y,color):
                print("ganh doc",x,"-",y)
                self.change_color(x-1,y,color)
                self.change_color(x+1,y,color)
                gl.append((x-1,y))
                gl.append((x+1,y))
                if self.valid(x-2,y,color) and self.valid(x+2,y,color):
                    self.change_color(x-2,y,color)
                    self.change_color(x+2,y,color)
                    gl.append((x-2,y))
                    gl.append((x+2,y))
            if self.valid(x,y-1,color) and self.valid(x,y+1,color):
                print("ganh ngang")
                self.change_color(x,y-1,color)
                self.change_color(x,y+1,color)
                gl.append((x,y-1))
                gl.append((x,y+1))
                if self.valid(x,y-2,color) and self.valid(x,y+2,color):
                    self.change_color(x,y-2,color)
                    self.change_color(x,y+2,color)
                    gl.append((x,y-2))
                    gl.append((x,y+2))