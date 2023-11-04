import tkinter as tk
import tkinter.messagebox as mb
from typing import Any
import ttkbootstrap as ttk
import mysql.connector
import os
import dotenv
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

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
    
    def login_menu(self) -> None:
        login_menu = ttk.Toplevel(self)
        login_menu.title('Login')
        login_menu.geometry(self.middle_cordinate(window_width=600,window_height=500))
        
        ttk.Frame(login_menu).pack(side='top', expand=True)
        self.login_input_field(master=login_menu)
        ttk.Frame(login_menu).pack(side='bottom', expand='True')
        
        login_menu.protocol("WM_DELETE_WINDOW", lambda : self.destroy())
      
    def main_menu(self, temp) -> None:
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
        self.transaction_table(main_frame)
        
        
        
        main_menu.protocol("WM_DELETE_WINDOW", lambda : self.destroy())

    def add_product(self) -> None:
        name = 'test'
        price = 9000
        qty = 8
        total = int(price) * int(qty)
        id = self.table_len + 1
        self.transaction_table.insert(parent='', index=self.table_len, iid=id, text='', values=(id, name, price, qty, total))    
        self.table_len += 1
                
            
    def logout(self, close_window : ttk) -> None:
        close_window.destroy()
        self.login_menu()
    
    def login_input_field(self, master) -> None:
        
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
        
    def submit_login(self, master, username, password) -> None:
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
    def fullscreen_size(self) -> str:
        width = self.winfo_screenwidth()
        height =  self.winfo_screenheight()
        return f'{width}x{height}'
        
    # get the middle of possition for the window
    def middle_cordinate(self,window_width, window_height) -> str:
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        # to get integer output so it's valid for geometry size
        x = (screen_w - window_width) //2
        y = (screen_h - window_height)//2
        
        return f'{window_width}x{window_height}+{x}+{y}'
    
    # Component section
    def transaction_menu(self, master) -> None:
        # add button position top right
        add_product = ttk.Frame(master)
        ttk.Button(add_product, text='Add Product +', command=lambda : self.add_product_menu()).pack(side='right')
        add_product.pack(side='top', fill='both')
    
    def transaction_table(self, master) -> None:
        transaction_frame = ttk.Frame(master)
        self.transaction_table = ttk.Treeview(transaction_frame, columns=('id', 'name', 'price', 'qty', 'total'))
        self.transaction_table.column('#0', width=0, stretch='no')
        self.transaction_table.column('id', width=100, anchor='center')
        self.transaction_table.column('name', width=200, anchor='center')
        self.transaction_table.column('price', width=100, anchor='center')
        self.transaction_table.column('qty', width=100, anchor='center')
        self.transaction_table.column('total', width=100, anchor='center')
        
        # setup heading
        self.transaction_table.heading('#0', text='', anchor='center')
        self.transaction_table.heading('id', text='ID', anchor='center')
        self.transaction_table.heading('name', text='Name', anchor='center')
        self.transaction_table.heading('price', text='Price', anchor='center')
        self.transaction_table.heading('qty', text='Qty', anchor='center')
        self.transaction_table.heading('total', text='Total', anchor='center')
        
        self.table_len = 0
        
        self.transaction_table.pack(side='left', expand=True, fill='both')
        transaction_frame.pack(side='top', expand=True, fill='both')
    
    def add_product_menu(self) -> None:
        self.search_item = tk.StringVar()
        menu = ttk.Toplevel(self)
        menu.title('Add Product')
        menu.geometry(self.middle_cordinate(600,500))
        
        # search product
        search_frame = ttk.Frame(menu)
        search_frame.pack(side='top', fill='both')
        search_input = ttk.Entry(search_frame, width=60, textvariable=self.search_item)
        search_input.bind('<Any-KeyRelease>', lambda event : self.search_product(self.search_item.get()))
        search_input.pack(side='top', pady=5)
        
        # table product (id,name,price)
        search_table = ttk.Treeview(search_frame, columns=('id', 'name', 'price'))
        search_table.column('#0', width=0, stretch='no')
        search_table.column('id', width=100, anchor='center')
        search_table.column('name', width=200, anchor='center')
        search_table.column('price', width=100, anchor='center')
        
        search_table.heading('#0', text='', anchor='center')
        search_table.heading('id', text='ID', anchor='center')
        search_table.heading('name', text='Name', anchor='center')
        search_table.heading('price', text='Price', anchor='center')
        
        search_table.pack(side='top', expand=True, fill='both')
        
        
        menu.protocol("WM_DELETE_WINDOW", lambda : menu.destroy())
     
    def search_product(self, input : str) -> None:
        print(input)
    
    # Database section
    # get data from database
    def get_data(self, query : list) -> MySQLCursor:
        mydb_cursor = self.mydb.cursor()
        mydb_cursor.execute(query)
        return  mydb_cursor.fetchall()
    
    # setup mysql connector
    def connect_db(self) -> (MySQLConnection | PooledMySQLConnection):
        return mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME'), 
    )
        
        
app = App()
