import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.minsize(400, 300)
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

        btn_edit_dialog = tk.Button(self, text='Тест', bg='#ffffff', bd=2, command=self.open_auth_dialog)
        btn_edit_dialog.pack()

    def connect(self, logpass):
        # messagebox.showinfo(title='WOW', message=f'Login: {login}\nPassword: {password}')
        print(f'Login: {logpass["login"]}\nPassword: {logpass["password"]}')

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
        btn_signin.bind('<Return>', self.on_submit)

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
