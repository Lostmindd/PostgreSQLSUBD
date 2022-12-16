from tkinter import *
import psycopg2

bg_color = "black"

def create_window():
    window = Tk()
    window.title("Окно авторизации")
    window.geometry('320x400')
    window.resizable(width=False, height=False)
    window["bg"] = bg_color

    notice = Label(
        text="вам нужно авторизоваться, чтобы получить доступ к БД!",
        fg="white",
        bg=bg_color,
        width=32,
        height=2,
        justify=CENTER,
        wraplength=320,
        font=("Verdana", 12)
    )
    database = Entry()
    user = Entry()
    password = Entry()
    host = Entry()
    port = Entry()

    notice.grid(row=1, column=0)
    database.grid(row=2, column=0)
    user.grid(row=3, column=0)
    password.grid(row=4, column=0)
    host.grid(row=5, column=0)
    port.grid(row=6, column=0)
    window.mainloop()
