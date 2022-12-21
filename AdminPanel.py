import tkinter as tk
import UserPanel
import psycopg2

class AdminPanel(UserPanel.UserPanel):
    def __init__(self, connect_cursor, user_level):
        super().__init__(connect_cursor, user_level)
        self.table1.bind('<<TreeviewSelect>>', self.edit_table1)
        self.table2.bind('<<TreeviewSelect>>', self.edit_table2)
        self.table3.bind('<<TreeviewSelect>>', self.edit_table3)
        self.table4.bind('<<TreeviewSelect>>', self.edit_table4)



    def delete_record(self, table_name, table):
        row = table.item(table.selection())
        try:
            self.connect_cursor.execute("DELETE FROM " + table_name + " WHERE " + table_name + " = " + str(row['values'][0]))
            self.connect_cursor.execute("COMMIT")
            self.refresh_table(table, table_name)
        except psycopg2.Error:
            self.connect_cursor.execute("ROLLBACK")

    def fill_search_entry(self, table):
        self.clear_search_field()
        row = table.item(table.selection())
        for i in range(len(self.current_search_entry)):
            self.current_search_entry[i].insert(0, row['values'][i])

    def get_search_entry(self):
        search_entry_list = []
        for i in range(len(self.current_search_entry)):
            search_entry_list.append(self.current_search_entry[i].get())
        return search_entry_list

    def table_update(self, table_name, table, columns):
        search_str = ""
        row = table.item(table.selection())
        key_column = row['values'][0]
        records = self.get_search_entry()
        for i in range(len(records)):
            if records[i] != '':
                search_str += columns[i] + " = '" + records[i] + "', "
        search_str = search_str[:-2]
        if search_str != '':
            try:
                self.connect_cursor.execute("UPDATE " + table_name + " SET " + search_str + " WHERE " + table_name + " = " + str(key_column))
                self.connect_cursor.execute("COMMIT")
                self.refresh_table(table, table_name)
                self.clear_search_field()
            except psycopg2.Error:
                self.connect_cursor.execute("ROLLBACK")

    def edit_table1(self, event):
        self.fill_search_entry(self.table1)
        redact = tk.Button(text="Редакт", width=10, font=("Verdana", 8), bg="DarkOliveGreen1",
                           command=lambda: self.table_update('magazin', self.table1, ["magazin", "rayon", "kategor", "administrator", "adress", "chas_rab", "telefon", "nazv"]))
        redact.place(x=1131, y=50)
        delete = tk.Button(text="Удален", width=10, font=("Verdana", 8), bg="firebrick1",
                           command=lambda: self.delete_record('magazin', self.table1))
        delete.place(x=1221, y=50)

    def edit_table2(self, event):
        self.fill_search_entry(self.table2)
        redact = tk.Button(text="Редакт", width=10, font=("Verdana", 8), bg="DarkOliveGreen1",
                           command=lambda: self.table_update('kategor', self.table2, ["kategor", "nazv"]))
        redact.place(x=1131, y=50)
        delete = tk.Button(text="Удален", width=10, font=("Verdana", 8), bg="firebrick1",
                           command=lambda: self.delete_record('kategor', self.table2))
        delete.place(x=1221, y=50)

    def edit_table3(self, event):
        self.fill_search_entry(self.table3)
        redact = tk.Button(text="Редакт", width=10, font=("Verdana", 8), bg="DarkOliveGreen1",
                           command=lambda: self.table_update('rayon', self.table3, ["rayon", "nazv", "kolvo_mag"]))
        redact.place(x=1131, y=50)
        delete = tk.Button(text="Удален", width=10, font=("Verdana", 8), bg="firebrick1",
                           command=lambda: self.delete_record('rayon', self.table3))
        delete.place(x=1221, y=50)

    def edit_table4(self, event):
        self.fill_search_entry(self.table4)
        redact = tk.Button(text="Редакт", width=10, font=("Verdana", 8), bg="DarkOliveGreen1",
                           command=lambda: self.table_update('administrator', self.table4, ["administrator", "imya", "famil", "otch", "telefon"]))
        redact.place(x=1131, y=50)
        delete = tk.Button(text="Удален", width=10, font=("Verdana", 8), bg="firebrick1",
                           command=lambda: self.delete_record('administrator', self.table4))
        delete.place(x=1221, y=50)

