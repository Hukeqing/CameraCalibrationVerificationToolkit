import tkinter
import data


def changeradio():
    data.change_render(r'D:\PhotoCheck\checkbox\left\left1.png', False)


def tkinterwindow():
    mainwin = tkinter.Tk()
    mainwin.geometry('200x200')
    mainwin.title('Test')
    global curradio
    curradio = tkinter.IntVar()
    curradio.set(0)
    radio1 = tkinter.Radiobutton(mainwin, variable=curradio, text='Cam1-Cam2', value=0, indicatoron=0,
                                 command=changeradio)
    radio2 = tkinter.Radiobutton(mainwin, variable=curradio, text='Cam1-Cam3', value=1, indicatoron=0,
                                 command=changeradio)
    radio3 = tkinter.Radiobutton(mainwin, variable=curradio, text='Cam1-Cam4', value=2, indicatoron=0,
                                 command=changeradio)
    radio1.pack()
    radio2.pack()
    radio3.pack()
    mainwin.mainloop()


if __name__ == '__main__':
    tkinterwindow()
