from tkinter import *
import psycopg2
import hashlib
from functools import partial


class LoginWindow(object):
    def __init__(self, connect_cursor):
        self.connect_cursor = connect_cursor
    bg_color = "black"

    def bd_enter(self, login, passw):
        self.connect_cursor.execute("SELECT pass from auth where login = '"+ login.get() +"'")
        password = self.connect_cursor.fetchall()
        if len(password) == 0:
            print('нет такого пароля')
            return

        hash_pass = hashlib.sha1(passw.get().encode('utf-8'))
        if password[0][0] == hash_pass.hexdigest():
            print('Закрытие окна')
        else:
            print('Неверный пароль')
            return


    def create_window(self):
        window = Tk()
        window.title("Окно авторизации")
        window.geometry('320x400')
        window.resizable(width=False, height=False)
        window["bg"] = self.bg_color

        notice = Label(
            text="Вход",
            fg="white", bg=self.bg_color,
            width=4, height=3,
            justify=CENTER,
            font=("Verdana", 28)
        )
        login_note = Label(
            text="Пароль:",
            fg="white", bg=self.bg_color,
            width=32, height=2,
            justify=CENTER,
            font=("Verdana", 12)
        )
        pass_note = Label(
            text="Логин:",
            fg="white", bg=self.bg_color,
            width=32, height=2,
            justify=CENTER,
            font=("Verdana", 12)
        )
        empty = Label(width=32, height=2, bg=self.bg_color)
        login = Entry(width=24, font=("Verdana", 12))
        password = Entry(width=24, font=("Verdana", 12))
        enter_button = Button(text="Вход",
                              width=8, font=("Verdana", 12),
                              command=partial(self.bd_enter, login, password))

        notice.grid(row=1, column=0)
        login_note.grid(row=2, column=0)
        login.grid(row=3, column=0)
        pass_note.grid(row=4, column=0)
        password.grid(row=5, column=0)
        empty.grid(row=6, column=0)
        enter_button.grid(row=7, column=0)
        window.mainloop()
