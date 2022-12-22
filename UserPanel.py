import tkinter.ttk as ttk
import tkinter as tk
import psycopg2
import hashlib
import pandas as pd
import datetime
from openpyxl.workbook import Workbook

class UserPanel(object):
    def __init__(self, connect_cursor, user_level):
        self.connect_cursor = connect_cursor
        self.window = tk.Tk()
        self.user_level = user_level
        self.table1 = self.create_magazin_table()
        self.table2 = self.create_kategor_table()
        self.table3 = self.create_rayon_table()
        self.table4 = self.create_administrator_table()
        self.table5 = self.create_magazin_kategor_rayon_view()
        self.table6 = self.create_magazin_kruglosutoch_view()
        self.table7 = self.create_magazin_contact_data_view()
        self.table8 = self.create_magazin_count_by_kategor_view()
        self.search_where_condition = ""
        self.bg_color = "gray75"
        self.search_empty = tk.Label(fg="grey6", bg=self.bg_color, width=147, height=5)
        self.block2 = tk.Label(width=250, height=47, bg=self.bg_color)
        self.block3 = tk.Label(width=101, height=21, font=("Verdana", 12), bg="grey25")
        self.buttons_list = []
        self.current_search_entry = []
        self.table_block = tk.Label(width=146, height=41, bg="grey25", relief=tk.RAISED)

    def table_search(self, table, table_name, search_entry_list):
        search_str = ""
        i = 0
        for search in search_entry_list:
            if len(search.get()) > 0:
                search_str += table["column"][i] + " = " + "'" + (search.get()) + "'" + " and "
            i+=1
        if len(search_str) > 0:
            search_str = search_str[:-4]
        else: search_str = ""
        self.search_where_condition = search_str
        if search_str == "":
            quary ="SELECT * from " + table_name
        else: quary = "SELECT * from " + table_name + " WHERE " + search_str
        try:
            self.connect_cursor.execute(quary)
            records = self.connect_cursor.fetchall()
            table.delete(*table.get_children())
            for record in records:
                table.insert("", tk.END, values=record)

        except psycopg2.Error:
            self.connect_cursor.execute("ROLLBACK")

    def table_insert(self, table_name, records, table, columns=None):
        empty_records = 0
        insert_str = ""
        for record in records:
            if record.get() == "":
                empty_records+= 1
            else: insert_str += "'" + record.get() + "'" + ", "
        insert_str = insert_str[:-2]
        if empty_records == 0:
            try:
                self.connect_cursor.execute("INSERT INTO " + table_name + " VALUES ("+ insert_str +")")
                self.connect_cursor.execute("COMMIT")
                self.refresh_table(table, table_name)
            except psycopg2.Error:
                self.connect_cursor.execute("ROLLBACK")
        if empty_records == 1 and records[0].get() == "" and columns is not None:
            try:
                self.connect_cursor.execute("INSERT INTO " + table_name + " (" +", ".join(columns) +") VALUES (" + insert_str + ")")
                self.connect_cursor.execute("COMMIT")
                self.refresh_table(table, table_name)
            except psycopg2.Error:
                self.connect_cursor.execute("ROLLBACK")

    def clear_search_field(self):
        for entry in self.current_search_entry:
            entry.delete(0, 'end')

    def save_in_file(self, table, table_name):
        columns = table["columns"]
        val = []
        data_dict = {key: list(val) for key in columns}
        i = 0
        for line in table.get_children():
            for value in table.item(line)['values']:
                current_column = columns[i]
                data_dict[current_column].append(value)
                i += 1
            i = 0
        output_file = pd.DataFrame(data_dict)
        now = datetime.datetime.now()
        filename = table_name + "_" + str(now.day) + "_" + str(now.month)+ "_" + str(now.year)+ "T" + str(now.hour)+ "_" + str(now.minute)+ "_" + str(now.second)
        output_file.to_excel('./'+ filename +'.xlsx', sheet_name=table_name)

    def block_show(self, block, button, hide, entry = None):
        if hide:
            block.lower()
            if entry != None:
                entry.delete(0, 'end')
        else:
            block.lift()
            if entry != None:
                entry.delete(0, 'end')
                entry.insert(0, "none")
        button['command'] = lambda: self.block_show(block, button, not hide, entry)

    def refresh_table(self, table, table_name):
        self.connect_cursor.execute("SELECT * from " + table_name)
        records = self.connect_cursor.fetchall()
        table.delete(*table.get_children())
        for record in records:
            table.insert("", tk.END, values=record)

    def constructor_table_columns(self, columns, entry, table_name):
        selected_columns = []
        for i in range(len(columns)):
            if entry[i].get() != 'none':
                selected_columns.append(table_name + "_" + columns[i])
        return selected_columns

    def create_select_line(self, columns, entry, table_name):
        select_str = ""
        for i in range(len(columns)):
            if entry[i].get() != 'none':
                select_str += table_name + "." + columns[i] + ", "
        return select_str

    def create_where_line(self, columns, entry, table_name):
        select_str = ""
        for i in range(len(columns)):
            if entry[i].get() != 'none' and entry[i].get() != '':
                select_str += table_name + "." + columns[i] + " " + entry[i].get() + " and  "
        return select_str

    def form_request(self, magazin_entry, rayon_entry, kategor_entry, admin_entry):
        magazin_columns_name = ["rayon", "adress", "chas_rab", "telefon", "kategor", "nazv", "administrator"]
        rayon_columns_name = ["nazv", "kolvo_mag"]
        kategor_columns_name = ["nazv"]
        admin_columns_name = ["famil", "imya", "otch", "telefon"]

        magazin_select_line = self.create_select_line(magazin_columns_name, magazin_entry, 'magazin')
        rayon_select_line = self.create_select_line(rayon_columns_name, rayon_entry, 'rayon')
        kategor_select_line = self.create_select_line(kategor_columns_name, kategor_entry, ' kategor')
        admin_select_line = self.create_select_line(admin_columns_name, admin_entry, 'administrator')
        query_select_part = (magazin_select_line + rayon_select_line + kategor_select_line + admin_select_line)[:-2]
        query_from_part = "magazin "
        if rayon_select_line != "":
            query_from_part += " LEFT JOIN rayon on magazin.rayon = rayon.rayon "
        if kategor_select_line != "":
            query_from_part += " LEFT JOIN kategor on magazin.kategor = kategor.kategor "
        if admin_select_line != "":
            query_from_part += " LEFT JOIN administrator on magazin.administrator = administrator.administrator "
        query_where_part = ( self.create_where_line(magazin_columns_name, magazin_entry, 'magazin') +
                      self.create_where_line(rayon_columns_name, rayon_entry, 'rayon') +
                      self.create_where_line(kategor_columns_name, kategor_entry, ' kategor') +
                      self.create_where_line(admin_columns_name, admin_entry, 'administrator'))[:-6]

        columns = (self.constructor_table_columns(magazin_columns_name, magazin_entry, 'magazin') +
        self.constructor_table_columns(rayon_columns_name, rayon_entry, 'rayon') +
        self.constructor_table_columns(kategor_columns_name, kategor_entry, 'kategor') +
        self.constructor_table_columns(admin_columns_name, admin_entry, 'administrator'))

        self.create_constructor_query_table(query_select_part, query_from_part, query_where_part, columns)

    def constructor_columns_entry_create(self, count, x, but_indent=80):
        entry_indent = 170
        but_indent += 3
        magazin_entry = []
        for i in range(count):
            magazin_entry.append(tk.Entry(width=14, font=("Verdana", 9)))
            magazin_entry[i].insert(0, "none")
        for entry in magazin_entry:
            entry.place(x=x+entry_indent, y=but_indent)
            but_indent += 26
        return magazin_entry

    def create_constructor_query_table(self, query_select_part=None, query_from_part=None, query_where_part=None, columns=None, custom_query=None):
        names_on_rus = {'magazin_rayon': 'Район', 'magazin_adress': 'Адрес', 'magazin_chas_rab': 'Часы Работы', 'magazin_telefon': 'Телефон маг.', 'magazin_kategor': 'Категория',
                        'magazin_nazv': 'Название маг.', 'magazin_administrator': 'Администратор', 'rayon_nazv': 'Название район', 'rayon_kolvo_mag': 'Кол. магазин', 'kategor_nazv': 'Категория',
                        'administrator_famil': 'Фамилия', 'administrator_imya': 'Имя', 'administrator_otch': 'Отчество', 'administrator_telefon': 'Телефон адм.'}
        if custom_query is None:
            if query_select_part == "":
                return
            else:
                query = "SELECT " + query_select_part + " FROM " + query_from_part
            if query_where_part != "":
                query += " WHERE " + query_where_part
        else: query = custom_query
        try:
            self.connect_cursor.execute(query)
            records = self.connect_cursor.fetchall()
        except psycopg2.Error:
            self.connect_cursor.execute("ROLLBACK")
            return
        columns_was_none = False
        if columns is None:
            columns_was_none = True
            columns = []
            for i in range(len(self.connect_cursor.description)):
                columns.append(self.connect_cursor.description[i][0])
        table = ttk.Treeview(columns=columns, show="headings", height=17)
        save = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.save_in_file(table, "custom_request"))
        save.place(x=372, y=292)
        if len(columns) == 0: column_size = 125
        else: column_size = int(1007 / len(columns))
        for i in range(len(columns)):
            table.column(column=i, width=column_size)

        if columns_was_none:
            for column in columns:
                table.heading(column, text=column)
        else:
            for column in columns:
                table.heading(column, text=names_on_rus[column])
        table.place(x=372, y=315)

        for record in records:
            table.insert("", tk.END, values=record)

    def constructor_columns_buttons_create(self, columns_name_list, x, but_indent=80):
        entry_indent = 170
        but_indent += 3
        magazin_blocks = []
        magazin_plus = []
        notice = tk.Label(text='столбец               условие отбора', fg="blue", bg=self.bg_color, width=40, height=1,
                           font=("Verdana", 10))
        notice.place(x=x, y=but_indent-30)
        for i in range(len(columns_name_list)):
            magazin_plus.append(tk.Label(text='+', fg="blue", bg=self.bg_color, width=1, height=1, font=("Verdana", 12)))
            magazin_blocks.append(tk.Label(bg=self.bg_color, width=18, height=1, font=("Verdana", 9)))
        for block in magazin_blocks:
            block.place(x=x+entry_indent - 30, y=but_indent)
            but_indent += 26
        but_indent -= (26 * len(columns_name_list)) + 4
        for plus in magazin_plus:
            plus.place(x=x + entry_indent - 30, y=but_indent)
            but_indent += 26
        return magazin_blocks

    def request_constructor(self):
        self.block2.lift()
        table_block = tk.Label(width=146, height=26, bg="grey25", relief=tk.RAISED)
        table_block.place(x=363, y=300)
        magazin_but = tk.Button(text='Магазин', width=25, font=("Verdana", 13))
        rayon_but = tk.Button(text='Район', width=25, font=("Verdana", 13))
        kategor_but = tk.Button(text='Категория', width=25, font=("Verdana", 13))
        administrator_but = tk.Button(text='Администратор', width=25, font=("Verdana", 13))

        magazin_but.place(x=370, y=10)
        rayon_but.place(x=720, y=10)
        kategor_but.place(x=720, y=166)
        administrator_but.place(x=1050, y=10)

        constructor_search = tk.Button(text='Поиск', width=25, font=("Verdana", 13),
                                       command=lambda: self.form_request(magazin_entry, rayon_entry, kategor_entry, admin_entry))
        constructor_search.place(x=1050, y=250)
        ###################################

        x_indent = 370
        y_indent = 80
        magazin_entry = self.constructor_columns_entry_create(7, x_indent)
        magazin_blocks = self.constructor_columns_buttons_create(['Район', 'Адрес', 'Часы работы', 'Телефон', 'Категория магазина',
                                        'Название магазина', 'Администратор'], x_indent)
        b1 = tk.Button(text='Район', width=16, font=("Verdana", 9), command=lambda: self.block_show(magazin_blocks[0], b1, True, magazin_entry[0]))
        b2 = tk.Button(text='Адрес', width=16, font=("Verdana", 9), command=lambda: self.block_show(magazin_blocks[1], b2, True, magazin_entry[1]))
        b3 = tk.Button(text='Часы работы', width=16, font=("Verdana", 9), command=lambda: self.block_show(magazin_blocks[2], b3, True, magazin_entry[2]))
        b4 = tk.Button(text='Телефон', width=16, font=("Verdana", 9), command=lambda: self.block_show(magazin_blocks[3], b4, True, magazin_entry[3]))
        b5 = tk.Button(text='Категория магазина', width=16, font=("Verdana", 9), command=lambda: self.block_show(magazin_blocks[4], b5, True, magazin_entry[4]))
        b6 = tk.Button(text='Название магазина', width=16, font=("Verdana", 9), command=lambda: self.block_show(magazin_blocks[5], b6, True, magazin_entry[5]))
        b7 = tk.Button(text='Администратор', width=16, font=("Verdana", 9), command=lambda: self.block_show(magazin_blocks[6], b7, True, magazin_entry[6]))
        for button in [b1, b2, b3, b4, b5, b6, b7]:
            button.place(x=x_indent, y=y_indent)
            y_indent += 26
        ############
        x_indent = 720
        y_indent = 80
        rayon_entry = self.constructor_columns_entry_create(2, x_indent)
        rayon_blocks = self.constructor_columns_buttons_create(
            ['Название района', 'Кол. магазинов'], x_indent)
        b8 = tk.Button(text='Название района', width=16, font=("Verdana", 9),
                       command=lambda: self.block_show(rayon_blocks[0], b8, True, rayon_entry[0]))
        b9 = tk.Button(text='Кол. магазинов', width=16, font=("Verdana", 9),
                       command=lambda: self.block_show(rayon_blocks[1], b9, True, rayon_entry[1]))
        for button in [b8, b9]:
            button.place(x=x_indent, y=y_indent)
            y_indent += 26
        kategor_entry = self.constructor_columns_entry_create(1, x_indent, 236)
        kategor_blocks = self.constructor_columns_buttons_create(
            ['Название'], x_indent, 236)
        b10 = tk.Button(text='Название района', width=16, font=("Verdana", 9),
                       command=lambda: self.block_show(kategor_blocks[0], b10, True, kategor_entry[0]))
        b10.place(x=x_indent, y=236)
        y_indent += 26
        ############
        x_indent = 1050
        y_indent = 80
        admin_entry = self.constructor_columns_entry_create(4, x_indent)
        admin_blocks = self.constructor_columns_buttons_create(
            ['Фамилия', 'Имя', 'Отчество', 'Телефон'], x_indent)
        b11 = tk.Button(text='Фамилия', width=16, font=("Verdana", 9),
                       command=lambda: self.block_show(admin_blocks[0], b11, True, admin_entry[0]))
        b12 = tk.Button(text='Имя', width=16, font=("Verdana", 9),
                       command=lambda: self.block_show(admin_blocks[1], b12, True, admin_entry[1]))
        b13 = tk.Button(text='Отчество', width=16, font=("Verdana", 9),
                       command=lambda: self.block_show(admin_blocks[2], b13, True, admin_entry[2]))
        b14 = tk.Button(text='Телефон', width=16, font=("Verdana", 9),
                       command=lambda: self.block_show(admin_blocks[3], b14, True, admin_entry[3]))
        for button in [b11, b12, b13, b14]:
            button.place(x=x_indent, y=y_indent)
            y_indent += 26
        ##################################

    def custom_request(self, query):
        self.block3.lift()
        if query.find('auth') != -1 and self.user_level < 4: return
        try:
            self.connect_cursor.execute(query)
            server_answer = tk.Label(text=self.connect_cursor.statusmessage, width=70, height=5, font=("Verdana", 12),
                                     bg="white", relief=tk.RAISED, anchor=tk.NW)
            server_answer.place(x=372, y=212)
            self.create_constructor_query_table(None, None, None, None, query)
            self.connect_cursor.execute("COMMIT")
        except psycopg2.Error as error:
            server_answer = tk.Label(text=error.pgcode + error.pgerror, width=70, height=5, font=("Verdana", 12), bg="white", fg="red2", relief=tk.RAISED, anchor=tk.NW)
            server_answer.place(x=372, y=212)
            self.connect_cursor.execute("ROLLBACK")

    def custom_request_button(self):
        self.block2.lift()
        request_field_border = tk.Label(width=101, height=38, font=("Verdana", 12), bg="grey25")
        request_field_border.place(x=367, y=8)
        request_field = tk.Text(width=100, height=10, font=("Verdana", 12))
        request_field.place(x=372, y=20)
        execute_button = tk.Button(text="Запустить",
                                 width=16, height=2, font=("Verdana", 20),
                                 command=lambda: self.custom_request(request_field.get(1.0, tk.END)))
        server_answer_empty = tk.Label(width=70, height=5, font=("Verdana", 12), bg="white", relief=tk.RAISED)
        server_answer_empty.place(x=372, y=212)
        table_empty = tk.Label(width=100, height=20, font=("Verdana", 12), bg="white", relief=tk.RAISED)
        table_empty.place(x=372, y=315)
        execute_button.place(x=1093, y=215)

    def create_account(self, entry, errmsg):
        errmsg.set("")
        empty_entry = 0
        for data in entry:
            if data.get() == "":
                empty_entry += 1
        if empty_entry > 0:
            errmsg.set("Нужно заполнить все поля")
            return
        if int(entry[2].get()) >= self.user_level:
            errmsg.set("У вас недостаточно прав для создания этого уровня привилегий")
            return

        try:
            hash_pass = hashlib.sha1(entry[1].get().encode('utf-8'))
            self.connect_cursor.execute("INSERT INTO auth VALUES ( '" + entry[0].get() + "', '" + hash_pass.hexdigest() + "', '" + entry[2].get() + "') ")
            self.connect_cursor.execute("COMMIT")
        except psycopg2.Error:
            self.connect_cursor.execute("ROLLBACK")

    def create_account_button(self):
        self.block2.lift()
        border = tk.Label(width=40, height=30, font=("Verdana", 12), bg="grey25")
        border.place(x=660, y=80)
        main_block = tk.Label(width=38, height=28, font=("Verdana", 12), bg="grey38")
        main_block.place(x=670, y=96)
        notice = tk.Label(
            text="Данные",
            fg="white", bg="grey38",
            width=10, height=2,
            justify=tk.CENTER,
            font=("Verdana", 38)
        )
        login_note = tk.Label(
            text="Логин:",
            fg="white", bg="grey38",
            width=10, height=2,
            justify=tk.CENTER,
            font=("Verdana", 16)
        )
        pass_note = tk.Label(
            text="Пароль:",
            fg="white", bg="grey38",
            width=10, height=2,
            justify=tk.CENTER,
            font=("Verdana", 16)
        )
        level_note = tk.Label(
            text="Уровень доступа:",
            fg="white", bg="grey38",
            width=17, height=2,
            justify=tk.CENTER,
            font=("Verdana", 16)
        )
        login = tk.Entry(width=26, font=("Verdana", 15))
        password = tk.Entry(width=26, font=("Verdana", 15), show="*")
        level = tk.Entry(width=1, font=("Verdana", 15))
        errmsg = tk.StringVar()
        create_button = tk.Button(text="Создать",
                                 width=8, font=("Verdana", 16),
                                 command= lambda: self.create_account([login, password, level], errmsg))

        error_note = tk.Label(foreground="red", textvariable=errmsg, wraplength=250,
                              bg="grey38", font=("Verdana", 12))

        notice.place(x=695, y=100)
        login_note.place(x=790, y=250)
        login.place(x=693, y=300)
        pass_note.place(x=790, y=320)
        password.place(x=693, y=370)
        level_note.place(x=730, y=405)
        level.place(x=950, y=420)
        create_button.place(x=800, y=500)
        error_note.place(x=740, y=540)

    def hide_buttons(self):
        self.search_empty.lift()

    def show_buttons(self):
        for button in self.buttons_list:
            button.lift()

    def show_table_block(self, table, table_name, search_entry, *args):
        self.block2.lift()
        self.table_block.lift()
        self.current_search_entry = search_entry
        self.hide_buttons()
        for elem in args:
            if elem is not None:
                elem.lift()
        for elem in search_entry:
            if elem is not None:
                elem.lift()
        table.lift()
        self.refresh_table(table, table_name)
        self.clear_search_field()
        self.search_where_condition = ""
        self.show_buttons()

    def table_sort(self, column, table, sort, table_name, select_columns='*', where_statement=''):
        quary = ''
        if where_statement == '' and self.search_where_condition == '':
            quary = "SELECT " + select_columns + " from " + table_name
        elif where_statement == '':
            where_statement = self.search_where_condition
            quary = "SELECT " + select_columns + " from " + table_name + " where " + where_statement
        if sort:
            self.connect_cursor.execute(quary + " ORDER BY " + column + " ASC")
        else: self.connect_cursor.execute(quary + " ORDER BY " + column + " DESC")
        records = self.connect_cursor.fetchall()
        table.delete(*table.get_children())
        for record in records:
            table.insert("", tk.END, values=record)
        table.heading(column, command=lambda: self.table_sort(column, table, not sort, table_name))
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
        table.heading("magazin", text="Магазин", command=lambda: self.table_sort(columns[0], self.table1, False,
                                                                                 "magazin"))
        table.heading("rayon", text="Район", command=lambda: self.table_sort(columns[1], self.table1, False, "magazin"))
        table.heading("kategor", text="Категория", command=lambda: self.table_sort(columns[2], self.table1, False,
                                                                                   "magazin"))
        table.heading("administrator", text="Администратор", command=lambda: self.table_sort(columns[3], self.table1,
                                                                                             False, "magazin"))
        table.heading("adress", text="Адрес", command=lambda: self.table_sort(columns[4], self.table1, False,
                                                                               "magazin"))
        table.heading("chas_rab", text="Часы Работы", command=lambda: self.table_sort(columns[5], self.table1, False,
                                                                                      "magazin"))
        table.heading("telefon", text="Телефон", command=lambda: self.table_sort(columns[6], self.table1, False,
                                                                                 "magazin"))
        table.heading("nazv", text="Название", command=lambda: self.table_sort(columns[7], self.table1, False,
                                                                               "magazin"))
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
        table.heading("kategor", text="Категория", command=lambda: self.table_sort(columns[0], self.table2, False,
                                                                                   "kategor"))
        table.heading("nazv", text="Название", command=lambda: self.table_sort(columns[1], self.table2, False,
                                                                               "kategor"))
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
        table.heading("rayon", text="Район", command=lambda: self.table_sort(columns[0], self.table3, False, "rayon"))
        table.heading("nazv", text="Название", command=lambda: self.table_sort(columns[1], self.table3, False, "rayon"))
        table.heading("kolvo_mag", text="Количество магазинов", command=lambda: self.table_sort(columns[2], self.table3,
                                                                                                False, "rayon"))
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
        table.heading("administrator", text="Администратор", command=lambda: self.table_sort(columns[0], self.table4,
                                                                                             False, "administrator"))
        table.heading("imya", text="Имя", command=lambda: self.table_sort(columns[1], self.table4, False,
                                                                          "administrator"))
        table.heading("famil", text="Фамилия", command=lambda: self.table_sort(columns[2], self.table4, False,
                                                                               "administrator"))
        table.heading("otch", text="Отчество", command=lambda: self.table_sort(columns[3], self.table4, False,
                                                                               "administrator"))
        table.heading("telefon", text="Телефон", command=lambda: self.table_sort(columns[4], self.table4, False,
                                                                                 "administrator"))
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
        table.heading("Название", text="Название магазина", command=lambda: self.table_sort(columns[0], self.table5,
                                                                                            False,
                                                                                            "magazin_kategor_rayon"))
        table.heading("Категория", text="Название категории", command=lambda: self.table_sort(columns[1], self.table5,
                                                                                              False,
                                                                                              "magazin_kategor_rayon"))
        table.heading("Район", text="Название района", command=lambda: self.table_sort(columns[2], self.table5, False,
                                                                                       "magazin_kategor_rayon"))
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
        table.heading("id", text="Магазин", command=lambda: self.table_sort(columns[0], self.table6, False,
                                                                            "magazin_kruglosutoch"))
        table.heading("Название", text="Название Магазина", command=lambda: self.table_sort(columns[1], self.table6,
                                                                                            False,
                                                                                            "magazin_kruglosutoch"))
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
        table.heading("Название", text="Название Магазина", command=lambda: self.table_sort(columns[0], self.table7,
                                                                                            False,
                                                                                            "magazin_contact_data"))
        table.heading("Адрес", text="Адрес Магазина", command=lambda: self.table_sort(columns[1], self.table7, False,
                                                                                      "magazin_contact_data"))
        table.heading("ТелефонМагазина", text="Телефон Магазина", command=lambda: self.table_sort(columns[2],
                                                                                                  self.table7, False,
                                                                                                  "magazin_contact_data"))
        table.heading("ФИОАдминистратора", text="ФИО администратора", command=lambda: self.table_sort(columns[3],
                                                                                                      self.table7,
                                                                                                      False,
                                                                                                      "magazin_contact_data"))
        table.heading("ТелефонАдминистратора", text="Телефон администратора", command=lambda: self.table_sort(
            columns[4], self.table7, False, "magazin_contact_data"))
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
        table.heading("Категория", text="Название категории", command=lambda: self.table_sort(columns[0], self.table8,
                                                                                              False,
                                                                                              "magazin_count_by_kategor"))
        table.heading("КоличествоМагазинов", text="Количество магазинов", command=lambda: self.table_sort(columns[1],
                                                                                                          self.table8,
                                                                                                          False,
                                                                                                          "magazin_count_by_kategor"))
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
        menu = tk.Label(
            text="Меню",
            fg="grey6", bg="grey38",
            width=5, height=1,
            font=("Arial Black", 50)  # Franklin Gothic
        )
        if self.user_level == 0:
            insert1 = None
            insert2 = None
            insert3 = None
            insert4 = None
        self.search_empty.place(x=360, y=-8)
        ####################################### Поиск магазина ######################################
        magazin_search1 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search2 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search3 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search4 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search5 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search6 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search7 = tk.Entry(width=14, font=("Verdana", 10))
        magazin_search8 = tk.Entry(width=14, font=("Verdana", 10))
        entry_list = [magazin_search1, magazin_search2, magazin_search3, magazin_search4, magazin_search5,
                                                                  magazin_search6, magazin_search7, magazin_search8]
        search1 = tk.Button(text="Поиск",
                           width=6, font=("Verdana", 9),
                           command=lambda: self.table_search(self.table1, "magazin", entry_list))
        if self.user_level > 0:
            insert1 = tk.Button(text="Вставка", width=10, font=("Verdana", 8), bg="light goldenrod",
                                command=lambda: self.table_insert("magazin", entry_list, self.table1,
                                ["rayon", "kategor", "administrator", "adress", "chas_rab", "telefon", "nazv"]))
            insert1.place(x=1311, y=50)

        clear1 = tk.Button(text="Очистка", width=10, font=("Verdana", 8), bg="light steel blue",
                           command=lambda: self.clear_search_field())
        clear1.place(x=364, y=50)
        save1 = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                           command=lambda: self.save_in_file(self.table1, "magazin"))
        save1.place(x=454, y=50)
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
        entry_list2 = [kategor_search1, kategor_search2]
        search2 = tk.Button(text="Поиск",
                           width=6, font=("Verdana", 9),
                           command=lambda: self.table_search(self.table2, "kategor", entry_list2))
        if self.user_level > 0:
            insert2 = tk.Button(text="Вставка", width=10, font=("Verdana", 8), bg="light goldenrod",
                                command=lambda: self.table_insert("kategor", entry_list2, self.table2, ["nazv"]))
            insert2.place(x=1311, y=50)
        clear2= tk.Button(text="Очистка", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.clear_search_field())
        clear2.place(x=364, y=50)
        save2 = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.save_in_file(self.table2, "kategor"))
        save2.place(x=454, y=50)
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
        entry_list3 = [rayon_search1, rayon_search2, rayon_search3]
        search3 = tk.Button(text="Поиск",
                            width=6, font=("Verdana", 9),
                            command=lambda: self.table_search(self.table3, "rayon", entry_list3))
        if self.user_level > 0:
            insert3 = tk.Button(text="Вставка", width=10, font=("Verdana", 8), bg="light goldenrod",
                                command=lambda: self.table_insert("rayon", entry_list3, self.table3,
                                                                  ["nazv", "kolvo_mag"]))
            insert3.place(x=1311, y=50)
        clear3 = tk.Button(text="Очистка", width=10, font=("Verdana", 8), bg="light steel blue",
                           command=lambda: self.clear_search_field())
        clear3.place(x=364, y=50)
        save3 = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.save_in_file(self.table3, "rayon"))
        save3.place(x=454, y=50)
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
        entry_list4 = [administrator_search1, administrator_search2, administrator_search3, administrator_search4,
                       administrator_search5]
        search4 = tk.Button(text="Поиск",
                            width=6, font=("Verdana", 9),
                            command=lambda: self.table_search(self.table4, "administrator", entry_list4))
        if self.user_level > 0:
            insert4 = tk.Button(text="Вставка", width=10, font=("Verdana", 8), bg="light goldenrod",
                                command=lambda: self.table_insert("administrator", entry_list4, self.table4,
                                                                  ["imya", "famil", "otch", "telefon"]))
            insert4.place(x=1311, y=50)
        clear4 = tk.Button(text="Очистка", width=10, font=("Verdana", 8), bg="light steel blue",
                           command=lambda: self.clear_search_field())
        clear4.place(x=364, y=50)
        save4 = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.save_in_file(self.table4, "administrator"))
        save4.place(x=454, y=50)
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
                            command=lambda: self.table_search(self.table5, "magazin_kategor_rayon", [view1_search1, view1_search2,
                                                              view1_search3]))
        save5 = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.save_in_file(self.table5, "magazin_kategor_rayon"))
        save5.place(x=364, y=50)
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
                            command=lambda: self.table_search(self.table6, "magazin_kruglosutoch", [view2_search1, view2_search2]))
        save6 = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.save_in_file(self.table6, "magazin_kruglosutoch"))
        save6.place(x=364, y=50)
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
                            command=lambda: self.table_search(self.table7, "magazin_contact_data", [view3_search1,
                                                              view3_search2, view3_search3,
                                                              view3_search4, view3_search5]))
        save7 = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.save_in_file(self.table7, "magazin_contact_data"))
        save7.place(x=364, y=50)
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
                            command=lambda: self.table_search(self.table8, "magazin_count_by_kategor", [view4_search1,
                                                              view4_search2]))
        save8 = tk.Button(text="Сохранить", width=10, font=("Verdana", 8), bg="light steel blue",
                          command=lambda: self.save_in_file(self.table8, "magazin_count_by_kategor"))
        save8.place(x=364, y=50)
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
                                   command=lambda: self.show_table_block(self.table1, 'magazin', [magazin_search1, magazin_search2,
                                                                   magazin_search3, magazin_search4, magazin_search5,
                                                                   magazin_search6, magazin_search7,
                                                                   magazin_search8], magazin_search_but1,
                                                                   magazin_search_but2, magazin_search_but3,
                                                                   magazin_search_but4, magazin_search_but5,
                                                                   magazin_search_but6, magazin_search_but7,
                                                                   magazin_search_but8, search1, insert1, clear1, save1))
        kategor_button = tk.Button(text="Категории",
                                   width=24, font=("Verdana", 12),
                                   command=lambda: self.show_table_block(self.table2, 'kategor', [kategor_search1, kategor_search2],
                                                                   kategor_search_but1, kategor_search_but2, search2, insert2, clear2, save2))
        rayon_button = tk.Button(text="Районы",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table3, 'rayon', [rayon_search1, rayon_search2,
                                                                 rayon_search3], rayon_search_but1, rayon_search_but2,
                                                                 rayon_search_but3, search3, insert3, clear3, save3))
        admin_button = tk.Button(text="Администраторы",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table4, 'administrator', [administrator_search1,
                                                                 administrator_search2,
                                                                 administrator_search3, administrator_search4,
                                                                 administrator_search5], administrator_search_but1,
                                                                 administrator_search_but2, administrator_search_but3,
                                                                 administrator_search_but4,
                                                                 administrator_search_but5, search4, insert4, clear4, save4))
        magazin_button.place(x=370, y=75)
        kategor_button.place(x=625, y=75)
        rayon_button.place(x=879, y=75)
        admin_button.place(x=1134, y=75)
        ###############################################################################################

        ####################################### Кнопки Представлений ######################################
        view1_button = tk.Button(text="Магазин-категория-район",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table5, 'magazin_kategor_rayon', [view1_search1, view1_search2,
                                                                 view1_search3], view1_search_but1, view1_search_but2,
                                                                 view1_search_but3, search5, save5))
        view2_button = tk.Button(text="круглосуточные магазины",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table6, 'magazin_kruglosutoch', [view2_search1, view2_search2],
                                                                 view2_search_but1, view2_search_but2, search6, save6))
        view3_button = tk.Button(text="Контактные данные магазина",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table7, 'magazin_contact_data', [view3_search1, view3_search2,
                                                                 view3_search3, view3_search4, view3_search5],
                                                                 view3_search_but1,
                                                                 view3_search_but2, view3_search_but3,
                                                                 view3_search_but4,
                                                                 view3_search_but5, search7, save7))
        view4_button = tk.Button(text="Кол. магазинов (категории)",
                                 width=24, font=("Verdana", 12),
                                 command=lambda: self.show_table_block(self.table8, 'magazin_count_by_kategor', [view4_search1, view4_search2],
                                                                 view4_search_but1, view4_search_but2, search8, save8))
        view1_button.place(x=370, y=658)
        view2_button.place(x=625, y=658)
        view3_button.place(x=879, y=658)
        view4_button.place(x=1134, y=658)
        ###############################################################################################

        self.buttons_list = [magazin_button, kategor_button, rayon_button, admin_button, view1_button, view2_button, view3_button, view4_button]
        menu.place(x=56, y=20)
        self.table_block.place(x=363, y=72)
        self.block2.place(x=360, y=-2)
        self.block3.place(x=367, y=314)
        block.place(x=0, y=0)


        ################################### Кнопки Меню ##########################################
        view_button = tk.Button(text="Просмотр таблиц", bg=self.bg_color,
                                   width=24, font=("Verdana", 14),
                                   command=lambda: self.show_table_block(self.table1, 'magazin', [magazin_search1, magazin_search2,
                        magazin_search3, magazin_search4, magazin_search5, magazin_search6, magazin_search7,
                        magazin_search8], magazin_search_but1, magazin_search_but2, magazin_search_but3,
                        magazin_search_but4, magazin_search_but5, magazin_search_but6, magazin_search_but7,
                        magazin_search_but8, search1, insert1, clear1, save1))
        view_button.place(x=32, y=200)

        request_constr_button = tk.Button(text="Конструктор запросов", bg=self.bg_color,
                                          width=24, font=("Verdana", 14),
                                          command=lambda: self.request_constructor())

        request_constr_button.place(x=32, y=260)
        if self.user_level > 0:
            request_handle_button = tk.Button(text="Ручной запрос", bg=self.bg_color,
                                              width=24, font=("Verdana", 14),
                                              command=lambda: self.custom_request_button())
            request_handle_button.place(x=32, y=400)
        if self.user_level > 1:
            request_handle_button = tk.Button(text="Создать аккаунт", bg=self.bg_color,
                                              width=24, font=("Verdana", 14),
                                              command=lambda: self.create_account_button())
            request_handle_button.place(x=32, y=460)
        ###############################################################################################

        self.show_table_block(self.table1, 'magazin', [magazin_search1, magazin_search2,
                        magazin_search3, magazin_search4, magazin_search5, magazin_search6, magazin_search7,
                        magazin_search8], magazin_search_but1, magazin_search_but2, magazin_search_but3,
                        magazin_search_but4, magazin_search_but5, magazin_search_but6, magazin_search_but7,
                        magazin_search_but8, search1, insert1, clear1, save1)
        self.window.mainloop()





