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
        # variable for user input
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        input_frame = ttk.Frame(self)
        input_frame.pack()
        
        ttk.Label(input_frame, text='Username').pack(ipadx=130)
        ttk.Entry(input_frame, width=40, textvariable=self.username).pack(pady=5)
        
        ttk.Label(input_frame, text='Password').pack(ipadx=135)
        ttk.Entry(input_frame, width=40,show='*', textvariable=self.password).pack(pady=5)
        
        ttk.Button(input_frame, text='send', width=10, command= lambda: self.submit_login(self.username.get(), self.password.get())).pack(pady=15)
        
    def submit_login(self, username, password):
        # get data from database
        # check if username is valid 
        # check if username is admin or not
        # check password
        print(f'username: {username}, password : {password}')
    
    # get the middle of possition for the window
    def middle_cordinate(self,window_width, window_height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        # // to get integer output so it's valid for geometry size
        x = (screen_w - window_width) //2
        y = (screen_h - window_height)//2
        
        return f'{window_width}x{window_height}+{x}+{y}'
    
        


login = Login()


