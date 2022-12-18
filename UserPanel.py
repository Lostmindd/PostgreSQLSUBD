import tkinter.ttk as ttk
import tkinter as tk
import psycopg2


class UserPanel(object):
    def __init__(self, connect_cursor):
        self.connect_cursor = connect_cursor
        self.window = tk.Tk()
        self.table1 = self.create_magazin_table()
        self.table2 = self.create_kategor_table()
        self.table3 = self.create_rayon_table()
        self.table4 = self.create_administrator_table()
        self.table5 = self.create_magazin_kategor_rayon_view()
        self.table6 = self.create_magazin_kruglosutoch_view()
        self.table7 = self.create_magazin_contact_data_view()
        self.table8 = self.create_magazin_count_by_kategor_view()
    bg_color = "gray75"

    def hide_tables(self):
        self.table1.lower()
        self.table2.lower()
        self.table3.lower()
        self.table4.lower()
        self.table5.lower()
        self.table6.lower()
        self.table7.lower()
        self.table8.lower()

    def show_table(self, table):
        self.hide_tables()
        table.lift()

    def table_sort(self, column, table, table_name, sort):
        if sort:
            self.connect_cursor.execute("SELECT * from " + table_name + " ORDER BY " + column + " ASC")
        else: self.connect_cursor.execute("SELECT * from " + table_name + " ORDER BY " + column + " DESC")
        records = self.connect_cursor.fetchall()
        table.delete(*table.get_children())
        for record in records:
            table.insert("", tk.END, values=record)
        table.heading(column, command=lambda: self.table_sort(column, table, table_name, not sort))
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
        table.heading("magazin", text="Магазин", command=lambda: self.table_sort(columns[0], self.table1, "magazin", False))
        table.heading("rayon", text="Район", command=lambda: self.table_sort(columns[1], self.table1, "magazin", False))
        table.heading("kategor", text="Категория", command=lambda: self.table_sort(columns[2], self.table1, "magazin", False))
        table.heading("administrator", text="Администратор", command=lambda: self.table_sort(columns[3], self.table1, "magazin", False))
        table.heading("adress", text="Адресс", command=lambda: self.table_sort(columns[4], self.table1, "magazin", False))
        table.heading("chas_rab", text="Часы Работы", command=lambda: self.table_sort(columns[5], self.table1, "magazin", False))
        table.heading("telefon", text="Телефон", command=lambda: self.table_sort(columns[6], self.table1, "magazin", False))
        table.heading("nazv", text="Название", command=lambda: self.table_sort(columns[7], self.table1, "magazin", False))
        table.place(x=372, y=78)

        self.connect_cursor.execute("SELECT * from magazin")
        records = self.connect_cursor.fetchall()
        for record in records:
            table.insert("", tk.END, values=record)
        return table

    def create_kategor_table(self):
        columns = ("kategor", "nazv")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=300)
        table.column(column=1, width=707)
        table.heading("kategor", text="Категория", command=lambda: self.table_sort(columns[0], self.table2, "kategor", False))
        table.heading("nazv", text="Название", command=lambda: self.table_sort(columns[1], self.table2, "kategor", False))
        table.place(x=372, y=78)

        self.connect_cursor.execute("SELECT * from kategor")
        records = self.connect_cursor.fetchall()
        for record in records:
            table.insert("", tk.END, values=record)
        return table
    def create_rayon_table(self):
        columns = ("rayon", "nazv", "kolvo_mag")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=300)
        table.column(column=1, width=300)
        table.column(column=2, width=407)
        table.heading("rayon", text="Район", command=lambda: self.table_sort(columns[0], self.table3, "rayon", False))
        table.heading("nazv", text="Название", command=lambda: self.table_sort(columns[1], self.table3, "rayon", False))
        table.heading("kolvo_mag", text="Количество магазинов", command=lambda: self.table_sort(columns[2], self.table3, "rayon", False))
        table.place(x=372, y=78)

        self.connect_cursor.execute("SELECT * from rayon")
        records = self.connect_cursor.fetchall()
        for record in records:
            table.insert("", tk.END, values=record)
        return table
    def create_administrator_table(self):
        columns = ("administrator", "imya", "famil", "otch", "telefon")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=150)
        table.column(column=1, width=216)
        table.column(column=2, width=215)
        table.column(column=3, width=216)
        table.column(column=4, width=210)
        table.heading("administrator", text="Администратор", command=lambda: self.table_sort(columns[0], self.table4, "administrator", False))
        table.heading("imya", text="Имя", command=lambda: self.table_sort(columns[1], self.table4, "administrator", False))
        table.heading("famil", text="Фамилия", command=lambda: self.table_sort(columns[2], self.table4, "administrator", False))
        table.heading("otch", text="Отчество", command=lambda: self.table_sort(columns[3], self.table4, "administrator", False))
        table.heading("telefon", text="Телефон", command=lambda: self.table_sort(columns[4], self.table4, "administrator", False))
        table.place(x=372, y=78)

        self.connect_cursor.execute("SELECT * from administrator")
        records = self.connect_cursor.fetchall()
        for record in records:
            table.insert("", tk.END, values=record)
        return table
    def create_magazin_kategor_rayon_view(self):
        columns = ("Название", "Категория", "Район")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=335)
        table.column(column=1, width=335)
        table.column(column=2, width=337)
        table.heading("Название", text="Название магазина", command=lambda: self.table_sort(columns[0], self.table5, "magazin_kategor_rayon", False))
        table.heading("Категория", text="Название категории", command=lambda: self.table_sort(columns[1], self.table5, "magazin_kategor_rayon", False))
        table.heading("Район", text="Название района", command=lambda: self.table_sort(columns[2], self.table5, "magazin_kategor_rayon", False))
        table.place(x=372, y=78)

        self.connect_cursor.execute("SELECT * from magazin_kategor_rayon")
        records = self.connect_cursor.fetchall()
        for record in records:
            table.insert("", tk.END, values=record)
        return table
    def create_magazin_kruglosutoch_view(self):
        columns = ("id", "Название")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=300)
        table.column(column=1, width=707)
        table.heading("id", text="Магазин", command=lambda: self.table_sort(columns[0], self.table6, "magazin_kruglosutoch", False))
        table.heading("Название", text="Название Магазина", command=lambda: self.table_sort(columns[1], self.table6, "magazin_kruglosutoch", False))
        table.place(x=372, y=78)

        self.connect_cursor.execute("SELECT * from magazin_kruglosutoch")
        records = self.connect_cursor.fetchall()
        for record in records:
            table.insert("", tk.END, values=record)
        return table
    def create_magazin_contact_data_view(self):
        columns = ("Название", "Адрес", "ТелефонМагазина",
                   "ФИОАдминистратора", "ТелефонАдминистратора")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=150)
        table.column(column=1, width=307)
        table.column(column=2, width=150)
        table.column(column=3, width=250)
        table.column(column=4, width=150)
        table.heading("Название", text="Название Магазина", command=lambda: self.table_sort(columns[0], self.table7, "magazin_contact_data", False))
        table.heading("Адрес", text="Адрес Магазина", command=lambda: self.table_sort(columns[1], self.table7, "magazin_contact_data", False))
        table.heading("ТелефонМагазина", text="Телефон Магазина", command=lambda: self.table_sort(columns[2], self.table7, "magazin_contact_data", False))
        table.heading("ФИОАдминистратора", text="ФИО администратора", command=lambda: self.table_sort(columns[3], self.table7, "magazin_contact_data", False))
        table.heading("ТелефонАдминистратора", text="Телефон администратора", command=lambda: self.table_sort(columns[4], self.table7, "magazin_contact_data", False))
        table.place(x=372, y=78)

        self.connect_cursor.execute("SELECT * from magazin_contact_data")
        records = self.connect_cursor.fetchall()
        for record in records:
            table.insert("", tk.END, values=record)
        return table
    def create_magazin_count_by_kategor_view(self):
        columns = ("Категория", "КоличествоМагазинов")
        table = ttk.Treeview(columns=columns, show="headings", height=26)
        table.column(column=0, width=707)
        table.column(column=1, width=300)
        table.heading("Категория", text="Название категории", command=lambda: self.table_sort(columns[0], self.table8, "magazin_count_by_kategor", False))
        table.heading("КоличествоМагазинов", text="Количество магазинов", command=lambda: self.table_sort(columns[1], self.table8, "magazin_count_by_kategor", False))
        table.place(x=372, y=78)

        self.connect_cursor.execute("SELECT * from magazin_count_by_kategor")
        records = self.connect_cursor.fetchall()
        for record in records:
            table.insert("", tk.END, values=record)
        return table
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
                                 width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table(self.table1))
        kategor_button = tk.Button(text="Категории",
                                 width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table(self.table2))
        rayon_button = tk.Button(text="Районы",
                                 width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table(self.table3))
        admin_button = tk.Button(text="Администраторы",
                                 width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table(self.table4))
        magazin_button.place(x=370, y=47)
        kategor_button.place(x=625, y=47)
        rayon_button.place(x=879, y=47)
        admin_button.place(x=1134, y=47)

        view1_button = tk.Button(text="Магазин-категория-район",
                                   width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table(self.table5))
        view2_button = tk.Button(text="круглосуточные магазины",
                                   width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table(self.table6))
        view3_button = tk.Button(text="Контактные данные магазина",
                                 width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table(self.table7))
        view4_button = tk.Button(text="Кол. магазинов (категории)",
                                 width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table(self.table8))
        view1_button.place(x=370, y=624)
        view2_button.place(x=625, y=624)
        view3_button.place(x=879, y=624)
        view4_button.place(x=1134, y=624)

        ######
        self.show_table(self.table1)

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

        print(self.table1.keys())
        ######







        self.window.mainloop()