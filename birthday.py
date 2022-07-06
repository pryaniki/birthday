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
    if data[4] == 0:
        return result + f'исполнилось {int(data[2])}\n'
    return result + f'через {data[4]} д. исполнится {int(data[2])}\n'


def set_window_location(window, width_win, height_win, width_offset=0, height_offset=0):
    """
    Функция располагает окно на экране
    Если оставить width_offset=0, height_offset=0, то окно
    будет выровнено по центру
    """
    if width_offset == height_offset == 0:
        center_screen_x = window.winfo_screenwidth() // 2  # середина экрана
        center_screen_y = window.winfo_screenheight() // 2
        width_offset = center_screen_x - int(width_win / 2)  # смещение по ширине
        height_offset = center_screen_y - int(height_win / 2)  # смещение по высоте

    window.geometry(f'{width_win}x{height_win}+{width_offset}+{height_offset}')


def create_interface():
    def butt_get_information():
        birthday_today = []
        birthdays = []
        data = None
        if var.get() in (0, 1, 2, 3):
            data = connect_to_db('get_birthdays_from_people', [var.get()])
        else:
            print('Ошибка в функции butt_get_information')
        if data:
            for people in data:
                if people[4] == 0:
                    birthday_today.append(processing_human_data(people))
                else:
                    birthdays.append(processing_human_data(people))
        else:
            print('У вас нет именинников, вы можете их добавить')

        background = '#d1d1d1'
        size_fount = 12
        win = tk.Toplevel(window)
        win.config(bg=background)
        win.resizable(False, False)
        set_window_location(win, width_win=500, height_win=500)

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
        win.config(bg='#d1d1d1')
        win.title('Birthday')
        win.resizable(False, False)
        width_win = 500
        height_win = 500
        set_window_location(win, width_win=width_win, height_win=height_win)

        frame_warp = tk.Frame(win, width=width_win, height=height_win, bg=background)
        frame_warp.pack()
        f_name = tk.Frame(frame_warp, width=width_win, height=15, bg='#d1d1d1')
        f_surname = tk.Frame(frame_warp, width=width_win, height=15, bg='white')
        f_patronymic = tk.Frame(frame_warp, width=width_win, height=15, bg='#d1d1d1')
        f_date_gender = tk.Frame(frame_warp, width=width_win, height=15, bg='white')
        f_date = tk.Frame(f_date_gender, width=width_win * (2 / 3), height=15, bg='#d1d1d1')
        f_gender = tk.Frame(f_date_gender, width=width_win * (1 / 3), height=15, bg='red')
        f_about_person = tk.Frame(frame_warp, width=width_win, height=100, bg='white')
        f_butt_add = tk.Frame(frame_warp, width=width_win, height=40, bg='#d1d1d1')

        l_name = tk.Label(f_name, bg=background, text='Name* ', font=('', size_fount))  # Имя
        l_surname = tk.Label(f_surname, bg=background, text='Surname* ', font=('', size_fount))  # Фамилия
        l_patronymic = tk.Label(f_patronymic, bg=background, text='Patronymic ', font=('', size_fount))  # Отчество
        l_date = tk.Label(f_date, bg=background, text='Date of birth* ', font=('', size_fount))  # Дата рождения
        l_gender = tk.Label(f_gender, bg=background, text='Gender* ', font=('', size_fount))  # Пол
        l_about_person = tk.Label(f_about_person, height=5, bg=background, text='About a person ',
                                  font=('', size_fount))  #
        # Информация о человеке

        ent_name = tk.Entry(f_name, font=('', size_fount))
        ent_surname = tk.Entry(f_surname, font=('', size_fount))
        ent_patronymic = tk.Entry(f_patronymic, font=('', size_fount))
        ent_date = DateEntry(f_date, width=10, background='darkblue', font=('', size_fount),
                             foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        gender_value = ['male', 'female']
        ent_gender = ttk.Combobox(f_gender, state="readonly", values=gender_value, font=('', size_fount))
        ent_about_person = tk.Entry(f_about_person, font=('', size_fount))

        tk.Button(f_butt_add, text='Add a birthday boy', font=('', size_fount), command=add_people).pack()  # Добавить именинника
        tk.Button(f_butt_add, text='Clear information', font=('', size_fount), command=clear_frame).pack()

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
            win.config(bg='red')
            win.title('Birthday')
            win.resizable(False, False)
            set_window_location(win, width_win=500, height_win=500)

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
        win.config(bg=background)
        win.resizable(False, False)

        center_screen_x = win.winfo_screenwidth() // 2  # середина экрана
        center_screen_y = win.winfo_screenheight() // 2
        width_win = 1400
        height_win = 500
        width_offset = center_screen_x - int(width_win / 2)  # смещение по ширине
        height_offset = center_screen_y - int(height_win / 2)  # смещение по высоте
        win.geometry(f'{width_win}x{height_win}+{width_offset}+{height_offset}')

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

        tk.Label(frame_main, bg=background, text='Id* ', font=('', size_fount)).pack()  # Имя
        ent_id = tk.Entry(frame_main, font=('', size_fount))  # является ли числом
        ent_id.pack()
        tk.Button(frame_main, text='Change birthday boy', font=('', size_fount),
                               command=butt_change_birthday_boy).pack()  # Добавить именинника

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
    home = os.getcwd()
    icon_path = home + f'{os.sep}data{os.sep}icons{os.sep}cake.ico'
    window.iconphoto(True, tk.PhotoImage(file=icon_path))
    window.config(bg=background)
    window.title('Birthday')
    window.resizable(False, False)
    set_window_location(window, width_win=400, height_win=400)

    tk.Label(window, bg=background, width=20, text='Select an interval.', font=('', 12)).pack(pady=10)

    var = tk.IntVar()
    var.set(0)

    tk.Radiobutton(window, text='Tomorrow', bg=background, variable=var, value=0).pack()
    tk.Radiobutton(window, text='For this week', bg=background, variable=var, value=1).pack()
    tk.Radiobutton(window, text='This month', bg=background, variable=var, value=2).pack()
    tk.Radiobutton(window, text='This year', bg=background, variable=var, value=3).pack()

    tk.Button(window, text='Find out the birthday people', command=butt_get_information).pack()  # Узнать именинников
    tk.Button(window, text='Add a birthday person', command=butt_add_birthday_boy).pack()  # Добавить именинника
    tk.Button(window, text='See all birthday people', command=butt_all_bd_people).pack()  # Просмотр всех именинников
    tk.Button(window, text='Exporting data to file people1.csv', command=butt_export_data_to_file).pack()
    tk.Button(window, text='Import data from file people.csv', command=butt_import_date_from_file).pack()

    window.mainloop()


def main():
    #get_setiings(os.path.abspath('settings'))
    #path = os.getcwd() + f'{os.sep}dist{os.sep}start_with_system{os.sep}start_with_system.exe'
    #print(path.split(str(os.sep)).join('\\'))
    #print(os.getcwd() + f'{os.sep*2}dist{os.sep*2}start_with_system{os.sep*2}start_with_system.exe')
    #start_with_system('E:\\Programs\\My_programs\\birthday\\dist\\start_with_system\\start_with_system.exe')
    #start_with_system(os.getcwd() + f'{os.sep}dist{os.sep}start_with_system{os.sep}start_with_system.exe')

    create_interface()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
