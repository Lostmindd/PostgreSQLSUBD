import tkinter as tk
import UserPanel
import psycopg2

class AdminPanel(UserPanel.UserPanel):
    def __init__(self, connect_cursor, user_level):
        super().__init__(connect_cursor, user_level)
        self.table1.bind('<<TreeviewSelect>>', self.edit_table)
        self.table2.bind('<<TreeviewSelect>>', self.edit_table)
        self.table3.bind('<<TreeviewSelect>>', self.edit_table)
        self.table4.bind('<<TreeviewSelect>>', self.edit_table)


    def delete_record(self, table_name, table):
        row = table.item(table.selection())
        try:
            self.connect_cursor.execute("DELETE FROM " + table_name + " WHERE " + table_name + " = " + str(row['values'][0]))
            self.connect_cursor.execute("COMMIT")
            self.refresh_table(table, table_name)
        except psycopg2.Error:
            self.connect_cursor.execute("ROLLBACK")

    def search_entry_fill(self, search_entry, table):
        row = table.item(table.selection())
        for i in range(len(search_entry)):
            search_entry[i].insert(0, row['values'][i])

    def table_update(self, records, columns, key_column, table_name, table, search_entry):
        search_str = ""
        for i in range(len(records)):
            if records[i].get() != '':
                search_str += columns[i] + " = '" + records[i].get() + "', "
        search_str = search_str[:-2]
        if search_str != '':
            try:
                self.connect_cursor.execute("UPDATE " + table_name + " SET " + search_str + " WHERE " + table_name + " = " + key_column)
                self.connect_cursor.execute("COMMIT")
                self.refresh_table(table, table_name)
            except psycopg2.Error:
                self.connect_cursor.execute("ROLLBACK")

    def edit_table(self, event):
        redact = tk.Button(text="Редакт", width=10, font=("Verdana", 8), bg="DarkOliveGreen1")
        redact.place(x=1131, y=50)
        redact.lift()
        delete = tk.Button(text="Удален", width=10, font=("Verdana", 8), bg="firebrick1",
                           command=lambda : self.delete_record('magazin', self.table1))
        delete.place(x=1221, y=50)
        delete.lift()

        # for selection in self.table1.selection():
        #     item = self.table1.item(selection)
        #     print(item['values'])

    def create_admin_function(self):
        pass
