import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        btn_edit_dialog = tk.Button(self, text='Тест', bg='#ffffff', bd=2, command=self.destroy)
        btn_edit_dialog.pack()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    app.pack()
    root.title('Т Е С Т')
    root.geometry("800x600+100+100")
    root.mainloop()
