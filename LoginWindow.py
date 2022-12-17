import tkinter as tk
import psycopg2
import hashlib
from functools import partial


class LoginWindow(object):
    def __init__(self, connect_cursor):
        self.connect_cursor = connect_cursor
        self.window = tk.Tk()
        self.level = -1
    bg_color = "black"

    def try_enter(self, login, passw, errmsg):
        self.connect_cursor.execute("SELECT pass, level from auth where login = '" + login.get() + "'")
        password = self.connect_cursor.fetchall()
        if len(password) == 0:
            errmsg.set('Аккаунта с таким логином не существует')
            return

        hash_pass = hashlib.sha1(passw.get().encode('utf-8'))
        if password[0][0] == hash_pass.hexdigest():
            self.level = password[0][1]
            self.window.destroy()
        else:
            errmsg.set('Неверный пароль')
            return

    def create_window(self):
        self.window.title("Окно авторизации")
        self.window.geometry('320x400')
        self.window.resizable(width=False, height=False)
        self.window["bg"] = self.bg_color

        notice = tk.Label(
            text="Вход",
            fg="white", bg=self.bg_color,
            width=4, height=3,
            justify=tk.CENTER,
            font=("Verdana", 28)
        )
        login_note = tk.Label(
            text="Логин:",
            fg="white", bg=self.bg_color,
            width=32, height=2,
            justify=tk.CENTER,
            font=("Verdana", 12)
        )
        pass_note = tk.Label(
            text="Пароль:",
            fg="white", bg=self.bg_color,
            width=32, height=2,
            justify=tk.CENTER,
            font=("Verdana", 12)
        )
        empty = tk.Label(width=32, height=2, bg=self.bg_color)
        login = tk.Entry(width=24, font=("Verdana", 12))
        password = tk.Entry(width=24, font=("Verdana", 12), show="*")
        errmsg = tk.StringVar()
        enter_button = tk.Button(text="Вход",
                              width=8, font=("Verdana", 12),
                              command=partial(self.try_enter, login, password, errmsg))

        error_note = tk.Label(foreground="red", textvariable=errmsg, wraplength=250,
                           bg=self.bg_color, font=("Verdana", 10))

        notice.grid(row=1, column=0)
        login_note.grid(row=2, column=0)
        login.grid(row=3, column=0)
        pass_note.grid(row=4, column=0)
        password.grid(row=5, column=0)
        empty.grid(row=6, column=0)
        enter_button.grid(row=7, column=0)
        error_note.grid(row=8, column=0)
        self.window.mainloop()
        return self.level
