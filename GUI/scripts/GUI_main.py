import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from db_create import CREATE_DATABASE
from sqlalchemy import exc
from auxiliary import post_tables


class SQLTreeView(ttk.Treeview):
    """ ttk.TreeView that is able to interact with a specific table/view in a given DB """

    def __init__(self, root, db, table, *args, **kwargs):
        self.root = root
        self.db = db
        self.table = table
        self.select_columns = ', '.join([c for c in table['columns']])
        # this workaround allows us to get columns of a given table
        # FIXME be careful with sql injections when using f-strings
        # self.columns = list(self.db.execute(f'select * from {self.table} where false;').keys())
        super().__init__(root, columns=table['columns'], show='headings', **kwargs)
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label='Выбрать все', command=self.select_all)
        self.popup_menu.add_command(label='Снять выделение', command=self.deselect)
        self.popup_menu.add_command(label='Добавить', command=self.create_record)
        self.popup_menu.add_command(label='Удалить', command=self.delete_records)
        self.popup_menu.add_command(label='Изменить', command=self.update_record)
        self.bind('<Button-3>', self.popup)

        # col_width = int((self.root.master.root.master.winfo_width() - 20) / len(table['columns']))
        for col, heading in zip(table['columns'], table['col_headings']):
            self.column(col, anchor=tk.CENTER, minwidth=10, stretch=False)
            self.heading(col, text=heading)
        self.read_records()

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def select_all(self, event=None):
        """ Selects all lines in the treeview """

        self.selection_set(tuple(self.get_children()))

    def deselect(self, event=None):
        """ Remove selection """

        [self.selection_remove(item) for item in self.selection()]

    def read_records(self):
        """ Loads all records from DB into the treeview """
        records = self.db.execute(f'SELECT {self.select_columns} FROM {self.table["name"]};').fetchall()
        [self.delete(i) for i in self.get_children()]
        [self.insert('', 'end', values=list(row)) for row in records]

    def create_record(self):
        print(f'{self.table}.create_record')
        AddDialog(self, self.table).show()
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

    def update_record(self):
        print(f'{self.table}.update_record')
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

    def delete_records(self, event=None):
        """ Deletes selected records from the DB and refreshes the treeview """

        print(f'{self.table}.delete_records')
        try:
            for item in self.selection():
                self.db.execute(text(f'DELETE FROM {self.table["name"]} WHERE {self.table["columns"][0]} = :id'), id=self.set(item, '#1'))
        except exc.SQLAlchemyError as err:
            messagebox.showerror(title='Ошибка', message=err)
        self.read_records()


class SQLNotebook(ttk.Notebook):
    """ ttk.Notebook that is able to interact with specific tables/views in a given DB """

    def __init__(self, root, db, tables=None, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.db = db
        self.tables = tables
        self.current_tab = None
        self.current_tab_id = 0
        self.tabs_frames = [tk.Frame(self) for i in range(len(self.tables))]
        self.tabs_tables = [SQLTreeView(frame, self.db, table)
                            for frame, table in zip(self.tabs_frames, tables)]
        for frame, table in zip(self.tabs_frames, self.tabs_tables):
            frame.pack(expand=True, fill=tk.BOTH)

            scroll_x = tk.Scrollbar(frame, orient='horizontal', command=table.xview)
            scroll_x.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH)

            table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

            scroll_y = tk.Scrollbar(frame, command=table.yview)
            scroll_y.pack(side=tk.RIGHT, expand=False, fill=tk.BOTH)

            table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.init_notebook()

    def init_notebook(self):
        for i, table in enumerate(self.tables):
            self.add(self.tabs_frames[i], padding=3)
            self.tab(i, text=table['heading'])
        self.current_tab = self.index('current')
        self.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def create_record(self):
        """ Call create_record() of a currently selected table """

        self.tabs_tables[self.index(self.select())].create_record()

    def update_record(self):
        """ Call update_record() of a currently selected table """

        self.tabs_tables[self.index(self.select())].update_record()

    def delete_records(self):
        """ Call delete_records() of a currently selected table """

        self.tabs_tables[self.index(self.select())].delete_records()

    def reset_records(self):
        """ Call read_records() of a currently selected table """

        self.tabs_tables[self.index(self.select())].read_records()

    def on_tab_change(self, event):
        # TODO remove this ???
        # this may be unnecessary because we can do the following
        # self.tabs_tables[self.index(self.select())] to get current tab
        # self.index(self.select()) to get current tab's index
        self.current_tab = event.widget.select()
        self.current_tab_id = event.widget.index(self.current_tab)


class MainWindow(tk.Frame):
    """ Main window class with a SQLNotebook and some buttons """

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.minsize(550, 450)
        self.window_width = 800
        self.window_height = 600
        self.init_main()
        self.cashier_station = {'direction': None, 'station': None}
        self.employee_post = None
        self.connect()
        self.configure_notebook()
        self.root.title(self.employee_post)

    def init_main(self):
        root_width = self.root.winfo_screenwidth()
        root_height = self.root.winfo_screenheight()
        left = (root_width - self.window_width) // 2
        top = (root_height - self.window_height) // 2
        self.root.geometry(f'{self.window_width}x{self.window_height}+{left}+{top}')

        self.f_btns = tk.Frame(height=self.window_height*1//8)
        self.f_tabs = tk.Frame(height=self.window_height*7//8)

        self.btn_create = tk.Button(self.f_btns, text='Добавить', width=10, command=self.on_create)
        self.btn_update = tk.Button(self.f_btns, text='Изменить', width=10, command=self.on_update)
        self.btn_delete = tk.Button(self.f_btns, text='Удалить', width=10, command=self.on_delete)
        self.btn_reset = tk.Button(self.f_btns, text='Сброс', width=10, command=self.on_reset)
        self.btn_search = tk.Button(self.f_btns, text='Поиск', width=10, command=self.on_search)

        self.btn_create.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_update.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_delete.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_reset.pack(side=tk.RIGHT, padx=10, pady=10)
        self.btn_search.pack(side=tk.RIGHT, padx=10, pady=10)

        self.f_btns.pack(expand=False, fill=tk.BOTH)
        self.f_tabs.pack(expand=True, fill=tk.BOTH)

    def on_create(self):
        print('on_create')
        self.nb_main.create_record()
        # # exception example
        # try:
        #     self.db.execute("INSERT INTO stations VALUES(13, 'Мытищи', 3, 16.68, 'Ярославское')")
        # except exc.SQLAlchemyError as err:
        #     messagebox.showerror(title='Ошибка', message=err)
        # try:
        #     self.db.execute("INSERT INTO directions VALUES('asdf', 28, '123456')")
        # except exc.SQLAlchemyError as err:
        #     messagebox.showerror(title='Ошибка', message=err)

    def on_update(self):
        print('on_update')
        self.nb_main.update_record()

    def on_delete(self):
        print('on_delete')
        self.nb_main.delete_records()

    def on_reset(self):
        print('on_reset')
        self.nb_main.reset_records()

    def on_search(self):
        print('on_search')

    def configure_notebook(self):
        """ Create a SQLNotebook instance """

        # tables that will be accessible with the notebook
        tables = ['directions', 'stations']  # , 'active_staff']
        self.nb_main = SQLNotebook(self.f_tabs, self.db, post_tables[self.employee_post])
        self.nb_main.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def connect(self):
        """ Connect to a DB with the given logpass like {'login': str, 'password': str} """

        success = False
        logpass = AuthDialog(self).show()
        while not success:
            try:
                if not logpass:
                    self.root.destroy()
                    sys.exit()
                db_connect = f'postgresql://{logpass["login"]}:{logpass["password"]}@localhost:5432/suburban_trains'
                self.db = create_engine(db_connect)
                self.db.connect()
            except exc.SQLAlchemyError as err:
                messagebox.showerror(title='Ошибка', message='Неверные данные для входа!')
                logpass = AuthDialog(self).show()
            else:
                success = True

        for table in CREATE_DATABASE:
            self.db.execute(table)

        employee_post = self.db.execute(text('SELECT post FROM employees WHERE tabno=:login'), login=logpass['login'])
        if employee_post.rowcount == 0:
            messagebox.showerror(title='Ошибка', message='Работник не найден.')
            self.destroy()
            sys.exit()
        self.employee_post = employee_post.fetchone()[0]
        if self.employee_post == 'Кассир':
            self.cashier_station = CashierDialog(self).show()
            print(self.cashier_station)


class ModalWindow(tk.Toplevel):
    """ Base modal window class. Inherit from it to create other modal windows """

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


class AddDialog(ModalWindow):
    """ Window for change data """

    def __init__(self, root, table):
        super().__init__(root)
        self.init_pass(table)
        # self.root.root.withdraw()
        self.protocol('WM_DELETE_WINDOW', self.on_exit)

    def create_combobox(self, column, table, i):
        self.Edits[i] = ttk.Combobox(self)
        self.Edits[i]['values'] = [item[0] for item in self.root.db.execute(f"SELECT {column} FROM {table}").fetchall()]

    def init_pass(self, table):
        self.title('Введите значения')
        x = str(self.root.winfo_screenwidth() // 2 - 150)
        y = str(self.root.winfo_screenheight() // 2 - 200)
        self.geometry('350x400+' + x + '+' + y)
        self.Labels = [None] * len(table['columns'])
        self.Edits = [None] * len(table['columns'])
        self.retDict = dict()
        for i in range(len(table['columns'])):
            heading = table['col_headings'][i]
            self.retDict[heading] = tk.StringVar()
            editHeight = 0.8 * 400 / len(table['col_headings'])
            self.Labels[i] = tk.Label(self, text=heading + ':', anchor='e')
            self.Labels[i].place(relx=0.1, y=40 + i * editHeight, width=100)
            if heading == 'Модель':
                self.create_combobox('model', 'trains', i)
            elif heading == 'Поезд':
                self.create_combobox('id', 'trains', i)
            elif heading == 'Номер маршрута':
                self.create_combobox('id', 'routes', i)
            elif heading == 'Направление':
                self.create_combobox('name', 'directions', i)
            elif heading == 'Пригородная зона':
                self.create_combobox('', '', i)
            else:
                self.Edits[i] = tk.Entry(self,
                                         textvariable=self.retDict[table['col_headings'][i]],
                                         validate='key')
            self.Edits[i].place(relx=0.5, y=40 + i * editHeight, width=100)
        self.ok_button = tk.Button(self, text='OK', command=self.on_ok)
        self.ok_button.place(relx=.5, rely=.9, relwidth=.4,
                             height=30, anchor='c')
        self.bind('<Return>', self.on_ok)

    def on_exit(self, event=None):
        self.retDict = None
        self.destroy()

    def on_ok(self, event=None):
        self.on_exit()

    def show(self):
        self.wait_window()


class AuthDialog(ModalWindow):
    """ Authorization window """

    def __init__(self, root):
        super().__init__(root)
        self.retDict = {'login': tk.StringVar(), 'password': tk.StringVar()}
        self.init_pass()
        self.root.root.withdraw()
        self.protocol('WM_DELETE_WINDOW', self.on_exit)

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
        self.retDict = None
        self.root.root.deiconify()
        self.destroy()

    def show(self):
        self.wait_window()
        if not self.retDict:
            return None
        return {k: v.get() for k, v in self.retDict.items()}


class CashierDialog(ModalWindow):
    """ Cashier dialog """

    def __init__(self, root):
        super().__init__(root)
        self.ret_dict = {'direction': tk.StringVar(), 'station': tk.StringVar(), 'station_id': tk.StringVar()}
        self.init_pass()
        self.root.root.withdraw()
        self.protocol('WM_DELETE_WINDOW', self.on_exit)

    def init_pass(self):
        self.title('Кассир')
        label_welcome = tk.Label(self, text='Выберите направление и станцию,\nна которой сегодня работаете')
        label_welcome.place(x=self.window_width//2, y=20, anchor='center')

        label_direction = tk.Label(self, text='Направление:')
        label_direction.place(x=self.window_width//2, y=80, anchor='e')

        directions = [item[0] for item in self.root.db.execute('SELECT name FROM directions;').fetchall()]
        self.combo_direction = ttk.Combobox(self, values=directions, textvariable=self.ret_dict['direction'])
        self.combo_direction.current(0)
        self.combo_direction.place(x=self.window_width//2, y=80, anchor='w')
        self.combo_direction.bind('<<ComboboxSelected>>', self.update_stations)

        label_station = tk.Label(self, text='Станция:')
        label_station.place(x=self.window_width//2, y=110, anchor='e')

        self.station_ids = []
        self.station_names = []
        self.combo_station = ttk.Combobox(self, values='', textvariable=self.ret_dict['station'])
        self.combo_station.place(x=self.window_width//2, y=110, anchor='w')
        self.update_stations()

        btn_signin = tk.Button(self, text='Подтвердить', command=self.on_submit)
        btn_signin.place(x=self.window_width*3//4, y=150, anchor='e')
        self.bind('<Return>', self.on_submit)

        btn_exit = tk.Button(self, text='Отмена', command=self.on_exit)
        btn_exit.place(x=self.window_width * 3 // 4, y=150, anchor='w')

    def update_stations(self, event=None):
        self.station_ids.clear()
        self.station_names.clear()
        for item in self.root.db.execute(text('SELECT id, name FROM stations WHERE direction=:direction;'),
                                         direction=self.ret_dict['direction'].get()).fetchall():
            self.station_ids.append(item[0])
            self.station_names.append(item[1])
        self.combo_station['values'] = self.station_names
        self.combo_station.set('')

    def on_submit(self, event=None):
        if not self.ret_dict['direction'].get() or not self.ret_dict['station'].get():
            messagebox.showerror(title='Ошибка', message='Поля не могут быть пустыми')
            return
        self.ret_dict['station_id'].set(self.station_ids[self.combo_station.current()])
        self.root.root.deiconify()
        self.destroy()

    def on_exit(self, event=None):
        self.root.root.deiconify()
        self.destroy()
        sys.exit()

    def show(self):
        self.wait_window()
        return {k: v.get() for k, v in self.ret_dict.items()}


if __name__ == '__main__':
    rootObj = tk.Tk()
    app = MainWindow(rootObj)
    app.pack()
    rootObj.mainloop()
