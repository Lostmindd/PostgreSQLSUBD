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
        self.current_columns = ""
        self.button_empty = tk.Label( fg="grey6", bg=self.bg_color, width=147, height=4)
    bg_color = "gray75"

    def table_search(self, table, table_name, *args):
        search_str = ""
        i = 0
        for search in args:
            if len(search.get()) > 0:
                search_str += table["column"][i] + " = " + "'" + (search.get()) + "'" + " and "
            i+=1
        search_str = search_str[:-4]
        self.current_columns = " WHERE " + search_str
        self.connect_cursor.execute("SELECT * from " + table_name + " WHERE " + search_str)
        records = self.connect_cursor.fetchall()
        table.delete(*table.get_children())
        for record in records:
            table.insert("", tk.END, values=record)

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
        self.current_columns = ""

    def table_sort(self, column, table, table_name, sort):
        if sort:
            self.connect_cursor.execute("SELECT * from " + table_name + self.current_columns + " ORDER BY " + column + " ASC")
        else: self.connect_cursor.execute("SELECT * from " + table_name + self.current_columns + " ORDER BY " + column + " DESC")
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
        table.place(x=372, y=109)

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
        table.place(x=372, y=109)

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
        table.place(x=372, y=109)

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
        table.place(x=372, y=109)

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
        table.place(x=372, y=109)

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
        table.place(x=372, y=109)

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
        table.place(x=372, y=109)

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
        table.place(x=372, y=109)

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

        self.button_empty.place(x=360, y=5)
        ####################################### Поиск магазина ######################################
        magazin_search1 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search2 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search3 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search4 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search5 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search6 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search7 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search8 = tk.Entry(width=14, font=("Verdana", 10))
        search = tk.Button(text="Поиск",
                           width=6, font=("Verdana", 9),
                           command=lambda: self.table_search(self.table1, "magazin", magazin_search1, magazin_search2,
                            magazin_search3, magazin_search4, magazin_search5, magazin_search6, magazin_search7,
                            magazin_search8))
        magazin_search_but1 = tk.Label(text="Магазин", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        magazin_search_but2 = tk.Label(text="Район", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        magazin_search_but3 = tk.Label(text="Категория", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        magazin_search_but4 = tk.Label(text="Администратор", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        magazin_search_but5 = tk.Label(text="Адрес", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        magazin_search_but6 = tk.Label(text="Часы работы", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        magazin_search_but7 = tk.Label(text="Телефон", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        magazin_search_but8 = tk.Label(text="Название", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        magazin_search_but1.place(x=370, y=30)
        magazin_search_but2.place(x=490, y=30)
        magazin_search_but3.place(x=610, y=30)
        magazin_search_but4.place(x=730, y=30)
        magazin_search_but5.place(x=850, y=30)
        magazin_search_but6.place(x=970, y=30)
        magazin_search_but7.place(x=1090, y=30)
        magazin_search_but8.place(x=1210, y=30)
        magazin_search1.place(x=370, y=10)
        magazin_search2.place(x=490, y=10)
        magazin_search3.place(x=610, y=10)
        magazin_search4.place(x=730, y=10)
        magazin_search5.place(x=850, y=10)
        magazin_search6.place(x=970, y=10)
        magazin_search7.place(x=1090, y=10)
        magazin_search8.place(x=1210, y=10)
        search.place(x=1332, y=10)
        ###############################################################################################


        menu.place(x=62, y=20)
        table_block.place(x=363, y=72)
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
        magazin_button.place(x=370, y=75)
        kategor_button.place(x=625, y=75)
        rayon_button.place(x=879, y=75)
        admin_button.place(x=1134, y=75)

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
        view1_button.place(x=370, y=658)
        view2_button.place(x=625, y=658)
        view3_button.place(x=879, y=658)
        view4_button.place(x=1134, y=658)
        self.show_table(self.table1)


        self.window.mainloop()