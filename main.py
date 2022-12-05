import minmax as mm
import welcome
import random
import demo
import sys
import pygame
from client import Network
import playing
#from client import Network
import os
rect = (260,165,280,280)

turn = "w"
def main():
    while True:
        status = welcome.welcome2(screen)
        if status == 1:
            ###############
            goFirst,level,mode=welcome.welcome(screen)
            #If user decided to escape
            if(goFirst==-1 and level==-1):
                print("Program exited.")
                sys.exit()
            ###############
            #Who get to go first
            if (goFirst==1): player=-1 
            else: player=1 
            ###############
            #Setting up board
            mm.board()
            ###############
            #Current board
            res=[mm.dupTable(mm.board.current_board)]
            ###############
            counter=0
            demo.move(mm.board.current_board,screen,counter)
            win=0
            while True:
                previous_board=mm.board.copy_board(mm.board.current_board)

                if (player==-1): #Bot -1
                    move=mm.board.select_move(player,level)
                    if move==None: 
                        win=1
                        break
                else:            #Random Agent 1
                    valid_move_temp=mm.board.get_valid_moves(mm.board.current_board, mm.board.previous_board, player)
                    if(len(valid_move_temp)==0):
                        win=-1
                        break
                    if(mode==1):
                        index=random.randint(0,len(valid_move_temp)-1)
                        move=valid_move_temp[index]
                    elif(mode==0):
                        a,b=playing.play(mm.board.current_board,screen,counter,valid_move_temp,1)
                        if(a==-1 and b==-1):
                            sys.exit()
                        move=mm.Move(mm.Position(a[0],a[1]),mm.Position(b[0],b[1]))
                #Move
                mm.board.act_move(mm.board.current_board,move,player)
                mm.board.previous_board=mm.board.copy_board(previous_board)
                counter+=1

                #Update to UI
                demo.move(mm.board.current_board,screen,counter)

                #Print to terminal for Debugging
                for i in range(5): print(mm.board.current_board[i])
                print()
                res.append(mm.dupTable(mm.board.current_board))
                player=-player
                if(counter>=100):
                    score=0
                    for i in range(5):
                        for j in range(5):
                            if(mm.board.current_board[i][j]==1): score-=1
                            elif(mm.board.current_board[i][j]==-1): score+=1
                    if(score>0):
                        win=-1
                    elif(score<0):
                        win=1
                    else:
                        win=0
                    break
            restart=demo.resDisOut(win,res,len(res),screen)
            res=[]
            mm.board.current_board=[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
            mm.board.previous_board=[[]]
            if(restart):pass
            else: break
        elif status == 2:
            menu_screen(screen, name)


def menu_screen(win, name):
    global bo, rect, turn
    run = True
    offline = False

    while run:
        #win.fill((131,238,255))
        small_font = pygame.font.SysFont("comicsans", 50)
        
        if offline:
            off = small_font.render("Server Offline, Try Again Later...", 1, (255, 0, 0))
            win.blit(off, (width / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        
        offline = False
        try:
            bo = connect()
            run = False
            main2()
            break
        except:
            print("Server Offline")
            offline = True

   
def redraw_gameWindow(win, bo, p1, p2, color, ready):
    #win.blit(board, (0, 0))
    win.fill((131,238,255))
    board=[pygame.Rect(255,160,290,290),pygame.Rect(260,165,280,280)]
    pygame.draw.rect(win,(139,69,19),board[0])
    pygame.draw.rect(win,(255,222,173),board[1])
    pygame.draw.line(win,(0,0,0),(260,165),(540,445),5)
    pygame.draw.line(win,(0,0,0),(260,445),(540,165),5)
    pygame.draw.line(win,(0,0,0),(400,165+26),(540-26,305),5)
    pygame.draw.line(win,(0,0,0),(400,165+26),(260+26,305),5)
    pygame.draw.line(win,(0,0,0),(400,445-26),(260+26,305),5)
    pygame.draw.line(win,(0,0,0),(400,445-26),(540-26,305),5)
    for i in range(5):
        pygame.draw.line(win,(0,0,0),(260+28+56*i,445),(260+28+56*i,165),5)
        pygame.draw.line(win,(0,0,0),(260,165+28+56*i),(540,165+28+56*i),5)
    bo.draw(win, color)

    formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if int(p1%60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2%60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

    font = pygame.font.SysFont("comicsans", 30)
    try:
        txt = font.render(bo.p2Name + "\'s Time: " + str(formatTime2), 1, (255, 255, 255))
        txt2 = font.render(bo.p1Name + "\'s Time: " + str(formatTime1), 1, (255,255,255))
    except Exception as e:
        print(e)
    win.blit(txt, (520,10))
    win.blit(txt2, (520, 550))

    txt = font.render("Press q to Quit", 1, (255, 255, 255))
    win.blit(txt, (10, 20))

    if color == "s":
        txt3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        win.blit(txt3, (width/2-txt3.get_width()/2, 10))

    if not ready:
        show = "Waiting for Player"
        if color == "s":
            show = "Waiting for Players"
        font = pygame.font.SysFont("comicsans", 80)
        txt = font.render(show, 1, (255, 0, 0))
        win.blit(txt, (width/2 - txt.get_width()/2, 220))

    if not color == "s":
        font = pygame.font.SysFont("comicsans", 30)
        if color == "w":
            txt3 = font.render("YOU ARE RED", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))
        else:
            txt3 = font.render("YOU ARE BLUE", 1, (0, 0, 255))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))

        if bo.turn == color:
            txt3 = font.render("YOUR TURN", 1, (0, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 550))
        else:
            txt3 = font.render("THEIR TURN", 1, (0, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 550))

    pygame.display.update()


def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text,1, (255,0,0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False


def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            divX = x - rect[0]
            divY = y - rect[1]
            i = int(divX / (rect[2]/5))
            j = int(divY / (rect[3]/5))
            return i, j

    return -1, -1


def connect():
    global n
    n = Network()
    return n.board


def main2():
    global turn, bo, name

    color = bo.start_user
    count = 0

    bo = n.send("update_moves")
    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    run = True
    print("Go")
    while run:
        if not color == "s":
            p1Time = bo.time1
            p2Time = bo.time2
            if count == 60:
                bo = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(30)

        try:
            redraw_gameWindow(screen, bo, p1Time, p2Time, color, bo.ready)
        except Exception as e:
            print(e)
            end_screen(screen, "Other player left")
            run = False
            break

        if not color == "s":
            if p1Time <= 0:
                bo = n.send("winner b")
            elif p2Time <= 0:
                bo = n.send("winner w")

            if bo.check_mate("b"):
                bo = n.send("winner b")
            elif bo.check_mate("w"):
                bo = n.send("winner w")

        if bo.winner == "w":
            end_screen(screen, "RED is the Winner!")
            run = False
        elif bo.winner == "b":
            end_screen(screen, "BLUE is the winner")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and color != "s":
                    # quit game
                    if color == "w":
                        bo = n.send("winner b")
                    else:
                        bo = n.send("winner w")

                if event.key == pygame.K_RIGHT:
                    bo = n.send("forward")

                if event.key == pygame.K_LEFT:
                    bo = n.send("back")


            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if color == bo.turn and bo.ready:
                    pos = pygame.mouse.get_pos()
                    print("check1")
                    bo = n.send("update moves")
                    print("check")
                    i, j = click(pos)
                    print(i,"-",j)
                    bo = n.send("select " + str(i) + " " + str(j) + " " + color)
                    bo.printb()
    
    n.disconnect()
    bo = 0
    menu_screen(screen)

clock = pygame.time.Clock()
clock.tick(30)
name = input("Please type your name: ")
pygame.init() 
#Setting up UI
width = 800
screen=pygame.display.set_mode((width,600))
pygame.display.set_caption("Cờ gánh")
icon = pygame.image.load("./img/logo.png")
pygame.display.set_icon(icon)
main()