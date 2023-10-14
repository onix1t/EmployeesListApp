import sqlite3
import tkinter as tk
from tkinter import ttk

# создаине интерфейса программы
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # кнопка добавления
        self.add_img = tk.PhotoImage(file="./img/add.png", height=50, width=50)
        btn_open_add_win = tk.Button(
            toolbar, 
            bg="#d7d8e0", 
            bd=0, 
            image=self.add_img, 
            command=self.open_add_win
        )
        btn_open_add_win.pack(side=tk.LEFT)

        # кнопка обновления
        self.update_img = tk.PhotoImage(file="./img/update.png", height=50, width=50)
        btn_edit_win = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_win,
        )
        btn_edit_win.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file="./img/search.png", height=50, width=50)
        btn_search_win= tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_win,
        )
        btn_search_win.pack(side=tk.LEFT)

        # кнопка удаления
        self.delete_img = tk.PhotoImage(file="./img/delete.png", height=50, width=50)
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.RIGHT)

        # вывод через виджет Treeview
        self.tree = ttk.Treeview(
            self, 
            columns=("ID", "name", "phone", "email", "salary"),
            height=45, 
            show="headings"
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH)

        # полоса прокрутки
        self.scroll = ttk.Scrollbar(
            self, 
            orient="vertical", 
            command=self.tree.yview
        )
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=self.scroll.set)

        # столбцы таблтцы базы данных
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=225, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=225, anchor=tk.CENTER)
        self.tree.column("salary", width=100, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")
    
    # считывание и добавление данных
    def open_add_win(self):
        Add(self)

    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    def view_records(self):
        self.db.cursor.execute("SELECT * FROM employees")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    def open_update_win(self):
        Update(self)

    def update_records(self, name, phone, email, salary):
        self.db.cursor.execute(
            """UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?""",
            (name, phone, email, salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM employees WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records()

    def open_search_win(self):
        Search(self)

    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM employees WHERE name LIKE ?", (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

# создание окна функции добавления
class Add(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_add()

    def init_add(self):
        self.title("Добавление контакта")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=35)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=65)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=95)
        label_salary = tk.Label(self, text="Зарплата:")
        label_salary.place(x=50, y=125)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=125, y=35, width=200)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=125, y=65, width=200)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=125, y=95, width=200)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=125, y=125, width=200)

        self.btn_add = ttk.Button(self, text="Добавить")
        self.btn_add.place(x=125, y=160)

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=205, y=160)


        self.btn_add.bind(
            "<Button-1>",
            lambda event: self.parent.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_phone.get(),
                self.entry_salary.get()
            ),
        )

# создание окна функции редактирования
class Update(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_edit()

    def init_edit(self):
        self.title("Редактирование контакта")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=35)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=65)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=95)
        label_salary = tk.Label(self, text="Зарплата:")
        label_salary.place(x=50, y=125)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=125, y=35, width=200)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=125, y=65, width=200)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=125, y=95, width=200)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=125, y=125, width=200)
        
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=160)

        btn_edit = ttk.Button(self, text="Редактировать", command=self.destroy)
        btn_edit.place(x=125, y=160)
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.parent.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_phone.get(),
                self.entry_salary.get()
            ),
        )
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")

    def default_data(self):
        self.parent.db.cursor.execute(
        "SELECT * FROM employees WHERE id=?",
        self.parent.tree.set(self.parent.tree.selection()[0], "#1"),
        )
        row = self.parent.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_phone.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# создание окна функции поиска
class Search(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_search()

    def init_search(self):
        self.title("Поиск контакта")
        self.geometry("325x100")
        self.resizable(False, False)
        
        self.grab_set()
        self.focus_set()

        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=25, y=25)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=75, y=25, width=200)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=155, y=60)

        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=75, y=60)
        search_btn.bind(
            "<Button-1>",
            lambda event: self.parent.search_records(self.entry_search.get()),

        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")

# структура базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("employees.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                name TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                salary REAL
            )"""
        )
        self.conn.commit()

    def insert_data(self, name, phone, email, salary):
        self.cursor.execute(
            """INSERT INTO employees(name, phone, email, salary) VALUES(?, ?, ?, ?)""",
            (name, phone, email, salary)
        )
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("750x350")
    root.resizable(False, False)
    root.mainloop()
