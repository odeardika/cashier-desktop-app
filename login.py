import tkinter as tk
import ttkbootstrap as ttk

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Login')
        self.geometry(self.middle_cordinate(window_width=600,window_height=500))
        
        ttk.Frame(self).pack(side='top', expand=True)
        self.input_field()
        ttk.Frame(self).pack(side='bottom', expand='True')
        self.mainloop()
        
    def input_field(self):
        input_frame = ttk.Frame(self)
        input_frame.pack()
        
        username_label = ttk.Label(input_frame, text='Username')
        username_label.pack(ipadx=130)
        username_input = ttk.Entry(input_frame, width=40)
        username_input.pack(pady=5)
        username_label = ttk.Label(input_frame, text='Password')
        username_label.pack(ipadx=135)
        password_input = ttk.Entry(input_frame, width=40)
        password_input.pack(pady=5)
        button = ttk.Button(input_frame, text='send', width=10)
        button.pack(pady=15)
    
    # get the middle of possition for the window
    def middle_cordinate(self,window_width, window_height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        # // to get integer output so it's valid for geometry size
        x = (screen_w - window_width) //2
        y = (screen_h - window_height)//2
        
        return f'{window_width}x{window_height}+{x}+{y}'
    
        


login = Login()


