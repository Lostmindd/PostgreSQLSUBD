from tkinter import ttk
import tkinter as tk
import psycopg2


class UserPanel(object):
    def __init__(self):  #connect_cursor
        # self.connect_cursor = connect_cursor
        self.window = tk.Tk()
    bg_color = "gray75"


    def create_magazin_table(self):
        columns = ("magazin", "rayon", "kategor", "administrator", "adress",
                   "chas_rab", "telefon", "nazv")
        table = ttk.Treeview(columns=columns, show="headings")
        table.column(column=0, width=70)
        table.column(column=1, width=70)
        table.column(column=2, width=70)
        table.column(column=3, width=100)
        table.column(column=4, width=277)
        table.column(column=5, width=100)
        table.column(column=6, width=120)
        table.column(column=7, width=200)
        table.heading("magazin", text="Магазин")
        table.heading("rayon", text="Район")
        table.heading("kategor", text="Категория")
        table.heading("administrator", text="Администратор")
        table.heading("adress", text="Адресс")
        table.heading("chas_rab", text="Часы Работы")
        table.heading("telefon", text="Телефон")
        table.heading("nazv", text="Название")
        table.place(x=372, y=78)


    def create_kategor_table(self):
        columns = ("kategor", "nazv")
        table = ttk.Treeview(columns=columns, show="headings")
        table.column(column=0, width=300)
        table.column(column=1, width=707)
        table.heading("kategor", text="Категория")
        table.heading("nazv", text="Название")
        table.place(x=372, y=78)

    def create_rayon_table(self):
        columns = ("rayon", "nazv", "kolvo_mag")
        table = ttk.Treeview(columns=columns, show="headings")
        table.column(column=0, width=300)
        table.column(column=1, width=300)
        table.column(column=2, width=407)
        table.heading("rayon", text="Район")
        table.heading("nazv", text="Название")
        table.heading("kolvo_mag", text="Количество магазинов")
        table.place(x=372, y=78)


    def create_window(self):
        self.window.title("Окно пользователя")
        self.window.geometry('1400x700')
        self.window.resizable(width=False, height=False)
        self.window["bg"] = self.bg_color

        block = tk.Label(width=50, height=47, bg="grey38", relief=tk.RAISED)
        table_block = tk.Label(width=144, height=36, bg="grey10", relief=tk.RAISED)
        menu = tk.Label(
            text="Меню",
            fg="grey6", bg="grey38",
            width=5, height=1,
            font=("Arial Black", 50)  # Franklin Gothic
        )


        menu.place(x=62, y=20)
        table_block.place(x=370, y=76)
        block.place(x=0, y=0)
        ######
        #self.create_magazin_table()
        #self.create_kategor_table()
        self.create_rayon_table()

        # enter_button = tk.Button(text="Вход",
        #                          width=50, font=("Verdana", 12),
        #                          command=lambda: tree.lower())
        # enter_button2 = tk.Button(text="Вход",
        #                          width=50, font=("Verdana", 12),
        #                          command=lambda: tree.lift())
        # enter_button2.place(x=30, y=30)
        # enter_button.place(x=0, y=0)
        #определяем заголовки
        # tree.heading("name", text="Имя")
        # tree.heading("age", text="Возраст")
        # tree.heading("email", text="Email")


        ######







        self.window.mainloop()