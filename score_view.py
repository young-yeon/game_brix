from tkinter import *

class InputName():
    def __init__(self, master, score):
        self.master = master
        self.master.title('Please Input your Name')
        self.master.geometry('500x200')
        self.score = score

        self.input = Entry(self.master, font = ('양재깨비체B', 20), width = 10)
        self.input.place(x = 150, y = 50)

        self.Please_input = StringVar()
        self.Please_input.set('Please input your name')
        self.Please_input_lbl = Label(self.master, \
                                      textvariable = self.Please_input, \
                                      font = ('양재깨비체B', 20), width = 25)
        self.Please_input_lbl.place(x = 30, y = 0)

        self.input_txt = StringVar()
        self.input_txt.set('input name :')
        self.input_lbl = Label(self.master, \
                               textvariable = self.input_txt, \
                               font = ('양재깨비체B', 10), width = 10)
        self.input_lbl.place(x = 50, y = 50)

        self.prn_score = StringVar()
        self.prn_score.set('You were clear in {} seconds.'.format(self.score))
        self.score_lbl = Label(self.master, \
                               textvariable = self.prn_score, \
                               font = ('양재깨비체B', 15), width = 25)
        self.score_lbl.place(x = 150, y = 150)

    def get_data(self):
        self.name = self.input.get()
        return self.name

class GetButton:
    def __init__(self, master, entry):
        self.master = master
        self.entry = entry
        self.btn = Button(self.master, text = 'Upload', \
                          font = ('양재깨비체B', 10), \
                          command = lambda : self.Push(), height = 2)
        self.btn.place(x = 350, y = 50)
        self.name = None

    def Push(self):
        self.name = self.entry.get_data()

        f = open('save.csv', mode='a')
        f.write('%s,%s\n' %(self.name, self.entry.score))
        f.close()

class ScoreWrite:
    def __init__(self, master, state):
        self.master = master
        self.master.title('Rank')
        self.master.geometry('500x750')
        self.state = state

    def data_print(self):
        self.view_design()

        f = open('save.csv', mode='r')
        datas = f.read().split('\n')
        datas.pop()

        for i in range(len(datas)):
            datas[i] = datas[i].split(',')

        if datas:
            tmp = datas[-1]

        sub_datas = []
        for data in datas:
            sub_datas.append(float(data[1]))
        sub_datas.sort()

        if len(sub_datas) < 20:
            for i in range(20-len(sub_datas)):
                sub_datas.append('-')
                datas.append(['-','-'])

        for i in range(20):
            sub_datas[i] = str(sub_datas[i])

        cnt = 0

        for i in range(20):
            for data in datas:
                if data[1] == sub_datas[i]:
                    self.lbl = StringVar()
                    self.lbl.set('#{}. {} : {} sec' \
                                .format(i+1, data[0], data[1]))
                    self.score_lbl = Label(self.master, \
                                        textvariable = self.lbl, \
                                        font = ('양재깨비체B', 20), width = 30)

                    if i < 10: self.score_lbl.config(foreground = 'red')

                    if i < 3: self.score_lbl.config(foreground = 'orange')

                    if self.state:
                        if data == tmp:
                            self.score_lbl.config(foreground = 'brown')

                    self.score_lbl.place(x = 30, y = cnt * 30 + 45)
                    datas.remove(data)
                    break

            cnt = cnt + 1

        for i in range(3):
            self.lbl = StringVar()
            self.lbl.set('.')
            self.score_lbl = Label(self.master, \
                                textvariable = self.lbl, \
                                font = ('양재깨비체B', 20), width = 30)
            self.score_lbl.place(x = 30, y = cnt * 30 + 45)

            cnt = cnt + 1

        f.close()

    def view_design(self):
        self.view_lbl = StringVar()
        self.view_lbl.set('== TOP Ranking ==')
        self.top_rank = Label(self.master, textvariable = self.view_lbl, \
                            font = ('양재깨비체B', 30), width = 23)
        self.top_rank.config(foreground = 'green')
        self.top_rank.place(x = 0, y = 0)

        cnt = 1

if __name__ == '__main__':
    print('''
    This is Module
    Please Run BallGame.py Instead.
    ''')
