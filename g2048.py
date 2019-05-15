import utime

def newNum(board, gg):
    xrand = gg.randint(0, 3)
    yrand = gg.randint(0, 3)
    while (board[xrand][yrand] > 0):
        xrand = gg.randint(0, 3)
        yrand = gg.randint(0, 3)
    board[xrand][yrand] = gg.randint(1, 2)

def showBoard(board, gg):
    gg.display.fill(0)
    x=20
    y=2
    spacing = 15
    max = 0;
    for r in board:
        for c in r:
            if c > max:
                max = c
            print(c, end=" ")
            if c == -1:
                gg.display.text("_ ", x, y)
            else:
                gg.display.text(str(c), x, y)
            x += spacing
        print()
        x = 20
        y += spacing

    gg.display.rect(18,0,58,58,1)
    gg.display.text("Score", 82, 22)
    gg.display.text(str(2**max), 82, 32)
    gg.display.show()


def goDown(board, gg):
    repeat = True
    while repeat:
        repeat = False
        for c in range(0,4):
            for r in range(0,3):
                if board[r][c] > 0:
                    if board[r+1][c] < 0:
                        board[r+1][c] = board[r][c]
                        board[r][c] = -1
                        repeat = True
                    elif board[r][c] == board[r+1][c]:
                        board[r+1][c] = board[r][c]+1
                        board[r][c] = -1
                        repeat = True
                    showBoard(board, gg)


def goUp(board, gg):
    repeat = True
    while repeat:
        repeat = False
        for c in range(0,4):
            for r in range(3,0,-1):
                if board[r][c] > 0:
                    if board[r-1][c] < 0:
                        board[r-1][c] = board[r][c]
                        board[r][c] = -1
                        repeat = True
                    elif board[r][c] == board[r-1][c]:
                        board[r-1][c] = board[r][c]+1
                        board[r][c] = -1
                        repeat = True
                    showBoard(board, gg)


def goRight(board, gg):
    repeat = True
    while repeat:
        repeat = False
        for r in range(0,4):
            for c in range(0,3):
                if board[r][c] > 0:
                    if board[r][c+1] < 0:
                        board[r][c+1] = board[r][c]
                        board[r][c] = -1
                        repeat = True
                    elif board[r][c] == board[r][c+1]:
                        board[r][c + 1] = board[r][c]+1
                        board[r][c] = -1
                        repeat = True
                    showBoard(board, gg)


def goLeft(board, gg):
    repeat = True
    while repeat:
        repeat = False
        for r in range(0,4):
            for c in range(3,0,-1):
                if board[r][c] > 0:
                    if board[r][c-1] < 0:
                        board[r][c-1] = board[r][c]
                        board[r][c] = -1
                        repeat = True
                    elif board[r][c] == board[r][c-1]:
                        board[r][c-1] = board[r][c]+1
                        board[r][c] = -1
                        repeat = True
                    showBoard(board, gg)


def isGameOver(board):
    for r in range(0, 3):
        for c in range(0, 3):
            if board[r][c] < 0:
                return False
    return True

def main(gg):
    board = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
    newNum(board, gg)
    newNum(board, gg)
    showBoard(board, gg)

    while(not isGameOver(board)):

        JoyX = gg.getJoyStickX()
        JoyY = gg.getJoyStickY()
        while JoyX > 300 and JoyX <700 and JoyY > 300 and JoyY <700:
            JoyX = gg.getJoyStickX()
            JoyY = gg.getJoyStickY()

        if JoyX > 700:
            goRight(board,gg)
        elif JoyX < 300:
            goLeft(board,gg)
        elif JoyY > 700:
            goDown(board, gg)
        elif JoyY < 300:
            goUp(board, gg)

        newNum(board, gg)
        showBoard(board, gg)

        utime.sleep_ms(200)
    #game is over
    gg.display.fill(0)
    gg.display.text("Game Over", 10, 10)
    gg.display.text(str(2**max), 10, 20)
    gg.display.show()
    utime.sleep_ms(3000)