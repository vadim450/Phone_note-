import tkinter as tk
from tkinter import ttk
import sqlite3

# главный класс
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    # виджеты для главного окна
    def init_main(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # кнопка добавления
        self.img_add = tk.PhotoImage(file="F:/PRO/img/add.png")
        btn_add = tk.Button(toolbar, text="Добавить", bg="#d7d8e0",
                            bd = 0, image=self.img_add,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # кнопка редактирования
        self.upd_img = tk.PhotoImage(file="F:/PRO/img/update.png")
        btn_upd = tk.Button(toolbar, bg="#d7d8e0",
                            bd = 0, image=self.upd_img,
                            command=self.open_update)
        btn_upd.pack(side=tk.LEFT)

        # кнопка удаления
        self.del_img = tk.PhotoImage(file="F:/PRO/img/delete.png")
        btn_del = tk.Button(toolbar, bg="#d7d8e0",
                            bd = 0, image=self.del_img,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)
        
        # кнопка поиска
        self.search_img = tk.PhotoImage(file="F:/PRO/img/search.png")
        btn_search = tk.Button(toolbar, bg="#d7d8e0",
                            bd = 0, image=self.search_img,
                            command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.refresh_img = tk.PhotoImage(file="F:/PRO/img/refresh.png")
        btn_refresh = tk.Button(toolbar, bg="#d7d8e0",
                            bd = 0, image=self.refresh_img,
                            command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # таблица для вывода информоции для контактов
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'),
                                 show='headings', height=45)

        # настройка столбцов
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        
        # название столбцов
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Email')
        
        self.tree.pack()

        # скроллбар
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        # Метод добавления данных

    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()


    def view_records(self):
        self.db.cur.execute("SELECT * FROM users")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    # Метод поиска данных

    def search_records(self, name):
        self.db.cur.execute("SELECT * FROM users WHERE name LIKE ?",
                            ("%" + name + "%", ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    # Метод изменения данных
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], "#1")
        self.db.cur.execute("""
            UPDATE users
            SET name = ?, phone = ?, email = ?
            WHERE id = ?
        """, (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления строк
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute("DELETE FROM users WHERE id = ?",
                                (self.tree.set(row, "#1"), ))
            
            self.db.conn.commit()
            self.view_records()

    # открытие окна добавления
    def open_child(self):
        Child()

    # открытие окна редактирования
    def open_update(self):
        Update()

    # открытие окна поиска
    def open_search(self):
        Search()

# класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    # виджеты для дочерних окон
    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x200')
        self.resizable(False, False)

        # перехват события
        self.grab_set()

        # перехват фокуса
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_phone = tk.Label(self, text='Телефон')
        label_email = tk.Label(self, text='Email')

        label_name.place(x=60, y=50)
        label_phone.place(x=60, y=70)
        label_email.place(x=60, y=90)

        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)

        self.entry_name.place(x=250, y=50)
        self.entry_phone.place(x=250, y=70)
        self.entry_email.place(x=250, y=90)

        btn_close = tk.Button(self, text= 'Закрыть', command=self.destroy)
        btn_close.place(x=250, y=160)

        self.btn_add = tk.Button(self, text="Добавить")
        self.btn_add.bind("<Button-1>", lambda ev: self.view.records(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get() ))
        self.btn_add.place(x=310, y=160)

# класс редактирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title("Изменение контакта")
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text="Изменить")
        self.btn_upd.bind("<Button-1>",lambda ev: self.view.update_record(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get() ))
        self.btn_upd.bind("<Button-1>", lambda ev: self.destroy(), add="+")
        self.btn_upd.place(x=310, y=160)

# метод автозаполнения формы
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], "#1")
        self.db.cur.execute("SELECT * from users WHERE id = ?", (id, ))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])

# класс окон поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()

    # виджеты для окон поиска
    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False, False)

        # перехват события
        self.grab_set()

        # перехват фокуса
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=40, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=140, y=20)
        
        btn_close = tk.Button(self, text= 'Закрыть', command=self.destroy)
        btn_close.place(x=130, y=70)

        self.btn_add = tk.Button(self, text='Найти')
        self.btn_add.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_add.bind('<Button-1>', lambda ev: self.destroy(),
                          add='+')
        self.btn_add.place(x=220, y=70)


# класс базы данных
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT )''')
    
    # метод добавления в базу двнных
    def insert_data(self, name, phone, email):
        self.cur.execute('''INSERT INTO users (name, phone, email)
                         VALUES (?,?,?)''', (name, phone, email))
        self.conn.commit()

# запуск
if __name__ == '__main__':
    root = tk.Tk()
    # экземпляр класса Db
    db = Db()
    app = Main(root)
    app.pack()
    # заголовок окна
    root.title('Список сотрудников компании')
    # размер окна
    root.geometry('665x450')
    # ограничение изменения размеров окна
    root.resizable(False, False)
    root.mainloop()