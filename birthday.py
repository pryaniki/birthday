import tkinter as tk
import os

from tkinter import ttk
from work_with_db import connect_to_db, test as t
from tkcalendar import Calendar, DateEntry
from datetime import date, timedelta, datetime  # working with a date



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

def processing_human_data(data: list) -> str:
    result = f'{data[0]} {data[1]} ({data[5]}) '
    if data[4] != 0:
        result = result + f'через {data[4]} д. '
    result = result + f'исполнится {int(data[2])}\n'
    return result

def create_interface():
    def butt_get_information():
        birthday_today = []
        birthdays = []
        if var.get() in (0, 1, 2, 3):
            data = connect_to_db(var.get())
        for people in data:
            if people[4] == 0:
                birthday_today.append(processing_human_data(people))
            else:
                birthdays.append(processing_human_data(people))

        background = '#d1d1d1'
        size_fount = 12
        win = tk.Toplevel(window)
        w = win.winfo_screenwidth()
        h = win.winfo_screenheight()
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 200  # смещение от середины
        h = h - 200

        # icon = tk.PhotoImage(file=f'image{os.sep}birthday-cake.png')
        # win.iconphoto(False, icon)
        win.config(bg=background)
        win.title('Birthday')
        win.resizable(False, False)
        width_win = 500
        height_win = 500

        win.geometry(f'{width_win}x{height_win}+800+50')
        tk.Label(win, bg=background, text='Сегодня День Рождения у следующих людей:', font=('', size_fount)) \
            .pack()  # Сегодня день рождения у следующих людей:
        frame1 = tk.Frame(win)
        frame1.pack()

        scrollbar = tk.Scrollbar(frame1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        birthday_today_listbox = tk.Listbox(frame1, yscrollcommand=scrollbar.set, width=60, font=('', size_fount))

        for birthday in birthday_today:
            birthday_today_listbox.insert(tk.END, birthday)

        birthday_today_listbox.pack(fill=tk.Y)
        scrollbar.config(command=birthday_today_listbox.yview)
        # l1 = tk.Label(win, bg='white', text=birthday_today, font=('', size_fount))
        # l1.pack()

        tk.Label(win, bg=background, text='Скоро День Рождения у следующих людей:', font=('', size_fount)) \
            .pack()  # Сегодня день рождения у следующих людей:

        frame2 = tk.Frame(win)
        frame2.pack()

        scrollbar = tk.Scrollbar(frame2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        birthdays_listbox = tk.Listbox(frame2, yscrollcommand=scrollbar.set, width=60, font=('', size_fount))

        for birthday in birthdays:
            birthdays_listbox.insert(tk.END, birthday)

        birthdays_listbox.pack(fill=tk.Y)
        scrollbar.config(command=birthdays_listbox.yview)

        # l2 = tk.Label(win, bg='white', text=birthdays, font=('', size_fount))
        # l2.pack()

        win.mainloop()

    def butt_add_birthday_boy():
        def check_data(any_date):
            #  Проверить все поля на правильность заполнения
            pass

        def get_date(date_1):
            # print(cal.get_date())
            date_1.delete(0, tk.END)
            # date_obj = datetime.strptime(str(cal.get_date()), '%Y-%m-%d')
            # date_str = datetime.strftime(date_obj, '%d-%m-%Y')
            # date_1.insert(0, date_str)

        def add_people():

            men = [ent_name.get(),
                   ent_surname.get(),
                   ent_patronymic.get(),
                   ent_date.get_date(),
                   ent_gender.get(),
                   ent_about_person.get()]

            check_data(men)

            print(f'{men}')

        background = '#d1d1d1'
        size_fount = 12
        win = tk.Toplevel(window)
        w = win.winfo_screenwidth()
        h = win.winfo_screenheight()
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 200  # смещение от середины
        h = h - 200
        width_win = 500
        height_win = 500
        # icon = tk.PhotoImage(file=f'image{os.sep}birthday-cake.png')
        # win.iconphoto(False, icon)
        win.config(bg='red')
        win.title('Birthday')
        # win.geometry(f'{width_win}x{height_win}+{w}+{h}')
        win.resizable(False, False)
        win.geometry(f'{width_win}x{height_win}+800+50')

        frame_warp = tk.Frame(win, width=width_win, height=height_win, bg=background)
        frame1 = tk.Frame(frame_warp, width=width_win, height=15, bg='black')
        frame2 = tk.Frame(frame_warp, width=width_win, height=15, bg='white')
        frame3 = tk.Frame(frame_warp, width=width_win, height=15, bg='black')
        frame_date_gender = tk.Frame(frame_warp, width=width_win, height=15, bg='white')
        frame_date = tk.Frame(frame_date_gender, width=width_win * (2 / 3), height=15, bg='yellow')
        frame_gender = tk.Frame(frame_date_gender, width=width_win * (1 / 3), height=15, bg='red')
        frame6 = tk.Frame(frame_warp, width=width_win, height=100, bg='white')
        frame7 = tk.Frame(frame_warp, width=width_win, height=40, bg='black')

        l_name = tk.Label(frame1, bg=background, text='Name* ', font=('', size_fount))  # Имя
        l_surname = tk.Label(frame2, bg=background, text='Surname* ', font=('', size_fount))  # Фамилия
        l_patronymic = tk.Label(frame3, bg=background, text='Patronymic ', font=('', size_fount))  # Отчество
        l_date = tk.Label(frame_date, bg=background, text='Date of birth* ', font=('', size_fount))  # Дата рождения
        l_gender = tk.Label(frame_gender, bg=background, text='Gender* ', font=('', size_fount))  # Пол
        l_about_person = tk.Label(frame6, height=5, bg=background, text='About a person ', font=('', size_fount))  #
        # О человеке

        ent_name = tk.Entry(frame1, font=('', size_fount))
        ent_surname = tk.Entry(frame2, font=('', size_fount))
        ent_patronymic = tk.Entry(frame3, font=('', size_fount))
        ent_date = DateEntry(frame_date, width=10, background='darkblue', font=('', size_fount),
                             foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        gender_value = ['male', 'female']
        ent_gender = ttk.Combobox(frame_gender, state="readonly", values=gender_value, font=('', size_fount))
        ent_about_person = tk.Entry(frame6, font=('', size_fount))

        button_add = tk.Button(frame7, text='Add a birthday boy', font=('', size_fount),
                               command=add_people)  # Добавить именинника

        frame_warp.pack()
        frame1.pack(fill=tk.X, padx=10, pady=10)
        frame2.pack(fill=tk.X, padx=10, pady=10)
        frame3.pack(fill=tk.X, padx=10, pady=10)
        frame_date_gender.pack(fill=tk.X, padx=10, pady=10)
        frame_date.pack(fill=tk.X, side=tk.LEFT)
        frame_gender.pack(fill=tk.X, side=tk.LEFT)
        frame6.pack(fill=tk.X, padx=10, pady=10)
        frame7.pack(fill=tk.X, padx=10, pady=10)

        l_name.pack(side='left')
        l_surname.pack(side='left')
        l_patronymic.pack(side='left')
        l_date.pack(side='left')
        l_gender.pack(side='left')
        l_about_person.pack(side='left')

        ent_name.pack(fill=tk.X, padx=10, side='right', expand=True)
        ent_surname.pack(fill=tk.X)
        ent_patronymic.pack(fill=tk.X)
        ent_date.pack(side='left')
        ent_gender.pack(side='left')
        ent_about_person.pack(fill=tk.X)

        button_add.pack()

        win.mainloop()

    def butt_all_bd_people():
        from work_with_db import get_all_data_from_table
        background = '#d1d1d1'
        size_fount = 12
        win = tk.Toplevel(window)
        w = win.winfo_screenwidth()
        h = win.winfo_screenheight()
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 200  # смещение от середины
        h = h - 200
        width_win = 1400
        height_win = 500

        # icon = tk.PhotoImage(file=f'image{os.sep}birthday-cake.png')
        # win.iconphoto(False, icon)
        win.config(bg=background)
        win.title('Birthday')
        win.geometry(f'{width_win}x{height_win}')
        win.resizable(False, False)

        frame_main = tk.Frame(win, width=width_win, height=15, bg='white')
        frame_main.pack(fill='both', expand=True)
        all_people = get_all_data_from_table()

        heads = ['id', 'name', 'surname', 'patronymic', 'birthday', 'gender', 'about person']
        table = ttk.Treeview(frame_main, show='headings')
        table['columns'] = heads
        table['displaycolumns'] = ['name', 'surname', 'patronymic', 'birthday', 'gender', 'about person', 'id']

        for header in heads:
            table.heading(header, text=header, anchor='center')
            table.column(header, anchor='center')

        for row in all_people:
            table.insert('', 'end', values=row)

        scroll_pane = ttk.Scrollbar(frame_main, command=table.yview)
        table.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side='right', fill=tk.Y)

        table.pack(expand=tk.YES, fill=tk.BOTH)

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
    window.geometry(f'400x400+{w}+{h}')
    window.resizable(False, False)

    l = tk.Label(window, bg=background, width=20, text='Select an interval.',
                 font=('', 12))
    l.pack(pady=10)

    var = tk.IntVar()
    var.set(0)

    day = tk.Radiobutton(window, text='Tomorrow', bg=background, variable=var, value=0)
    week = tk.Radiobutton(window, text='For this week', bg=background, variable=var, value=1)
    month = tk.Radiobutton(window, text='This month', bg=background, variable=var, value=2)
    year = tk.Radiobutton(window, text='This year', bg=background, variable=var, value=3)

    day.pack()
    week.pack()
    month.pack()
    year.pack()

    button1 = tk.Button(window, text='Find out the birthday people', command=butt_get_information)  # Узнать именинников
    button1.pack()
    button2 = tk.Button(window, text='Add a birthday boy', command=butt_add_birthday_boy)  # Добавить именинника
    button2.pack()
    button_all_bd_people = tk.Button(window, text='See all birthday people', command=butt_all_bd_people)  #
    # Просмотр всех именинников
    button_all_bd_people.pack()

    window.mainloop()


def test():
    pass


def main():
    #global connection

    test()
    create_interface()

    get_setiings(os.path.abspath('settings'))



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
