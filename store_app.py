import tkinter as tk
import tkinter.messagebox as mb
import ttkbootstrap as ttk
import mysql.connector
import os
import dotenv

dotenv.load_dotenv()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.mydb = self.connect_db()
        
        # hide root window
        self.withdraw()
        
        # calling login menu
        self.login_menu()
        
        self.mainloop()
    
    def login_menu(self):
        login_menu = ttk.Toplevel(self)
        login_menu.title('Login')
        login_menu.geometry(self.middle_cordinate(window_width=600,window_height=500))
        
        ttk.Frame(login_menu).pack(side='top', expand=True)
        self.login_input_field(master=login_menu)
        ttk.Frame(login_menu).pack(side='bottom', expand='True')
        
        login_menu.protocol("WM_DELETE_WINDOW", lambda : self.destroy())
      
    def main_menu(self, temp):
        temp.destroy()
        
        # create main menu
        main_menu = ttk.Toplevel(self)
        main_menu.title('Menu')              
        main_menu.geometry(self.fullscreen_size())
        left_frame = ttk.Frame(main_menu, bootstyle="secondary")
        left_frame.pack(side='left', fill='both')
        ttk.Button(left_frame, text='Transaction').pack(pady=5,side='top')
        ttk.Button(left_frame, text='Show Product').pack(pady=5,side='top')
        
        ttk.Frame(left_frame, bootstyle="secondary" ).pack(expand=True, fill='both')
        ttk.Button(left_frame, text='Logout', command=lambda: self.logout(main_menu)).pack(pady=5,side='bottom')
    
        main_frame = ttk.Frame(main_menu, bootstyle="danger")
        main_frame.pack(side='right', expand=True, fill='both')
        
        
        self.transaction_menu(main_frame)
        main_menu.protocol("WM_DELETE_WINDOW", lambda : self.destroy())

    def logout(self, close_window : ttk):
        close_window.destroy()
        self.login_menu()
    
    
    def login_input_field(self, master):
        # variable for user input
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        input_frame = ttk.Frame(master)
        input_frame.pack()
        
        ttk.Label(input_frame, text='Username').pack(ipadx=130)
        ttk.Entry(input_frame, width=40, textvariable=self.username).pack(pady=5)
        
        ttk.Label(input_frame, text='Password').pack(ipadx=135)
        ttk.Entry(input_frame, width=40,show='*', textvariable=self.password).pack(pady=5)
        
        ttk.Button(input_frame, text='send', width=10, command= lambda: self.submit_login(master, self.username.get(), self.password.get())).pack(pady=15)
        
    def submit_login(self, master, username, password):
        # get data from database
        query = f'SELECT * FROM users WHERE username = "{username}"'
        user_data = self.get_data(query)
        
        # check if username is valid 
        if len(user_data) == 0 : 
            return mb.showerror('Login failed', 'username not found')
        user_data = list(user_data[0])
        
        # check password
        if password != user_data[2] :
            return mb.showerror('Login failed', 'password does not match')
        mb.showinfo('Login status', 'successfully login')
        
        # check if username is admin or not
        print('Menu Admin') if (user_data[3] == 1) else self.main_menu(master)
    
    # get full screen size window
    def fullscreen_size(self):
        width = self.winfo_screenwidth()
        height =  self.winfo_screenheight()
        return f'{width}x{height}'
        
    # get the middle of possition for the window
    def middle_cordinate(self,window_width, window_height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        # to get integer output so it's valid for geometry size
        x = (screen_w - window_width) //2
        y = (screen_h - window_height)//2
        
        return f'{window_width}x{window_height}+{x}+{y}'
    
    # Component section
    def transaction_menu(self, master):
        # add button position top right
        add_product = ttk.Frame(master)
        ttk.Button(add_product, text='Add Product +').pack(side='right')
        add_product.pack(side='top', fill='both')
        
        
    
    # Database section
    # get data from database
    def get_data(self, query : list):
        mydb_cursor = self.mydb.cursor()
        mydb_cursor.execute(query)
        return  mydb_cursor.fetchall()
    
    # setup mysql connector
    def connect_db(self):
        return mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME'), 
    )
        
        
app = App()
