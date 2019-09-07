import tkinter
import data

cur_radio = None


def change_radio():
    data.change_render(cur_radio.get())


def tkinter_window():
    main_win = tkinter.Tk()
    main_win.geometry('200x200')
    main_win.title('Test')
    global cur_radio
    cur_radio = tkinter.IntVar()
    cur_radio.set(0)
    for index, item in enumerate(data.couple_list):
        radio = tkinter.Radiobutton(main_win, variable=cur_radio, text=item.left_camera.name + ' - ' + item.right_camera.name, value=index,
                                    indicatoron=0,
                                    command=change_radio)
        radio.pack()

    main_win.mainloop()


if __name__ == '__main__':
    tkinter_window()
