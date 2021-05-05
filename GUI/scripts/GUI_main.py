import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        btn_edit_dialog = tk.Button(self, text='Тест', bg='#ffffff', bd=2, command=self.open_auth_dialog)
        btn_edit_dialog.pack()

    def connect(self, login, password):
        # messagebox.showinfo(title='WOW', message=f'Login: {login}\nPassword: {password}')
        print(f'Login: {login}\nPassword: {password}')

    def open_auth_dialog(self):
        PassWindow()


class ModalWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_modal()
        self.parent = app

    def init_modal(self):
        self.title('Modal window')
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()


class PassWindow(ModalWindow):
    def __init__(self):
        super().__init__()
        self.init_pass()

    def init_pass(self):
        self.title('Авторизация')
        label_welcome = tk.Label(self, text='Введите логин и пароль')
        label_welcome.place(x=135, y=10)

        label_login = tk.Label(self, text='Табельный номер:')
        label_login.place(x=50, y=50)

        self.entry_login = tk.Entry(self)
        self.entry_login.place(x=200, y=50)

        label_pass = tk.Label(self, text='Пароль:')
        label_pass.place(x=50, y=80)

        self.entry_pass = tk.Entry(self, show='*')
        self.entry_pass.place(x=200, y=80)

        btn_signin = tk.Button(self, text='Войти')
        btn_signin.place(x=200, y=170)
        btn_signin.bind('<Button-1>', self.submit)

    def submit(self, event):
        self.parent.connect(self.entry_login.get(), self.entry_pass.get())
        self.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    app.pack()
    root.title('Т Е С Т')
    root.geometry("800x600+100+100")
    root.mainloop()
