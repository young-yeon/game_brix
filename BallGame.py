from tkinter import *
from time import *
from random import *
import pygame, csv
import score_view

class Ball:
    def __init__(self, canvas, color, paddle):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill = color)
        self.canvas.move(self.id, 245, 200)

        self.x = 0
        while not self.x : self.x = randint(-3, 3)
        self.y = 4

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

        self.paddle = paddle
        self.Gamelose = False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        self.pos = self.canvas.coords(self.id)

        if self.pos[1] <= 0:
            self.y = 4
        if self.pos[3] >= self.canvas_height:
            self.Gamelose = True
        if self.hit_paddle():
            self.y = -4
            self.x += randint(-50, 50) / 50
            if self.x > 4 : self.x = 4
            if self.x < -4 : self.x = -4
        if self.pos[0] <= 0 or self.pos[2] >= self.canvas_width:
            self.x = self.x * -1

    def hit_paddle(self):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if self.pos[2] >= paddle_pos[0] and self.pos[0] <= paddle_pos[2]:
            if self.pos[3] >= paddle_pos[1] and paddle_pos[3] >= self.pos[3]:
                return True
        return False

class Paddle:
    def __init__(self, canvas, color, score):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill = color)
        self.canvas.move(self.id, 200, 700)
        self.score = score

        self.x = 0

        self.canvas_width = self.canvas.winfo_width()

        self.started = False

        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<Key>', self.start)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

    def turn_left(self, event):
        self.x = -3

    def turn_right(self, event):
        self.x = 3

    def start(self, event):
        self.started = True
        global start_time
        start_time = time()
        self.score.Game_time = time()

class Block:
    def __init__(self, canvas, color, ball):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 46, 28, fill = color)
        self.ball = ball

    def move(self, point_x, point_y):
        self.canvas.move(self.id, point_x, point_y)

    def checkBall(self, BallPos):
        self.pos = self.canvas.coords(self.id)
        if BallPos[2] >= self.pos[0] and BallPos[0] <= self.pos[2]:
            if BallPos[3] >= self.pos[1] and self.pos[3] >= BallPos[3]:
                self.ball.y = self.ball.y*-1
                self.canvas.move(self.id, 1000, 1000)
                self.canvas.itemconfig(self.id, state = 'hidden')
                return True
        return  False

class Score:
    def __init__(self, canvas, color):
        self.Game_time = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 780, text = self.Game_time, \
                                    font=('양재깨비체B', 20), fill = color)

    def update(self):
        self.score = '%.2f' %(time() - self.Game_time)
        self.canvas.itemconfig(self.id, text = self.score, \
                               font=('양재깨비체B', 20))

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load('main_bgm.mp3')
    pygame.mixer.music.play()

    tk = Tk()
    tk.title("Brix Buster")
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=800, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()

    block_count = 40
    line = 4

    score = Score(canvas, 'red')
    paddle = Paddle(canvas, 'red', score)
    ball = Ball(canvas, 'orange', paddle)
    Blocks = []
    for i in range(40):
        Blocks.append(Block(canvas, 'brown', ball))
        Blocks[i].move((i % 10) * 50 + 2, (i // 10)*30 + 2)

    while True:
        if paddle.started:
            ball.draw()
            paddle.draw()
            score.update()
            for B in Blocks:
                if B.checkBall(ball.pos):
                    block_count = block_count - 1

            if time() - start_time > 45:
                start_time = time()
                for B in Blocks:
                    B.move(0, 30)

                for i in range(10):
                    Blocks.append(Block(canvas, 'brown', ball))
                    Blocks[i + line * 10].move(i * 50 + 2, 2)

                block_count = block_count + 10
                line = line + 1

        tk.update_idletasks()
        tk.update()
        sleep(0.01)

        if ball.Gamelose:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('lose_3s.mp3')
            pygame.mixer.music.play()

            img = PhotoImage(file = 'lose.png')
            lbl = Label(tk, image = img)
            lbl.image = img
            lbl.place(x = 90, y = 200)
            tk.update_idletasks()
            tk.update()
            sleep(3)
            pygame.mixer.music.stop()
            Clear = False
            break

        if block_count == 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('win_4s.mp3')
            pygame.mixer.music.play()

            img = PhotoImage(file = 'win.png')
            lbl = Label(tk, image = img)
            lbl.image = img
            lbl.place(x = 90, y = 200)
            tk.update_idletasks()
            tk.update()
            sleep(4)
            pygame.mixer.music.stop()
            Clear = True
            break

    tk.destroy()

    if Clear:
        Input = Tk()
        set = score_view.InputName(Input, score.score)
        get = score_view.GetButton(Input, set)

        while get.name == None:
            Input.update_idletasks()
            Input.update()

        Input.destroy()

    Write = Tk()
    datas = score_view.ScoreWrite(Write,Clear)
    datas.data_print()

    Write.mainloop()
