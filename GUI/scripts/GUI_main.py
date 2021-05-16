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
        CreateDialog(self, self.table).show()
        self.read_records()
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

    def update_record(self, selected_row_values):
        print(f'{self.table}.update_record')
        UpdateDialog(self, self.table, selected_row_values).show()
        self.read_records()
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
                self.db.execute(text(f'DELETE FROM {self.table["name"]} WHERE {self.table["columns"][0]} = :id'),
                                id=self.set(item, '#1'))
        except exc.SQLAlchemyError as err:
            messagebox.showerror(title='Ошибка', message=err.orig)
        self.read_records()

    def search_records(self, event=None):
        ScheduleSearch(self, self.table).show()


class SQLNotebook(ttk.Notebook):
    """ ttk.Notebook that is able to interact with specific tables/views in a given DB """

    def __init__(self, root, db, tables=None, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.db = db
        self.tables = tables
        self.current_tab = None
        self.current_tab_id = 0
        self.selected_row_values = None
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
            table.bind("<<TreeviewSelect>>", self.on_tree_select)
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

        self.tabs_tables[self.index(self.select())].update_record(self.selected_row_values)

    def delete_records(self):
        """ Call delete_records() of a currently selected table """

        self.tabs_tables[self.index(self.select())].delete_records()

    def reset_records(self):
        """ Call read_records() of a currently selected table """

        self.tabs_tables[self.index(self.select())].read_records()

    def search_records(self):
        """ Call update_record() of a currently selected table """

        self.tabs_tables[self.index(self.select())].search_records()

    def on_tab_change(self, event):
        self.root.master.children['!mainwindow'].update_btns(self.tables[self.index(self.select())])
        
    def on_tree_select(self, event):
        self.root.master.children['!mainwindow'].update_btns_special(self.tables[self.index(self.select())])
        cur_item = self.tabs_tables [self.index(self.select())].focus()
        self.selected_row_values = self.tabs_tables[self.index(self.select())].item(cur_item)['values']


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

        self.f_btns = tk.Frame(master=self.root, height=self.window_height * 1 // 8)
        self.f_tabs = tk.Frame(master=self.root, height=self.window_height * 7 // 8)

        self.btn_create = tk.Button(self.f_btns, text='Добавить', width=10, command=self.on_create)
        self.btn_update = tk.Button(self.f_btns, text='Изменить', width=10, command=self.on_update)
        self.btn_delete = tk.Button(self.f_btns, text='Удалить', width=10, command=self.on_delete)
        self.btn_reset = tk.Button(self.f_btns, text='Сброс', width=10, command=self.on_reset)
        self.btn_search = tk.Button(self.f_btns, text='Поиск', width=10, command=self.on_search)

        self.f_btns.pack(expand=False, fill=tk.BOTH)
        self.f_tabs.pack(expand=True, fill=tk.BOTH)

        self.btn_create.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_update.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_delete.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_reset.pack(side=tk.RIGHT, padx=10, pady=10)
        self.btn_search.pack(side=tk.RIGHT, padx=10, pady=10)

    def on_create(self):
        print('on_create')
        self.nb_main.create_record()
        # # exception example
        # try:
        #     self.db.execute("INSERT INTO stations VALUES(13, 'Мытищи', 3, 16.68, 'Ярославское')")
        # except exc.SQLAlchemyError as err:
        #     messagebox.showerror(title='Ошибка', message=err.orig)
        # try:
        #     self.db.execute("INSERT INTO directions VALUES('asdf', 28, '123456')")
        # except exc.SQLAlchemyError as err:
        #     messagebox.showerror(title='Ошибка', message=err.orig)

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
        self.nb_main.search_records()

    def configure_notebook(self):
        """ Create a SQLNotebook instance """

        self.nb_main = SQLNotebook(self.f_tabs, self.db, post_tables[self.employee_post])
        self.nb_main.pack(expand=True, fill=tk.BOTH)
        #self.nb_main.tabs_tables[self.nb_main.current_tab_id].bind("<<TreeviewSelect>>", self.on_tree_select)

    def update_btns(self, permissions):
        perm_map = {True: 'normal', False: 'disabled'}
        self.btn_create['state'] = perm_map[permissions['CREATE']]
        self.btn_update['state'] = 'disabled'
        self.btn_delete['state'] = perm_map[permissions['DELETE']]
        
    def update_btns_special(self, permissions):
        perm_map = {True: 'normal', False: 'disabled'}
        self.btn_create['state'] = perm_map[permissions['CREATE']]
        self.btn_update['state'] = perm_map[permissions['UPDATE']]
        self.btn_delete['state'] = perm_map[permissions['DELETE']]

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

        # for table in CREATE_DATABASE:
        #     self.db.execute(table)

        employee_post = self.db.execute(text('SELECT post FROM employees WHERE tabno=:login'), login=logpass['login'])
        if employee_post.rowcount == 0:
            messagebox.showerror(title='Ошибка', message='Работник не найден.')
            self.destroy()
            sys.exit()
        self.employee_post = employee_post.fetchone()[0]

        # if self.employee_post == 'Кассир':
        #     self.cashier_station = CashierDialog(self).show()
        #     print(self.cashier_station)


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


class CreateDialog(ModalWindow):
    """ Window for add data """

    def __init__(self, root, table):
        super().__init__(root)
        self.table = table
        self.init_pass()
        self.protocol('WM_DELETE_WINDOW', self.on_exit)

    # def on_round_trip(self, event, i):
    #     selected_row = event.widget.get()
    #     if selected_row == 'да':
    #         self.retDict[self.table['col_headings'][i]].set('1')
    #     else:
    #         self.retDict[self.table['col_headings'][i]].set('0')

    def on_station_select(self, event):
        selected_row = event.widget.get()
        station = selected_row.split(', ')
        place = self.Edits.index(event.widget)
        self.Edits[place + 1]['values'] = \
            [item[0] for item in self.root.db.execute(f"SELECT name || ', ' || id FROM stations WHERE direction = "
                                                      f"'{station[1]}' AND name != '{station[0]}'").fetchall()]

    def create_combobox(self, column, tab, i, table):
        self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[table['col_headings'][i]])
        self.Edits[i]['values'] = [item[0] for item in self.root.db.execute(f"SELECT {column} FROM {tab}").fetchall()]
        # self.Edits[i].bind("<<ComboboxSelected>>", self.on_cb_select)

    def init_pass(self):
        self.title('Введите значения')
        x = str(self.root.winfo_screenwidth() // 2 - 150)
        y = str(self.root.winfo_screenheight() // 2 - 200)
        self.geometry('350x420+' + x + '+' + y)
        self.Labels = [None] * len(self.table['columns'])
        self.Edits = [None] * len(self.table['columns'])
        self.retDict = dict()
        for i in range(len(self.table['columns'])):
            heading = self.table['col_headings'][i]
            self.retDict[heading] = tk.StringVar()
            editHeight = 0.8 * 400 / len(self.table['col_headings'])
            self.Labels[i] = tk.Label(self, text=heading + ':', anchor='e')
            self.Labels[i].place(relx=0.1, y=40 + i * editHeight, width=140)
            if heading == 'Модель' and self.table['heading'] != 'Модели поездов':
                self.create_combobox('model', 'train_models', i, self.table)
            elif heading == 'Поезд':
                self.create_combobox('id', 'trains', i, self.table)
            elif heading == 'Номер маршрута':
                self.create_combobox('id', 'routes', i, self.table)
            elif heading == 'Направление':
                self.create_combobox('name', 'directions', i, self.table)
            # elif heading == 'Пригородная зона':
            #     self.create_combobox('', '', i)
            elif heading == 'Тип':
                self.create_combobox('name', 'tariffs', i, self.table)
            elif heading == 'Режим движения':
                self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[self.table['col_headings'][i]])
                self.Edits[i]['values'] = ['ежедневно', 'по рабочим', 'по выходным']
            elif heading == 'Сторона':
                self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[self.table['col_headings'][i]])
                self.Edits[i]['values'] = ['в город', 'из города']
            elif heading == 'Машинист':
                self.create_combobox("last_name || ' ' || first_name || ' ' || patronymic || ', ' || tabno",
                                     'machinists', i, self.table)
            # elif heading == 'Кассир':
            #     self.create_combobox("last_name || ' ' || first_name || ' ' || patronymic || ', ' || tabno",
            #                          'cashiers', i, self.table)
            elif heading == 'Туда-обратно':
                self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[self.table['col_headings'][i]])
                # self.Edits[i].bind("<<ComboboxSelected>>", lambda event, i: self.on_round_trip(event, i))
                self.Edits[i]['values'] = ['да', 'нет']
            elif heading in ('Должность'):
                self.create_combobox('post', 'posts', i, self.table)
            elif heading == 'Заведующий':
                self.create_combobox("last_name || ' ' || first_name || ' ' || patronymic || ', ' || tabno",
                                     'route_managers', i, self.table)
            elif heading == 'Откуда':
                self.create_combobox("name || ', ' || direction || ', ' || id", 'stations', i, self.table)
                self.Edits[i].bind("<<ComboboxSelected>>", self.on_station_select)
            elif heading == 'Куда':
                self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[self.table['col_headings'][i]])
            else:
                self.Edits[i] = tk.Entry(self,
                                         textvariable=self.retDict[self.table['col_headings'][i]],
                                         validate='key')
                if heading == 'Остановки':
                    self.Edits[i].config(state='disabled')
                elif heading in ('Кассир', 'Стоимость'):
                    self.Edits[i].config(state='disabled')
                    self.retDict[self.table['col_headings'][i]].set('0')

            self.Edits[i].place(relx=0.5, y=40 + i * editHeight, width=150)
        self.ok_button = tk.Button(self, text='OK', command=self.on_ok)
        self.ok_button.place(relx=.5, rely=.9, relwidth=.4,
                             height=30, anchor='c')
        self.bind('<Return>', self.on_ok)

    def on_exit(self, event=None):
        self.retDict = None
        self.destroy()

    def on_ok(self, event=None):
        input_data = [x.get().split(', ')[-1] for x in list(self.retDict.values())]
        if 'да' in input_data:
            input_data[input_data.index('да')] = '1'
        elif 'нет' in input_data:
            input_data[input_data.index('нет')] = '0'
        insert_data = ', '.join([f"'{x}'" for x in input_data if x != ''])
        try:
            if insert_data:
                self.root.db.execute(text(f"INSERT INTO {self.table['name']} VALUES ({str(insert_data)})"))
        except exc.SQLAlchemyError as err:
            messagebox.showerror(title='Ошибка', message=err.orig)
        self.on_exit()

    def show(self):
        self.wait_window()
        
class UpdateDialog(ModalWindow):
    """ Window for update data """

    def __init__(self, root, table, selected_row_values):
        super().__init__(root)
        self.table = table
        self.selected_row_values = selected_row_values
        self.init_pass()
        self.protocol('WM_DELETE_WINDOW', self.on_exit)

    def on_station_select(self, event):
        selected_row = event.widget.get()
        station = selected_row.split(', ')
        place = self.Edits.index(event.widget)
        self.Edits[place + 1]['values'] = \
            [item[0] for item in self.root.db.execute(f"SELECT name || ', ' || id FROM stations WHERE direction = "
                                                      f"'{station[1]}' AND name != '{station[0]}'").fetchall()]

    def create_combobox(self, column, tab, i, table):
        self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[table['col_headings'][i]])
        self.Edits[i]['values'] = [item[0] for item in self.root.db.execute(f"SELECT {column} FROM {tab}").fetchall()]
        self.Edits[i].set(self.selected_row_values[i])
        
    def init_pass(self):
        self.title('Введите значения')
        x = str(self.root.winfo_screenwidth() // 2 - 150)
        y = str(self.root.winfo_screenheight() // 2 - 200)
        self.geometry('350x420+' + x + '+' + y)
        self.Labels = [None] * len(self.table['columns'])
        self.Edits = [None] * len(self.table['columns'])
        self.retDict = dict()
        for i in range(1, len(self.table['columns'])):
            heading = self.table['col_headings'][i]
            self.retDict[heading] = tk.StringVar()
            editHeight = 0.8 * 400 / len(self.table['col_headings'])
            self.Labels[i] = tk.Label(self, text=heading + ':', anchor='e')
            self.Labels[i].place(relx=0.1, y=40 + i * editHeight, width=140)
            if heading == 'Модель' and self.table['heading'] != 'Модели поездов':
                self.create_combobox('model', 'train_models', i, self.table)
            elif heading == 'Поезд':
                self.create_combobox('id', 'trains', i, self.table)
            elif heading == 'Номер маршрута':
                self.create_combobox('id', 'routes', i, self.table)
            elif heading == 'Направление':
                self.create_combobox('name', 'directions', i, self.table)
            # elif heading == 'Пригородная зона':
            #     self.create_combobox('', '', i)
            elif heading == 'Тип':
                self.create_combobox('name', 'tariffs', i, self.table)
            elif heading == 'Режим движения':
                self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[self.table['col_headings'][i]])
                self.Edits[i]['values'] = ['ежедневно', 'по рабочим', 'по выходным']
                self.Edits[i].set(self.selected_row_values[i])
            elif heading == 'Сторона':
                self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[self.table['col_headings'][i]])
                self.Edits[i]['values'] = ['в город', 'из города']
                self.Edits[i].set(self.selected_row_values[i])
            elif heading == 'Машинист':
                self.create_combobox("last_name || ' ' || first_name || ' ' || patronymic || ', ' || tabno",
                                     'machinists', i, self.table)
            # elif heading == 'Кассир':
            #     self.create_combobox("last_name || ' ' || first_name || ' ' || patronymic || ', ' || tabno",
            #                          'cashiers', i, self.table)
            elif heading == 'Туда-обратно':
                self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[self.table['col_headings'][i]])
                # self.Edits[i].bind("<<ComboboxSelected>>", lambda event, i: self.on_round_trip(event, i))
                self.Edits[i]['values'] = ['да', 'нет']
                self.Edits[i].set(self.selected_row_values[i])
            elif heading in ('Должность'):
                self.create_combobox('post', 'posts', i, self.table)
            elif heading == 'Заведующий':
                self.create_combobox("last_name || ' ' || first_name || ' ' || patronymic || ', ' || tabno",
                                     'route_managers', i, self.table)
            elif heading == 'Откуда':
                self.create_combobox("name || ', ' || direction || ', ' || id", 'stations', i, self.table)
                self.Edits[i].bind("<<ComboboxSelected>>", self.on_station_select)
                self.Edits[i].set(self.selected_row_values[i])
            elif heading == 'Куда':
                self.Edits[i] = ttk.Combobox(self, textvariable=self.retDict[self.table['col_headings'][i]])
                self.Edits[i].set(self.selected_row_values[i])
            else:
                self.Edits[i] = tk.Entry(self,
                                         textvariable=self.retDict[self.table['col_headings'][i]],
                                         validate='key')
                self.Edits[i].insert(0, self.selected_row_values[i])
                if heading == 'Остановки':
                    self.Edits[i].config(state='disabled')
                elif heading in ('Кассир', 'Стоимость'):
                    self.Edits[i].config(state='disabled')
                    self.retDict[self.table['col_headings'][i]].set('0')

            self.Edits[i].place(relx=0.5, y=40 + i * editHeight, width=150)
        self.ok_button = tk.Button(self, text='OK', command=self.on_ok)
        self.ok_button.place(relx=.5, rely=.9, relwidth=.4,
                             height=30, anchor='c')
        self.bind('<Return>', self.on_ok)

    def on_exit(self, event=None):
        self.retDict = None
        self.destroy()

    def on_ok(self, event=None):
        try:
            self.root.db.execute(text(f'UPDATE {self.table["name"]} SET {self.create_set_part()} WHERE {self.table["columns"][0]} = :id'),
                               id=self.selected_row_values[0])
        except exc.SQLAlchemyError as err:
            messagebox.showerror(title='Ошибка', message=err.orig)
        self.on_exit()

    def show(self):
        self.wait_window()
        
    def create_set_part(self):
        input_data = [x.get().split(', ')[-1] for x in list(self.retDict.values())]
        for i in range(len(input_data)):
            try:
                temp = int(float(input_data[i]))
            except:
                try:
                    input_data[i] = "'" + input_data[i].get() + "'"
                except:
                    input_data[i] = "'" + input_data[i] + "'"
        result = ''
        for i in range(1, len(self.table['columns'])):
            result = result + self.table['columns'][i] + '=' + input_data[i-1] + ', '
        return result[:-2]


class ScheduleSearch(ModalWindow):
    """ Search window for schedule """

    def __init__(self, root, table):
        super().__init__(root)
        self.retDict = {'from': tk.StringVar(), 'to': tk.StringVar()}
        self.table = table
        self.init_pass()
        self.protocol('WM_DELETE_WINDOW', self.on_exit)

    def init_pass(self):
        self.title("Поиск по дате")

        label_from = tk.Label(self, text='Поиск по дате')
        label_from.place(x=self.window_width // 2, y=20, anchor='center')

        label_to = tk.Label(self, text='Нижняя граница:')
        label_to.place(x=self.window_width // 2, y=80, anchor='e')

        self.entry_from = tk.Entry(self, textvariable=self.retDict['from'])
        self.entry_from.place(x=self.window_width // 2, y=80, anchor='w')

        label_pass = tk.Label(self, text='Верхняя граница:')
        label_pass.place(x=self.window_width // 2, y=110, anchor='e')

        self.entry_to = tk.Entry(self, textvariable=self.retDict['to'])
        self.entry_to.place(x=self.window_width // 2, y=110, anchor='w')

        self.ok_button = tk.Button(self, text='OK', command=self.on_ok)
        self.ok_button.place(x=self.window_width // 2, y=150, anchor='center')
        self.bind('<Return>', self.on_ok)

    def on_exit(self, event=None):
        self.retDict = None
        self.destroy()

    def on_ok(self, event=None):
        input_data = [value.get() for key, value in self.retDict.items()]
        if input_data:
            if not input_data[0]:
                print(self.root.db.execute(text("SELECT * FROM rides_verbose WHERE ddate < :input_date"),
                                     input_date=input_data[1]).fetchall())
            elif not input_data[1]:
                print(self.root.db.execute(text("SELECT * FROM rides_verbose WHERE ddate > :input_date"),
                                     input_date=input_data[0]).fetchall())
            else:
                print(self.root.db.execute(text("SELECT * FROM rides_verbose WHERE ddate BETWEEN (:from_date, :to_date)"),
                                     from_date=input_data[0], to_date=input_data[1]).fetchall())
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
        label_welcome.place(x=self.window_width // 2, y=20, anchor='center')

        label_login = tk.Label(self, text='Табельный номер:')
        label_login.place(x=self.window_width // 2, y=80, anchor='e')

        self.entry_login = tk.Entry(self, textvariable=self.retDict['login'])
        self.entry_login.place(x=self.window_width // 2, y=80, anchor='w')

        label_pass = tk.Label(self, text='Пароль:')
        label_pass.place(x=self.window_width // 2, y=110, anchor='e')

        self.entry_pass = tk.Entry(self, show='*', textvariable=self.retDict['password'])
        self.entry_pass.place(x=self.window_width // 2, y=110, anchor='w')

        btn_signin = tk.Button(self, text='Войти', command=self.on_submit)
        btn_signin.place(x=self.window_width * 3 // 4, y=150, anchor='e')
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
        label_welcome.place(x=self.window_width // 2, y=20, anchor='center')

        label_direction = tk.Label(self, text='Направление:')
        label_direction.place(x=self.window_width // 2, y=80, anchor='e')

        directions = [item[0] for item in self.root.db.execute('SELECT name FROM directions;').fetchall()]
        self.combo_direction = ttk.Combobox(self, values=directions, textvariable=self.ret_dict['direction'])
        self.combo_direction.current(0)
        self.combo_direction.place(x=self.window_width // 2, y=80, anchor='w')
        self.combo_direction.bind('<<ComboboxSelected>>', self.update_stations)

        label_station = tk.Label(self, text='Станция:')
        label_station.place(x=self.window_width // 2, y=110, anchor='e')

        self.station_ids = []
        self.station_names = []
        self.combo_station = ttk.Combobox(self, values='', textvariable=self.ret_dict['station'])
        self.combo_station.place(x=self.window_width // 2, y=110, anchor='w')
        self.update_stations()

        btn_signin = tk.Button(self, text='Подтвердить', command=self.on_submit)
        btn_signin.place(x=self.window_width * 3 // 4, y=150, anchor='e')
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
        # TODO read records

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
