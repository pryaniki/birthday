import os
import sys
import tkinter as tk

from tkinter import ttk
from work_with_db import connect_to_db
from tkcalendar import Calendar, DateEntry
from datetime import date, timedelta, datetime  # working with a date


def start_with_system(path_to_file):
    import os
    from win32com.client import Dispatch

    wDir, f_name = os.path.split(path_to_file)
    user_path = os.path.expanduser('~')  # Путь к папке пользователя

    path = os.path.join(wDir, f"{f_name}.lnk")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = path_to_file
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = path_to_file
    shortcut.save()

    if sys.platform == "win32":  # Windows
        if not os.path.exists(
                f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{f_name}"):
            os.system(
                f'copy "{path}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')
            print(f'{f_name} добавлен в автозагрузку')
    os.remove(path)


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


def get_setiings(f_name):
    if is_accessible(f_name):
        f = open(f_name, 'r')
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
            data = connect_to_db('get_birthdays_from_people', [var.get()])
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

        win.config(bg=background)
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

    def butt_add_birthday_boy():
        def check_data(any_date):
            #  Проверить все поля на правильность заполнения
            #  Удалить лишние пробелы
            pass

        def get_date(date_1):
            date_obj = datetime.strptime(str(date_1), '%Y-%m-%d')
            date_str = datetime.strftime(date_obj, '%Y-%m-%d')
            return date_str

        def add_people():
            men = [ent_name.get(),
                   ent_surname.get(),
                   ent_patronymic.get(),
                   get_date(ent_date.get_date()),
                   ent_gender.get().replace(' ', ''),
                   ent_about_person.get()]

            men = list(map(str, men))

            check_data(men)
            connect_to_db('insert_to_people', [men])

        def clear_frame():
            ent_name.delete(0, tk.END)
            ent_surname.delete(0, tk.END)
            ent_patronymic.delete(0, tk.END)
            # ent_date.set_date()
            ent_gender.set('')
            ent_about_person.delete(0, tk.END)

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
        win.config(bg='red')
        win.title('Birthday')
        win.geometry(f'{width_win}x{height_win}+{w}+{h}')
        win.resizable(False, False)

        frame_warp = tk.Frame(win, width=width_win, height=height_win, bg=background)
        f_name = tk.Frame(frame_warp, width=width_win, height=15, bg='black')
        f_surname = tk.Frame(frame_warp, width=width_win, height=15, bg='white')
        f_patronymic = tk.Frame(frame_warp, width=width_win, height=15, bg='black')
        f_date_gender = tk.Frame(frame_warp, width=width_win, height=15, bg='white')
        f_date = tk.Frame(f_date_gender, width=width_win * (2 / 3), height=15, bg='yellow')
        f_gender = tk.Frame(f_date_gender, width=width_win * (1 / 3), height=15, bg='red')
        f_about_person = tk.Frame(frame_warp, width=width_win, height=100, bg='white')
        f_butt_add = tk.Frame(frame_warp, width=width_win, height=40, bg='black')

        l_name = tk.Label(f_name, bg=background, text='Name* ', font=('', size_fount))  # Имя
        l_surname = tk.Label(f_surname, bg=background, text='Surname* ', font=('', size_fount))  # Фамилия
        l_patronymic = tk.Label(f_patronymic, bg=background, text='Patronymic ', font=('', size_fount))  # Отчество
        l_date = tk.Label(f_date, bg=background, text='Date of birth* ', font=('', size_fount))  # Дата рождения
        l_gender = tk.Label(f_gender, bg=background, text='Gender* ', font=('', size_fount))  # Пол
        l_about_person = tk.Label(f_about_person, height=5, bg=background, text='About a person ',
                                  font=('', size_fount))  #
        # О человеке

        ent_name = tk.Entry(f_name, font=('', size_fount))
        ent_surname = tk.Entry(f_surname, font=('', size_fount))
        ent_patronymic = tk.Entry(f_patronymic, font=('', size_fount))
        ent_date = DateEntry(f_date, width=10, background='darkblue', font=('', size_fount),
                             foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        gender_value = ['male', 'female']
        ent_gender = ttk.Combobox(f_gender, state="readonly", values=gender_value, font=('', size_fount))
        ent_about_person = tk.Entry(f_about_person, font=('', size_fount))

        button_add = tk.Button(f_butt_add, text='Add a birthday boy', font=('', size_fount),
                               command=add_people)  # Добавить именинника
        button_clear = tk.Button(f_butt_add, text='Clear information', font=('', size_fount),
                                 command=clear_frame)

        frame_warp.pack()
        f_name.pack(fill=tk.X, padx=10, pady=10)
        f_surname.pack(fill=tk.X, padx=10, pady=10)
        f_patronymic.pack(fill=tk.X, padx=10, pady=10)
        f_date_gender.pack(fill=tk.X, padx=10, pady=10)
        f_date.pack(fill=tk.X, side=tk.LEFT)
        f_gender.pack(fill=tk.X, side=tk.LEFT)
        f_about_person.pack(fill=tk.X, padx=10, pady=10)
        f_butt_add.pack(fill=tk.X, padx=10, pady=10)

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
        button_clear.pack()

    def butt_all_bd_people():

        def butt_change_birthday_boy():
            def check_data(any_date):
                #  Проверить все поля на правильность заполнения
                #  Удалить лишние пробелы
                pass

            def get_date(date_1):
                date_obj = datetime.strptime(str(date_1), '%Y-%m-%d')
                date_str = datetime.strftime(date_obj, '%Y-%m-%d')
                return date_str

            def fill_fields():
                from work_with_db import connect_to_db
                if not ent_id.get().isdigit():
                    print('ведите целое число')
                else:
                    data = connect_to_db('get_person_by_id', [ent_id.get()])
                    if not data:
                        print('Такого id нет в базе данных')

                    return data[0][1:]

            def change_people():
                men = [ent_name.get(),
                       ent_surname.get(),
                       ent_patronymic.get(),
                       get_date(ent_date.get_date()),
                       ent_gender.get(),
                       ent_about_person.get()]

                men = list(map(str, men))

                check_data(men)
                connect_to_db('update_people', [ent_id.get(), men])

            def clear_frame():
                ent_name.delete(0, tk.END)
                ent_surname.delete(0, tk.END)
                ent_patronymic.delete(0, tk.END)
                # ent_date.set_date()
                ent_gender.set('')
                ent_about_person.delete(0, tk.END)

            name, surname, patronymic, bd_date, gender, about_person = fill_fields()

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

            win.config(bg='red')
            win.title('Birthday')
            win.geometry(f'{width_win}x{height_win}+{w}+{h}')
            win.resizable(False, False)


            frame_warp = tk.Frame(win, width=width_win, height=height_win, bg=background)
            f_name = tk.Frame(frame_warp, width=width_win, height=15, bg='black')
            f_surname = tk.Frame(frame_warp, width=width_win, height=15, bg='white')
            f_patronymic = tk.Frame(frame_warp, width=width_win, height=15, bg='black')
            f_date_gender = tk.Frame(frame_warp, width=width_win, height=15, bg='white')
            f_date = tk.Frame(f_date_gender, width=width_win * (2 / 3), height=15, bg='yellow')
            f_gender = tk.Frame(f_date_gender, width=width_win * (1 / 3), height=15, bg='red')
            f_about_person = tk.Frame(frame_warp, width=width_win, height=100, bg='white')
            f_butt_add = tk.Frame(frame_warp, width=width_win, height=40, bg='black')

            l_name = tk.Label(f_name, bg=background, text='Name* ', font=('', size_fount))  # Имя
            l_surname = tk.Label(f_surname, bg=background, text='Surname* ', font=('', size_fount))  # Фамилия
            l_patronymic = tk.Label(f_patronymic, bg=background, text='Patronymic ', font=('', size_fount))  # Отчество
            l_date = tk.Label(f_date, bg=background, text='Date of birth* ', font=('', size_fount))  # Дата рождения
            l_gender = tk.Label(f_gender, bg=background, text='Gender* ', font=('', size_fount))  # Пол
            l_about_person = tk.Label(f_about_person, height=5, bg=background, text='About a person ',
                                      font=('', size_fount))  #
            # О человеке

            ent_name = tk.Entry(f_name, textvariable=name, font=('', size_fount))
            ent_surname = tk.Entry(f_surname, font=('', size_fount))
            ent_patronymic = tk.Entry(f_patronymic, font=('', size_fount))
            ent_date = DateEntry(f_date, width=10, background='darkblue', font=('', size_fount),
                                 foreground='white', borderwidth=2, date=bd_date, date_pattern='dd-mm-yyyy')
            gender_value = ['male', 'female']
            ent_gender = ttk.Combobox(f_gender, state="readonly", values=gender_value, font=('', size_fount))
            ent_about_person = tk.Entry(f_about_person, font=('', size_fount))
            ent_name.insert(0, name)
            ent_surname.insert(0, surname)
            ent_patronymic.insert(0, patronymic)
            ent_date.set_date(bd_date)
            ent_gender.set(gender)
            ent_about_person.insert(0, about_person)

            button_сhange = tk.Button(f_butt_add, text='Change a birthday boy', font=('', size_fount),
                                      command=change_people)  # Добавить именинника
            button_clear = tk.Button(f_butt_add, text='Clear information', font=('', size_fount),
                                     command=clear_frame)

            frame_warp.pack()
            f_name.pack(fill=tk.X, padx=10, pady=10)
            f_surname.pack(fill=tk.X, padx=10, pady=10)
            f_patronymic.pack(fill=tk.X, padx=10, pady=10)
            f_date_gender.pack(fill=tk.X, padx=10, pady=10)
            f_date.pack(fill=tk.X, side=tk.LEFT)
            f_gender.pack(fill=tk.X, side=tk.LEFT)
            f_about_person.pack(fill=tk.X, padx=10, pady=10)
            f_butt_add.pack(fill=tk.X, padx=10, pady=10)

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

            button_сhange.pack()
            button_clear.pack()

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

        win.config(bg=background)
        win.geometry(f'{width_win}x{height_win}')
        win.resizable(False, False)

        frame_main = tk.Frame(win, width=width_win, height=15, bg='white')
        frame_main.pack(fill='both', expand=True)
        all_people = connect_to_db('get_people', [])
        heads = ['id', 'name', 'surname', 'patronymic', 'birthday', 'gender', 'about person']
        table = ttk.Treeview(frame_main, show='headings')
        table['columns'] = heads
        table['displaycolumns'] = ['id', 'name', 'surname', 'patronymic', 'birthday', 'gender', 'about person']

        for header in heads:
            table.heading(header, text=header, anchor='center')
            table.column(header, anchor='center')

        for row in all_people:
            table.insert('', 'end', values=row)

        scroll_pane = ttk.Scrollbar(frame_main, command=table.yview)
        table.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side='right', fill=tk.Y)

        table.pack(expand=tk.YES, fill=tk.BOTH)

        l_name = tk.Label(frame_main, bg=background, text='Id* ', font=('', size_fount))  # Имя
        ent_id = tk.Entry(frame_main, font=('', size_fount))  # является ли числом

        button_add = tk.Button(frame_main, text='Change birthday boy', font=('', size_fount),
                               command=butt_change_birthday_boy)  # Добавить именинника
        button_add.pack()
        l_name.pack()
        ent_id.pack()

    def butt_import_date_from_file():
        """
        Загрузить данные из файла
        """
        connect_to_db('import_data', ['people.csv'])

    def butt_export_data_to_file():
        """
        Выгружает данные в файл
        """
        import csv
        f_name = 'people1.csv'
        data = connect_to_db('get_people', [])
        data = list(map(lambda x: x[1:], data))
        with open(f_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    background = '#599ede'
    window = tk.Tk()
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 200  # смещение от середины
    h = h - 200
    home = os.getcwd()
    icon_path = home + f'{os.sep}image{os.sep}cake.ico'
    icon = tk.PhotoImage(file=icon_path)
    window.iconphoto(True, icon)
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
    but_export_date = tk.Button(window, text='Exporting data to file people1.csv', command=butt_export_data_to_file)
    but_import_date = tk.Button(window, text='Import data from file people.csv', command=butt_import_date_from_file)

    but_export_date.pack()
    but_import_date.pack()

    window.mainloop()


def test():
    pass


def main():
    # get_setiings(os.path.abspath('settings'))
    # start_with_system('E:\\Programs\\My_programs\\birthday\\dist\\start_with_system\\start_with_system.exe')

    home = os.getcwd()
    icon_path = home + f'{os.sep}image{os.sep}cake.ico'
    create_interface()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
