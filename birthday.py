import tkinter as tk
import os

from psycopg2 import sql  # import sql
from work_with_db import connect_to_db


def is_accessible(path, mode='r'):
    """
    Проверка, является ли файл или папка из `path`
    доступным для работы в предоставленным `mode` формате.
    """
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True


def get_setiings(fileName):
    if (is_accessible(fileName)):
        f = open(fileName, 'r')
        #       for line in f:
        #          print(line)
        f.close()


def test():
    str = print('e')
    #print(str)


def processing_human_data(data: list) -> str:
    result = f'{data[0]} {data[1]} ({data[3]}) '
    if data[4] != 0:
        result = result + f'через {int(data[4])} д. '
    result = result + f'исполнится {int(data[2])}\n'
    return result


def create_interface():


    def about():
        a = tk.Toplevel()
        a.geometry('200x150')
        a['bg'] = 'grey'
        a.overrideredirect(True)
        tk.Label(a, text="About this") \
            .pack(expand=1)
        a.after(5000, lambda: a.destroy())

    def get_information():
        birthday_today = ''
        birthdays = ''
        if var.get() in (0, 1, 2):
            data = connect_to_db(var.get())
            counter = 1
        for people in data:
            if people[4] == 0:
                birthday_today = birthday_today + processing_human_data(people)
            else:
                birthdays = birthdays + processing_human_data(people)

        background = '#d1d1d1'
        size_fount = 12
        win = tk.Tk()
        w = win.winfo_screenwidth()
        h = win.winfo_screenheight()
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 200  # смещение от середины
        h = h - 200

        #icon = tk.PhotoImage(file=f'image{os.sep}birthday-cake.png')
        #win.iconphoto(False, icon)
        win.config(bg=background)
        win.title('Birthday')
        win.geometry(f'500x700+{w}+{h}')
        win.resizable(False, False)

        win.geometry('500x700+800+50')
        tk.Label(win, bg=background, text='Сегодня День Рождения у следующих людей:', font=('', size_fount)) \
            .pack()  # Сегодня день рождения у следующих людей:
        l1 = tk.Label(win, bg='white', text=birthday_today, font=('', size_fount))
        l1.pack()

        tk.Label(win, bg=background, text='Скоро День Рождения у следующих людей:', font=('', size_fount)) \
            .pack()  # Сегодня день рождения у следующих людей:
        l2 = tk.Label(win, bg='white', text=birthdays, font=('', size_fount))
        l2.pack()

        win.mainloop()

    background = '#599ede'
    window = tk.Tk()
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 200  # смещение от середины
    h = h - 200

    icon = tk.PhotoImage(file=f'image{os.sep}birthday-cake.png')
    window.iconphoto(False, icon)
    window.config(bg=background)
    window.title('Birthday')
    window.geometry(f'400x200+{w}+{h}')
    window.resizable(False, False)

    l = tk.Label(window, bg=background, width=20, text='Select an interval.',
                 font=('', 12))
    l.pack()

    var = tk.IntVar()
    var.set(0)

    day = tk.Radiobutton(text='Tomorrow', bg=background, variable=var, value=0)
    week = tk.Radiobutton(text='For this week', bg=background, variable=var, value=1)
    month = tk.Radiobutton(text='This month', bg=background, variable=var, value=2)
    #year = tk.Radiobutton(text='This year', bg=background, variable=var, value=3)

    day.pack()
    week.pack()
    month.pack()
    #year.pack()
    button1 = tk.Button(text='Find out the birthday people', command=get_information)  # Узнать именинников
    button1.pack()


    window.mainloop()


def main():
    global connection
    create_interface()
    # test()
    get_setiings(os.path.abspath('settings'))
    connect_to_db(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
