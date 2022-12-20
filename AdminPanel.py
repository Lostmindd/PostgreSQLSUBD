import tkinter as tk
import UserPanel

class AdminPanel(UserPanel.UserPanel):
    def __init__(self, connect_cursor):
        super().__init__(connect_cursor)
        self.table1.bind('<<TreeviewSelect>>', self.edit_table)
        self.table2.bind('<<TreeviewSelect>>', self.edit_table)
        self.table3.bind('<<TreeviewSelect>>', self.edit_table)
        self.table5.bind('<<TreeviewSelect>>', self.edit_table)


    def delete_record(self):
        item = self.table1.item(self.table1.selection())
        print(item['values'][0])

    def edit_table(self, event):
        redact = tk.Button(text="Редакт", width=10, font=("Verdana", 8), bg="DarkOliveGreen1")
        redact.place(x=1221, y=50)
        redact.lift()
        delete = tk.Button(text="Удален", width=10, font=("Verdana", 8), bg="firebrick1", command=self.delete_record)
        delete.place(x=1311, y=50)
        delete.lift()

        # for selection in self.table1.selection():
        #     item = self.table1.item(selection)
        #     print(item['values'])

    def create_admin_finction(self):
        pass
