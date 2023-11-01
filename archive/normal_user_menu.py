import tkinter as tk
import ttkbootstrap as ttk
import archive.login as login

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Menu')
        self.attributes('-fullscreen',True)
        
        ttk.Button(self, text='Logout', command=lambda: self.close()).pack()
        self.mainloop()
    
    def close(self):
        self.close()
        temp = login.Login()
menu = Menu()