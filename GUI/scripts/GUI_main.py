import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sqlalchemy import create_engine


class TreeViewWithPopup(ttk.Treeview):
    def __init__(self, root, *args, **kwargs):
        super().__init__(self)
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label='Удалить',
                                    command=self.deleteRecords)
        self.popup_menu.add_command(label='Выбрать все',
                                    command=self.selectAll)
        self.popup_menu.add_command(label='Изменить',
                                    command=self.modRecord)
        self.popup_menu.add_command(label='Добавить',
                                    command=self.addRecord)
        self.bind('<Button-3>', self.popup)
        self.root = root
        self.globalCounter = 0

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def add(self, parent, values):
        self.insert('', 'end', iid=self.globalCounter, values=values)
        self.globalCounter += 1

    def selectAll(self, event=None):
        self.selection_set(tuple(self.get_children()))

    def addRecord(self):
        print('addRecord')
        # nb = self.master.master
        # nb = nb.index(nb.select())
        # dic = funcs.askValuesDialog(self.root, self.config, DB.db[nb].columns).show()
        # values = list(dic.values())
        # keys = list(dic.keys())
        # if len(values):
        #     values = [item.get() for item in values]
        #     values[0] = str(self.genUID())
        #     DB.modified = True
        #
        #     DB.db[nb] = DB.db[nb].append(
        #         pd.DataFrame([[np.int64(item) if item.isdigit() else item for item in values]],
        #                      columns=keys), ignore_index=True)
        #     self.add('', values=values)

    def deleteRecords(self, event=None):
        print('deleteRecords')
        # nb = self.master.master
        # nb = nb.index(nb.select())
        # selected = [int(i) for i in self.selection()]
        # if not len(selected):
        #     funcs.message(self.root, 'Не выбран элемент', msgtype='warning').fade()
        # else:
        #     DB.modified = True
        #     for item in selected:
        #         itemId = int(self.item(item)['values'][0])
        #         DB.db[nb] = DB.db[nb].drop(DB.db[nb].index[DB.db[nb]['Код'] == itemId])
        #         self.delete(self.selection()[0])

    def modRecord(self):
        print('modRecord')
        # nb = self.master.master
        # nb = nb.index(nb.select())
        # selected = self.selection()
        # if not selected:
        #     funcs.message(self.root, 'Не выбран элемент', msgtype='warning').fade()
        # else:
        #     selected = int(selected[0])
        #     itemId = np.int64(self.item(selected)['values'][0])
        #     itemValues = DB.db[nb][DB.db[nb]['Код'] == itemId].values[0].tolist()
        #     dic = funcs.askValuesDialog(self.root, self.config, DB.db[nb].columns,
        #                                 currValues=itemValues).show()
        #     keys = list(dic.keys())
        #     values = list(dic.values())
        #     if len(values):
        #         values = [item.get() for item in values]
        #         values[0] = itemId
        #         DB.modified = True
        #         for i in range(len(keys)):
        #             self.item(selected, values=values)
        #             DB.db[nb].loc[itemId - 1, keys[i]] = values[i]


class SQLNotebook(ttk.Notebook):
    def __init__(self, root, views=None, headings=None, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.views = views
        self.headings = headings
        self.tabs = [tk.Frame(self) for i in range(len(views))]
        self.init_notebook()

    def init_notebook(self):
        for i, view, heading in zip(range(len(self.views)), self.views, self.headings):
            self.add(self.tabs[i], padding=3)
            self.tab(i, text=heading)


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.minsize(550, 450)
        self.window_width = 800
        self.window_height = 600
        self.init_main()
        logpass = PassWindow(self).show()
        self.connect(logpass)

    def init_main(self):
        self.root.title('Т Е С Т')
        root_width = self.root.winfo_screenwidth()
        root_height = self.root.winfo_screenheight()
        left = (root_width - self.window_width) // 2
        top = (root_height - self.window_height) // 2
        self.root.geometry(f'{self.window_width}x{self.window_height}+{left}+{top}')

        self.f_btns = tk.Frame(height=self.window_height*1//8)
        self.f_tabs = tk.Frame(height=self.window_height*7//8, bg='red')

        self.btn_create = tk.Button(self.f_btns, text='Добавить', width=10, command=self.on_create)
        self.btn_update = tk.Button(self.f_btns, text='Изменить', width=10, command=self.on_update)
        self.btn_delete = tk.Button(self.f_btns, text='Удалить', width=10, command=self.on_delete)
        self.btn_reset = tk.Button(self.f_btns, text='Сброс', width=10, command=self.on_reset)
        self.btn_search = tk.Button(self.f_btns, text='Поиск', width=10, command=self.on_search)

        self.btn_create.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_update.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_delete.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_reset.pack(side=tk.RIGHT,  padx=10, pady=10)
        self.btn_search.pack(side=tk.RIGHT, padx=10, pady=10)

        self.nb_main = SQLNotebook(self.f_tabs, views=['foo', 'bar', 'baz'], headings=['11', '22', '33'])
        self.nb_main.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.f_btns.pack(expand=False, fill=tk.BOTH)
        self.f_tabs.pack(expand=False, fill=tk.BOTH)
        # btn_edit_dialog = tk.Button(self, text='Тест', bg='#ffffff', bd=2, command=self.open_auth_dialog)
        # btn_edit_dialog.pack()

    def on_create(self):
        print('on_create')

    def on_update(self):
        print('on_update')

    def on_delete(self):
        print('on_delete')

    def on_reset(self):
        print('on_reset')

    def on_search(self):
        print('on_search')

    def connect(self, logpass):
        # messagebox.showinfo(title='WOW', message=f'Login: {login}\nPassword: {password}')
        print(f'Login: {logpass["login"]}\nPassword: {logpass["password"]}')
        db_connect = f'postgresql://{logpass["login"]}:{logpass["password"]}@localhost:5432/suburban_trains'
        # self.db = create_engine(db_connect)

    def open_auth_dialog(self):
        PassWindow(self)


class ModalWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.window_width = 300
        self.window_height = 200
        self.init_modal()

    def init_modal(self):
        self.title('Modal window')
        root_width = self.root.winfo_screenwidth()
        root_height = self.root.winfo_screenheight()
        left = (root_width - self.window_width) // 2
        top = (root_height - self.window_height) // 2
        self.geometry(f'{self.window_width}x{self.window_height}+{left}+{top}')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()


class PassWindow(ModalWindow):
    def __init__(self, root):
        super().__init__(root)
        self.retDict = {'login': tk.StringVar(), 'password': tk.StringVar()}
        self.init_pass()
        self.root.root.withdraw()

    def init_pass(self):
        self.title('Авторизация')
        label_welcome = tk.Label(self, text='Введите логин и пароль')
        label_welcome.place(x=self.window_width//2, y=20, anchor='center')

        label_login = tk.Label(self, text='Табельный номер:')
        label_login.place(x=self.window_width//2, y=80, anchor='e')

        self.entry_login = tk.Entry(self, textvariable=self.retDict['login'])
        self.entry_login.place(x=self.window_width//2, y=80, anchor='w')

        label_pass = tk.Label(self, text='Пароль:')
        label_pass.place(x=self.window_width//2, y=110, anchor='e')

        self.entry_pass = tk.Entry(self, show='*', textvariable=self.retDict['password'])
        self.entry_pass.place(x=self.window_width//2, y=110, anchor='w')

        btn_signin = tk.Button(self, text='Войти', command=self.on_submit)
        btn_signin.place(x=self.window_width*3//4, y=150, anchor='e')
        self.bind('<Return>', self.on_submit)

        btn_exit = tk.Button(self, text='Отмена', command=self.on_exit)
        btn_exit.place(x=self.window_width * 3 // 4, y=150, anchor='w')

    def on_submit(self, event=None):
        self.root.root.deiconify()
        self.destroy()

    def on_exit(self, event=None):
        self.root.root.deiconify()
        self.destroy()

    def show(self):
        self.wait_window()
        return {k: v.get() for k, v in self.retDict.items()}


if __name__ == '__main__':
    rootObj = tk.Tk()
    app = MainWindow(rootObj)
    app.pack()
    rootObj.mainloop()
