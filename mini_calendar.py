try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from datetime import date, timedelta, datetime  # working with a date

from tkcalendar import Calendar, DateEntry

def example1():
    def print_sel():
        print(cal.selection_get())
        date_1.delete(0, tk.END)
        date_obj = datetime.strptime(str(cal.selection_get()), '%Y-%m-%d')
        date_str = datetime.strftime(date_obj, '%d-%m-%Y')
        date_1.insert(0, date_str)
        top.destroy()


    top = tk.Toplevel(root)
    date_1 = tk.Entry(root)
    date_1.pack()
    l1 = ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
    cal = Calendar(top,
                   font="Arial 14", selectmode='day',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()


def test(window):
    def example2():
        def get_date():
            print(cal.get_date())
            date_1.delete(0, tk.END)
            date_obj = datetime.strptime(str(cal.get_date()), '%Y-%m-%d')
            date_str = datetime.strftime(date_obj, '%d-%m-%Y')
            date_1.insert(0, date_str)
            # top.destroy()

        top = tk.Toplevel(root)

        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')

        ttk.Button(top, text="ok", command=get_date).pack()
        cal.pack(padx=10, pady=10)

    root = window
    s = ttk.Style(root)
    s.theme_use('clam')
    date_1 = tk.Entry(root)
    date_1.pack()
    ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
    ttk.Button(root, text='DateEntry', command=example2).pack(padx=10, pady=10)

    root.mainloop()





if __name__ == '__main__':
    test()
