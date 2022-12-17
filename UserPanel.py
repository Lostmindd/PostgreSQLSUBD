import tkinter.ttk as ttk
import tkinter as tk
import psycopg2


class UserPanel(object):
    def __init__(self, connect_cursor):
        self.connect_cursor = connect_cursor
        self.window = tk.Tk()
    bg_color = "gray75"


    def create_magazin_table(self):
        columns = ("magazin", "rayon", "kategor", "administrator", "adress",
                   "chas_rab", "telefon", "nazv")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
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
        scrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
        scrollbar.place(x=1364, y=103, height=521)
        table.configure(yscrollcommand=scrollbar.set)

    def create_kategor_table(self):
        columns = ("kategor", "nazv")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=300)
        table.column(column=1, width=707)
        table.heading("kategor", text="Категория")
        table.heading("nazv", text="Название")
        table.place(x=372, y=78)
        scrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
        scrollbar.place(x=1364, y=103, height=521)
        table.configure(yscrollcommand=scrollbar.set)
    def create_rayon_table(self):
        columns = ("rayon", "nazv", "kolvo_mag")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=300)
        table.column(column=1, width=300)
        table.column(column=2, width=407)
        table.heading("rayon", text="Район")
        table.heading("nazv", text="Название")
        table.heading("kolvo_mag", text="Количество магазинов")
        table.place(x=372, y=78)
        scrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
        scrollbar.place(x=1364, y=103, height=521)
        table.configure(yscrollcommand=scrollbar.set)
    def create_administrator_table(self):
        columns = ("administrator", "imya", "famil", "otch", "telefon")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=150)
        table.column(column=1, width=216)
        table.column(column=2, width=215)
        table.column(column=3, width=216)
        table.column(column=4, width=210)
        table.heading("administrator", text="Администратор")
        table.heading("imya", text="Имя")
        table.heading("famil", text="Фамилия")
        table.heading("otch", text="Отчество")
        table.heading("telefon", text="Телефон")
        table.place(x=372, y=78)
        scrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
        scrollbar.place(x=1364, y=103, height=521)
        table.configure(yscrollcommand=scrollbar.set)
    def create_magazin_kategor_rayon_view(self):
        columns = ("magazin_nazv", "kategor_nazv", "rayon_nazv")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=335)
        table.column(column=1, width=335)
        table.column(column=2, width=337)
        table.heading("magazin_nazv", text="Название магазина")
        table.heading("kategor_nazv", text="Название категории")
        table.heading("rayon_nazv", text="Название района")
        table.place(x=372, y=78)
        scrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
        scrollbar.place(x=1364, y=103, height=521)
        table.configure(yscrollcommand=scrollbar.set)
    def create_magazin_kruglosutoch_view(self):
        columns = ("magazin_magazin", "magazin_nazv")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=300)
        table.column(column=1, width=707)
        table.heading("magazin_magazin", text="Магазин")
        table.heading("magazin_nazv", text="Название Магазина")
        table.place(x=372, y=78)
        scrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
        scrollbar.place(x=1364, y=103, height=521)
        table.configure(yscrollcommand=scrollbar.set)
    def create_magazin_contact_data_view(self):
        columns = ("magazin_nazv", "magazin_adress", "magazin_telefon",
                   "administrator_fio", "administrator_telefon")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=150)
        table.column(column=1, width=307)
        table.column(column=2, width=150)
        table.column(column=3, width=250)
        table.column(column=4, width=150)
        table.heading("magazin_nazv", text="Название Магазина")
        table.heading("magazin_adress", text="Адрес Магазина")
        table.heading("magazin_telefon", text="Телефон Магазина")
        table.heading("administrator_fio", text="ФИО администратора")
        table.heading("administrator_telefon", text="Телефон администратора")
        table.place(x=372, y=78)
        scrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
        scrollbar.place(x=1364, y=103, height=521)
        table.configure(yscrollcommand=scrollbar.set)
    def create_magazin_count_by_kategor_view(self):
        columns = ("kategor_nazv", "magazin_count")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=707)
        table.column(column=1, width=300)
        table.heading("kategor_nazv", text="Название категории")
        table.heading("magazin_count", text="Количество магазинов")
        table.place(x=372, y=78)
        scrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
        scrollbar.place(x=1364, y=103, height=521)
        table.configure(yscrollcommand=scrollbar.set)
    def create_window(self):
        self.window.title("Окно пользователя")
        self.window.geometry('1400x700')
        self.window.resizable(width=False, height=False)
        self.window["bg"] = self.bg_color

        block = tk.Label(width=50, height=47, bg="grey38", relief=tk.RAISED)
        table_block = tk.Label(width=146, height=41, bg="grey25", relief=tk.RAISED)
        menu = tk.Label(
            text="Меню",
            fg="grey6", bg="grey38",
            width=5, height=1,
            font=("Arial Black", 50)  # Franklin Gothic
        )

        menu.place(x=62, y=20)
        table_block.place(x=363, y=41)
        block.place(x=0, y=0)

        magazin_button = tk.Button(text="Магазины",
                                 width=24, font=("Verdana", 12))
        kategor_button = tk.Button(text="Категории",
                                 width=24, font=("Verdana", 12))
        rayon_button = tk.Button(text="Районы",
                                 width=24, font=("Verdana", 12))
        admin_button = tk.Button(text="Администраторы",
                                 width=24, font=("Verdana", 12))
        magazin_button.place(x=370, y=47)
        kategor_button.place(x=625, y=47)
        rayon_button.place(x=879, y=47)
        admin_button.place(x=1134, y=47)

        view1_button = tk.Button(text="Магазин-категория-район",
                                   width=24, font=("Verdana", 12))
        view2_button = tk.Button(text="круглосуточные магазины",
                                   width=24, font=("Verdana", 12))
        view3_button = tk.Button(text="Круглосуточные магазины",
                                 width=24, font=("Verdana", 12))
        view4_button = tk.Button(text="Кол. магазинов (категории)",
                                 width=24, font=("Verdana", 12))
        view1_button.place(x=370, y=624)
        view2_button.place(x=625, y=624)
        view3_button.place(x=879, y=624)
        view4_button.place(x=1134, y=624)

        ######
        self.create_magazin_table()
        #self.create_kategor_table()
        #self.create_rayon_table()
        #self.create_administrator_table()
        #self.create_magazin_kategor_rayon_view()
        #self.create_magazin_kruglosutoch_view()
        #self.create_magazin_contact_data_view()
        #self.create_magazin_count_by_kategor_view()

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