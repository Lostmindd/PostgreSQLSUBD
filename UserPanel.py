import tkinter.ttk as ttk
import tkinter as tk
from tkinter import Listbox
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
        self.search_empty = tk.Label( fg="grey6", bg=self.bg_color, width=147, height=5)
        self.block2 = tk.Label(width=250, height=47, bg=self.bg_color)
        self.buttons_list = []
    bg_color = "gray75"

    def table_search(self, table, table_name, *args):
        search_str = ""
        i = 0
        for search in args:
            if len(search.get()) > 0:
                search_str += table["column"][i] + " = " + "'" + (search.get()) + "'" + " and "
            i+=1
        if len(search_str) > 0:
            search_str = " WHERE " + search_str[:-4]
        else: search_str = ""
        self.current_columns = search_str
        self.connect_cursor.execute("SELECT * from " + table_name + search_str)
        records = self.connect_cursor.fetchall()
        table.delete(*table.get_children())
        for record in records:
            table.insert("", tk.END, values=record)

    def view_tables(self):
        pass
    def callback(self, list):
        print(list.curselection())

    def constructor_option_create(self, columns_name_list):
        magazin_columns = [tk.IntVar()] * len(columns_name_list)
        magazin_columns_opt = []
        for name in columns_name_list:
            magazin_columns_opt.append(
                tk.Checkbutton(self.window, text=name, variable=magazin_columns[columns_name_list.index(name)],
                               font=("Verdana", 9)))
        indent = 40
        for column in magazin_columns_opt:
            column.place(x=370, y=indent)
            indent += 30
    def request_constr(self):
        self.block2.lift()
        magazin = tk.IntVar()
        rayon = tk.IntVar()
        kategor = tk.IntVar()
        administrator = tk.IntVar()

        magazin_opt = tk.Checkbutton(self.window, text="Магазин", variable=magazin, font=("Verdana", 12))
        rayon_opt = tk.Checkbutton(self.window, text="Район", variable=rayon, font=("Verdana", 12))
        kategor_opt = tk.Checkbutton(self.window, text="Категория", variable=kategor, font=("Verdana", 12))
        administrator_opt = tk.Checkbutton(self.window, text="Администратор", variable=administrator, font=("Verdana", 12))

        magazin_opt.place(x=370, y=10)
        rayon_opt.place(x=635, y=10)
        kategor_opt.place(x=900, y=10)
        administrator_opt.place(x=1200, y=10)

        ###################################
        rayon_columns = [tk.IntVar()]*3
        kategor_columns = [tk.IntVar()]*2
        administrator_columns = [tk.IntVar()]*5
        magazin_columns_name = ['код_магазина', 'Район', 'Адрес', 'Часы работы', 'Телефон', 'Категория магазина',
                                'Название магазина', 'Администратор']
        self.constructor_option_create(magazin_columns_name)

        ##################################

        # block = tk.Label(width=146, height=41, bg="grey25", relief=tk.RAISED)
        # block.place(x=363, y=72)


        # OptionList = ["Таблица", "Магазин", "Категория", "Район", "Администратор"]
        # list = Listbox(self.window, selectmode="multiple")
        #
        # list.place(x=0, y=0)
        #
        # for each_item in range(len(OptionList)):
        #     list.insert(tk.END, OptionList[each_item])
        #
        #
        # search8 = tk.Button(text="Поиск",
        #                     width=6, font=("Verdana", 9),
        #                     command=lambda: self.callback(list))
        # search8.place(x=1332, y=10)
    def hide_buttons(self):
        self.search_empty.lift()

    def show_buttons(self):
        for button in self.buttons_list:
            button.lift()

    def show_table_block(self, table, *args):
        self.hide_buttons()
        for elem in args:
            elem.lift()
        table.lift()
        self.current_columns = ""
        self.show_buttons()

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

        self.search_empty.place(x=360, y=5)
        ####################################### Поиск магазина ######################################
        magazin_search1 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search2 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search3 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search4 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search5 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search6 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search7 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search8 = tk.Entry(width=14, font=("Verdana", 10))
        search1 = tk.Button(text="Поиск",
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
        search1.place(x=1332, y=10)
        ###############################################################################################
        self.hide_buttons()
        ####################################### Поиск Категории ######################################
        kategor_search1 = tk.Entry(width=14, font=("Verdana", 10))
        kategor_search2 = tk.Entry(width=14, font=("Verdana", 10))

        search2 = tk.Button(text="Поиск",
                           width=6, font=("Verdana", 9),
                           command=lambda: self.table_search(self.table2, "kategor", kategor_search1, kategor_search2))
        kategor_search_but1 = tk.Label(text="Категория", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        kategor_search_but2 = tk.Label(text="Название", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        kategor_search_but1.place(x=1090, y=30)
        kategor_search_but2.place(x=1210, y=30)
        kategor_search1.place(x=1090, y=10)
        kategor_search2.place(x=1210, y=10)
        search2.place(x=1332, y=10)
        ###############################################################################################

        ####################################### Поиск Района ######################################
        rayon_search1 = tk.Entry(width=14, font=("Verdana", 10))
        rayon_search2 = tk.Entry(width=14, font=("Verdana", 10))
        rayon_search3 = tk.Entry(width=14, font=("Verdana", 10))
        search3 = tk.Button(text="Поиск",
                            width=6, font=("Verdana", 9),
                            command=lambda: self.table_search(self.table3, "rayon", rayon_search1, rayon_search2,
                                                              rayon_search3))
        rayon_search_but1 = tk.Label(text="Район", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        rayon_search_but2 = tk.Label(text="Название", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        rayon_search_but3 = tk.Label(text="Кол-во магазинов", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        rayon_search_but1.place(x=970, y=30)
        rayon_search_but2.place(x=1090, y=30)
        rayon_search_but3.place(x=1210, y=30)
        rayon_search1.place(x=970, y=10)
        rayon_search2.place(x=1090, y=10)
        rayon_search3.place(x=1210, y=10)
        search3.place(x=1332, y=10)
        ###############################################################################################

        ####################################### Поиск Администратор ######################################
        administrator_search1 = tk.Entry(width=14, font=("Verdana", 10))
        administrator_search2 = tk.Entry(width=14, font=("Verdana", 10))
        administrator_search3 = tk.Entry(width=14, font=("Verdana", 10))
        administrator_search4 = tk.Entry(width=14, font=("Verdana", 10))
        administrator_search5 = tk.Entry(width=14, font=("Verdana", 10))
        search4 = tk.Button(text="Поиск",
                            width=6, font=("Verdana", 9),
                            command=lambda: self.table_search(self.table4, "administrator", administrator_search1,
                                                              administrator_search2, administrator_search3,
                                                              administrator_search4, administrator_search5))
        administrator_search_but1 = tk.Label(text="Администратор", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        administrator_search_but2 = tk.Label(text="Имя", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        administrator_search_but3 = tk.Label(text="Фамилия", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        administrator_search_but4 = tk.Label(text="Отчество", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        administrator_search_but5 = tk.Label(text="Телефон", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        administrator_search_but1.place(x=730, y=30)
        administrator_search_but2.place(x=850, y=30)
        administrator_search_but3.place(x=970, y=30)
        administrator_search_but4.place(x=1090, y=30)
        administrator_search_but5.place(x=1210, y=30)
        administrator_search1.place(x=730, y=10)
        administrator_search2.place(x=850, y=10)
        administrator_search3.place(x=970, y=10)
        administrator_search4.place(x=1090, y=10)
        administrator_search5.place(x=1210, y=10)
        search4.place(x=1332, y=10)
        ###############################################################################################

        ####################################### Поиск Представление 1 ######################################
        view1_search1 = tk.Entry(width=14, font=("Verdana", 10))
        view1_search2 = tk.Entry(width=14, font=("Verdana", 10))
        view1_search3 = tk.Entry(width=14, font=("Verdana", 10))
        search5 = tk.Button(text="Поиск",
                            width=6, font=("Verdana", 9),
                            command=lambda: self.table_search(self.table5, "magazin_kategor_rayon", view1_search1, view1_search2,
                                                              view1_search3))
        view1_search_but1 = tk.Label(text="Магазин", fg="grey6", bg=self.bg_color,
                                     width=14, height=1, font=("Verdana", 9))
        view1_search_but2 = tk.Label(text="Категория", fg="grey6", bg=self.bg_color,
                                     width=14, height=1, font=("Verdana", 9))
        view1_search_but3 = tk.Label(text="Район", fg="grey6", bg=self.bg_color,
                                     width=14, height=1, font=("Verdana", 9))
        view1_search_but1.place(x=970, y=30)
        view1_search_but2.place(x=1090, y=30)
        view1_search_but3.place(x=1210, y=30)
        view1_search1.place(x=970, y=10)
        view1_search2.place(x=1090, y=10)
        view1_search3.place(x=1210, y=10)
        search5.place(x=1332, y=10)
        ###############################################################################################

        ####################################### Поиск Представление 2 ######################################
        view2_search1 = tk.Entry(width=14, font=("Verdana", 10))
        view2_search2 = tk.Entry(width=14, font=("Verdana", 10))

        search6 = tk.Button(text="Поиск",
                            width=6, font=("Verdana", 9),
                            command=lambda: self.table_search(self.table6, "magazin_kruglosutoch", view2_search1, view2_search2))
        view2_search_but1 = tk.Label(text="Магазин", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        view2_search_but2 = tk.Label(text="Название магазина", fg="grey6", bg=self.bg_color,
                                       width=14, height=1, font=("Verdana", 9))
        view2_search_but1.place(x=1090, y=30)
        view2_search_but2.place(x=1210, y=30)
        view2_search1.place(x=1090, y=10)
        view2_search2.place(x=1210, y=10)
        search6.place(x=1332, y=10)
        ###############################################################################################

        ####################################### Поиск Представление 3 ######################################
        view3_search1 = tk.Entry(width=14, font=("Verdana", 10))
        view3_search2 = tk.Entry(width=14, font=("Verdana", 10))
        view3_search3 = tk.Entry(width=14, font=("Verdana", 10))
        view3_search4 = tk.Entry(width=14, font=("Verdana", 10))
        view3_search5 = tk.Entry(width=14, font=("Verdana", 10))
        search7 = tk.Button(text="Поиск",
                            width=6, font=("Verdana", 9),
                            command=lambda: self.table_search(self.table7, "magazin_contact_data", view3_search1,
                                                              view3_search2, view3_search3,
                                                              view3_search4, view3_search5))
        view3_search_but1 = tk.Label(text="Магазин", fg="grey6", bg=self.bg_color,
                                             width=14, height=1, font=("Verdana", 9))
        view3_search_but2 = tk.Label(text="Адрес", fg="grey6", bg=self.bg_color,
                                             width=14, height=1, font=("Verdana", 9))
        view3_search_but3 = tk.Label(text="Телефон", fg="grey6", bg=self.bg_color,
                                             width=14, height=1, font=("Verdana", 9))
        view3_search_but4 = tk.Label(text="ФИО Админа", fg="grey6", bg=self.bg_color,
                                             width=14, height=1, font=("Verdana", 9))
        view3_search_but5 = tk.Label(text="Телефон Админа", fg="grey6", bg=self.bg_color,
                                             width=14, height=1, font=("Verdana", 9))
        view3_search_but1.place(x=730, y=30)
        view3_search_but2.place(x=850, y=30)
        view3_search_but3.place(x=970, y=30)
        view3_search_but4.place(x=1090, y=30)
        view3_search_but5.place(x=1210, y=30)
        view3_search1.place(x=730, y=10)
        view3_search2.place(x=850, y=10)
        view3_search3.place(x=970, y=10)
        view3_search4.place(x=1090, y=10)
        view3_search5.place(x=1210, y=10)
        search7.place(x=1332, y=10)
        ###############################################################################################

        ####################################### Поиск Представление 4 ######################################
        view4_search1 = tk.Entry(width=14, font=("Verdana", 10))
        view4_search2 = tk.Entry(width=14, font=("Verdana", 10))

        search8 = tk.Button(text="Поиск",
                            width=6, font=("Verdana", 9),
                            command=lambda: self.table_search(self.table8, "magazin_count_by_kategor", view4_search1,
                                                              view4_search2))
        view4_search_but1 = tk.Label(text="Категория", fg="grey6", bg=self.bg_color,
                                     width=14, height=1, font=("Verdana", 9))
        view4_search_but2 = tk.Label(text="Кол-во магазинов", fg="grey6", bg=self.bg_color,
                                     width=14, height=1, font=("Verdana", 9))
        view4_search_but1.place(x=1090, y=30)
        view4_search_but2.place(x=1210, y=30)
        view4_search1.place(x=1090, y=10)
        view4_search2.place(x=1210, y=10)
        search8.place(x=1332, y=10)
        ###############################################################################################

        ####################################### Кнопки таблиц ######################################
        magazin_button = tk.Button(text="Магазины",
                                   width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table_block(self.table1, magazin_search1, magazin_search2,
                                                                   magazin_search3, magazin_search4, magazin_search5,
                                                                   magazin_search6, magazin_search7,
                                                                   magazin_search8, magazin_search_but1,
                                                                   magazin_search_but2, magazin_search_but3,
                                                                   magazin_search_but4, magazin_search_but5,
                                                                   magazin_search_but6, magazin_search_but7,
                                                                   magazin_search_but8, search1))
        kategor_button = tk.Button(text="Категории",
                                   width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table_block(self.table2, kategor_search1, kategor_search2,
                                                                   kategor_search_but1, kategor_search_but2, search2))
        rayon_button = tk.Button(text="Районы",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table3, rayon_search1, rayon_search2,
                                                                 rayon_search3, rayon_search_but1, rayon_search_but2,
                                                                 rayon_search_but3, search3))
        admin_button = tk.Button(text="Администраторы",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table4, administrator_search1,
                                                                 administrator_search2,
                                                                 administrator_search3, administrator_search4,
                                                                 administrator_search5, administrator_search_but1,
                                                                 administrator_search_but2, administrator_search_but3,
                                                                 administrator_search_but4,
                                                                 administrator_search_but5, search4))
        magazin_button.place(x=370, y=75)
        kategor_button.place(x=625, y=75)
        rayon_button.place(x=879, y=75)
        admin_button.place(x=1134, y=75)
        ###############################################################################################

        ####################################### Кнопки Представлений ######################################
        view1_button = tk.Button(text="Магазин-категория-район",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table5, view1_search1, view1_search2,
                                                                 view1_search3, view1_search_but1, view1_search_but2,
                                                                 view1_search_but3, search5))
        view2_button = tk.Button(text="круглосуточные магазины",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table6, view2_search1, view2_search2,
                                                                 view2_search_but1, view2_search_but2, search6))
        view3_button = tk.Button(text="Контактные данные магазина",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table7, view3_search1, view3_search2,
                                                                 view3_search3, view3_search4, view3_search5,
                                                                 view3_search_but1,
                                                                 view3_search_but2, view3_search_but3,
                                                                 view3_search_but4,
                                                                 view3_search_but5, search7))
        view4_button = tk.Button(text="Кол. магазинов (категории)",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table8, view4_search1, view4_search2,
                                                                 view4_search_but1, view4_search_but2, search8))
        view1_button.place(x=370, y=658)
        view2_button.place(x=625, y=658)
        view3_button.place(x=879, y=658)
        view4_button.place(x=1134, y=658)
        ###############################################################################################

        self.buttons_list = [magazin_button, kategor_button, rayon_button, admin_button, view1_button, view2_button, view3_button, view4_button]
        menu.place(x=56, y=20)
        table_block.place(x=363, y=72)
        self.block2.place(x=360, y=-2)
        block.place(x=0, y=0)


        ################################### Кнопки Меню ##########################################
        view_button = tk.Button(text="Просмотр таблиц", bg=self.bg_color,
                                   width=24, font=("Verdana", 14),
                                   command=lambda: self.show_table_block(self.table1, magazin_search1, magazin_search2,
                        magazin_search3, magazin_search4, magazin_search5, magazin_search6, magazin_search7,
                        magazin_search8, magazin_search_but1, magazin_search_but2, magazin_search_but3,
                        magazin_search_but4, magazin_search_but5, magazin_search_but6, magazin_search_but7,
                        magazin_search_but8, search1, table_block))

        view_button.place(x=32, y=200)

        request_constr_button = tk.Button(text="Конструктор запросов", bg=self.bg_color,
                                width=24, font=("Verdana", 14),
                                command=lambda: self.request_constr())

        request_constr_button.place(x=32, y=260)
        ###############################################################################################

        self.show_table_block(self.table1, magazin_search1, magazin_search2,
                        magazin_search3, magazin_search4, magazin_search5, magazin_search6, magazin_search7,
                        magazin_search8, magazin_search_but1, magazin_search_but2, magazin_search_but3,
                        magazin_search_but4, magazin_search_but5, magazin_search_but6, magazin_search_but7,
                        magazin_search_but8, search1)

        self.request_constr()
        self.window.mainloop()