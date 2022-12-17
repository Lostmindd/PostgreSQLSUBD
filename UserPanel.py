import tkinter as tk
import psycopg2


class UserPanel(object):
    def __init__(self, connect_cursor):
        self.connect_cursor = connect_cursor
        self.window = tk.Tk()
    bg_color = "white"
    def create_window(self):
        self.window.title("Окно пользователя")
        self.window.geometry('1000x800')
        self.window.resizable(width=False, height=False)
        self.window["bg"] = self.bg_color

        self.window.mainloop()