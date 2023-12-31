import tkinter as tk
import tkinter.messagebox as mb
# from typing import Any
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
    
    def login_menu(self):
        login_menu = ttk.Toplevel(self)
        login_menu.title('Login')
        login_menu.geometry(self.middle_cordinate(window_width=600,window_height=500))
        
        ttk.Frame(login_menu).pack(side='top', expand=True)
        self.login_input_field(master=login_menu)
        ttk.Frame(login_menu).pack(side='bottom', expand='True')
        
        login_menu.protocol("WM_DELETE_WINDOW", lambda : self.destroy())
    
    #admin menu
    def admin_menu(self, temp):
        temp.destroy()
        self.search_item = tk.StringVar()
        
        menu = ttk.Toplevel(self)
        menu.title('Menu')
        menu.state('zoomed')
        
        # side navbar
        left_frame = ttk.Frame(menu, bootstyle="secondary")
        left_frame.pack(side='left', fill='both')
        ttk.Button(left_frame, text='Product', width=20).pack(padx=5, pady=5,side='top')
        ttk.Button(left_frame, text='Transaction', width=20).pack(padx=5, pady=5,side='top')
        ttk.Button(left_frame, text='User', width=20).pack(padx=5, pady=5,side='top')
        
        # main menu
        search_bar = ttk.Frame(menu)
        search_bar.pack(side='top',fill='both')
        main_frame = ttk.Frame(menu)
        main_frame.pack(fill='both',expand=True)
        ttk.Frame(search_bar).pack(side='left',fill='both',expand=True)
        search_input = ttk.Entry(search_bar, width=100, textvariable=self.search_item)
        search_input.bind('<Any-KeyRelease>', lambda event : self.search_product(self.search_item.get(), product_table))
        search_input.pack(side='left', pady=5)
        ttk.Frame(search_bar).pack(side='left',fill='both',expand=True)
        ttk.Button(search_bar,text='Add Product +', command= lambda : self.add_new_product_menu()).pack(side='left',padx=5)
        
        product_table = ttk.Treeview(main_frame, columns=('id', 'name', 'price'))
        product_table.column('#0', width=0, stretch='no')
        product_table.column('id', width=100, anchor='center')
        product_table.column('name', width=200, anchor='center')
        product_table.column('price', width=100, anchor='center')
        
        product_table.heading('#0', text='', anchor='center')
        product_table.heading('id', text='ID', anchor='center')
        product_table.heading('name', text='Name', anchor='center')
        product_table.heading('price', text='Price', anchor='center')
        
        product_table.pack(fill='both',expand=True)
        product_table.bind('<<TreeviewSelect>>', lambda event : self.edit_product(product_table, self.search_item.get()))
        
        ttk.Button(left_frame, text='Logout', width=20, command=lambda: self.logout(menu)).pack(pady=5,side='bottom')
        menu.protocol("WM_DELETE_WINDOW", lambda : self.destroy())
    
    def add_new_product_menu(self):
        #setting up the window
        self.product_name = tk.StringVar()
        self.product_price = tk.IntVar()
        menu = ttk.Toplevel(self)
        menu.title('Add Product')
        menu.geometry(self.middle_cordinate(600,500))
        
        # add the widget to the window
        ttk.Label(menu,text='Product Name : ').pack()
        ttk.Entry(menu,textvariable=self.product_name).pack()
        ttk.Label(menu,text='Product Price').pack()
        ttk.Entry(menu,textvariable=self.product_price).pack()
        ttk.Button(menu,text='Save',command=lambda:self.add_new_product(self.product_name.get(),self.product_price.get(),menu)).pack(pady=5)
        
    def add_new_product(self,name,price,menu):
        self.mydb.cursor().execute(f"INSERT INTO products (product_name,product_price) VALUES (%s,%s)",(name,price))
        self.mydb.commit()
        menu.destroy()
    
    def edit_product(self, table : ttk.Treeview, search_input : str):
        # remove error output that not effect the app
        try:
            # get selected product data
            product = table.selection()[0]
            product = table.item(product)['values']
            id, name, price = product
            
            #edit product menu
            self.product_name = tk.StringVar(value=name)
            self.product_price = tk.IntVar(value=price)
            menu = ttk.Toplevel(self)
            menu.title('Edit Product')
            menu.geometry(self.middle_cordinate(600,500))
            
            ttk.Label(menu,text='Product Name : ').pack()
            ttk.Entry(menu,textvariable=self.product_name).pack()
            ttk.Label(menu,text='Product Price').pack()
            ttk.Entry(menu,textvariable=self.product_price).pack()
            
            ttk.Button(menu,text='Save',command=lambda:self.save_edit_product(id,self.product_name.get(),self.product_price.get(),menu,table,search_input)).pack(pady=5)
        except IndexError:
            pass
        
    def save_edit_product(self, id , name , price, prev_menu,table,search_input):
        # save the update data
        self.mydb.cursor().execute(f'UPDATE products SET product_name = %s, product_price = %s WHERE id = %s', (name,price,id))
        self.mydb.commit()
        
        # close update menu
        prev_menu.destroy()
        
        self.search_product(search_input,table)
        
     
    # main menu  
    def main_menu(self, temp):
        temp.destroy()
        self.total_trasaction = tk.IntVar(value=0)
        self.temp_transaction = []
        
        # create main menu
        main_menu = ttk.Toplevel(self)
        main_menu.title('Menu')              
        main_menu.state('zoomed')
        left_frame = ttk.Frame(main_menu, bootstyle="secondary")
        left_frame.pack(side='left', fill='both')
        ttk.Button(left_frame, text='Transaction',width=20).pack(pady=5,padx=5,side='top')
        ttk.Button(left_frame, text='Show Product',width=20).pack(pady=5,side='top')
        
        ttk.Frame(left_frame, bootstyle="secondary" ).pack(expand=True, fill='both')
        ttk.Button(left_frame, text='Logout',width=20, command=lambda: self.logout(main_menu)).pack(pady=5,side='bottom')
    
        main_frame = ttk.Frame(main_menu, bootstyle="danger")
        main_frame.pack(side='right', expand=True, fill='both')
        
        self.transaction_menu(main_frame)
        self.transaction_table(main_frame)
        
        ttk.Button(main_frame, text='Checkout', command=lambda : self.checkout_transaction()).pack(side='right', pady=5, padx=5)
        ttk.Entry(main_frame, textvariable=self.total_trasaction, state='readonly').pack(side='right', pady=5, padx=5)
        
        main_menu.protocol("WM_DELETE_WINDOW", lambda : self.destroy())

    def checkout_transaction(self):
        menu = ttk.Toplevel(self)
        menu.title('Transaction')
        menu.geometry(self.middle_cordinate(600,500))
        
        table_frame = ttk.Frame(menu)
        table = ttk.Treeview(table_frame,columns=('id', 'name', 'price', 'qty', 'total'))
        table.column('#0', width=0, stretch='no')
        table.column('id', width=100, anchor='center')
        table.column('name', width=200, anchor='center')
        table.column('price', width=100, anchor='center')
        table.column('qty', width=100, anchor='center')
        table.column('total', width=100, anchor='center')
        
        # setup heading
        table.heading('#0', text='', anchor='center')
        table.heading('id', text='ID', anchor='center')
        table.heading('name', text='Name', anchor='center')
        table.heading('price', text='Price', anchor='center')
        table.heading('qty', text='Qty', anchor='center')
        table.heading('total', text='Total', anchor='center')
        
        table.pack()
        
        #insert product in current transaction
        for product in self.temp_transaction:
            table.insert(parent='', index=0, iid=product['id'], text='', values=(product['id'], product['name'], product['price'],product['qty'],product['total']))
        
        table_frame.pack()
        
        total_trasaction_frame = ttk.Frame(menu)
        total_trasaction_frame.pack(fill='x')
        ttk.Entry(total_trasaction_frame, textvariable=self.total_trasaction, state='readonly', width=10).pack(side='right',padx=3,pady=5)
        ttk.Label(total_trasaction_frame, text='Total ').pack(side='right',padx=12)
        
        bottom_frame = ttk.Frame(menu)
        bottom_frame.pack(side='bottom')
        
        
        confirm_frame = ttk.Frame(bottom_frame)
        confirm_frame.pack(side='bottom', fill='x')
        ttk.Button(confirm_frame, text='Confirm Transaction', command=lambda:self.confirm_checkout(menu)).pack(pady=5)
    
    def confirm_checkout(self, menu) :
        menu.destroy()
        # save transaction to table transactions table
        self.mydb.cursor().execute(f'INSERT INTO transactions (transaction_total,product_type_total) VALUES (%s,%s)',(self.total_trasaction.get(),len(self.temp_transaction)))
        self.mydb.commit()
        
        # save product in the transaction into product_transactions table
        for product in self.temp_transaction:
            product_id = product['id']
            transaction_id = list(self.get_data(f'SELECT MAX(id) FROM transactions')[0])[0]
            product_quantity = product['qty']
            bill = product['total']
            self.mydb.cursor().execute(f'INSERT INTO product_transactions (product_id,transaction_id,product_quantity,product_bill) VALUES (%s,%s,%s,%s)',(product_id,transaction_id,product_quantity,bill))
            self.mydb.commit() 
        
        # clear the current tramsaction
        for i in self.product_table.get_children():
            self.product_table.delete(i)
        self.total_trasaction.set(0)
        self.temp_transaction = []
    
    def add_product(self, prev_menu, product, qty) :
        try:
            id, name, price = product['id'], product['name'], product['price']
            total = int(price) * int(qty)
            table_id = self.table_len + 1
            self.product_table.insert(parent='', index=self.table_len, iid=id, text='', values=(table_id, name, price, qty, total))    
            self.table_len += 1
            self.total_trasaction.set(self.total_trasaction.get() + total)   
            self.temp_transaction.append({
                'id' : id,
                'name' : name,
                'price' : price,
                'qty' : qty,
                'total' : total
            })             
            prev_menu.destroy()
        except ValueError:
            pass 
          
    def logout(self, close_window : ttk) :
        close_window.destroy()
        self.login_menu()
    
    def login_input_field(self, master) :
        
        # variable for user input
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        input_frame = ttk.Frame(master)
        input_frame.pack()
        
        ttk.Label(input_frame, text='Username').pack(ipadx=130)
        username_entry = ttk.Entry(input_frame, width=40, textvariable=self.username)
        username_entry.bind('<KeyPress-Return>',lambda event: self.submit_login(master, self.username.get(), self.password.get()))
        username_entry.pack(pady=5)
        
        ttk.Label(input_frame, text='Password').pack(ipadx=135)
        password_entry = ttk.Entry(input_frame, width=40,show='*', textvariable=self.password)
        password_entry.bind('<KeyPress-Return>',lambda event: self.submit_login(master, self.username.get(), self.password.get()))
        password_entry.pack(pady=5)
        
        login_button = ttk.Button(input_frame, text='Login', width=10, command= lambda: self.submit_login(master, self.username.get(), self.password.get()))
        login_button.bind('<KeyPress-Return>',lambda event: self.submit_login(master, self.username.get(), self.password.get()))
        login_button.pack(pady=15)
        
    def submit_login(self, master, username, password) :
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
        self.admin_menu(master) if (user_data[3] == 1) else self.main_menu(master)
        
    # get the middle of possition for the window
    def middle_cordinate(self,window_width, window_height) :
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        # to get integer output so it's valid for geometry size
        x = (screen_w - window_width) //2
        y = (screen_h - window_height)//2
        
        return f'{window_width}x{window_height}+{x}+{y}'
    
    # Component section
    def transaction_menu(self, master) :
        # add button position top right
        add_product = ttk.Frame(master)
        ttk.Button(add_product, text='Add Product +', command=lambda : self.add_product_menu()).pack(side='right', padx=5,pady=5)
        add_product.pack(side='top', fill='both')
    
    def transaction_table(self, master) :
        transaction_frame = ttk.Frame(master)
        self.product_table = ttk.Treeview(transaction_frame, columns=('id', 'name', 'price', 'qty', 'total'))
        self.product_table.column('#0', width=0, stretch='no')
        self.product_table.column('id', width=100, anchor='center')
        self.product_table.column('name', width=200, anchor='center')
        self.product_table.column('price', width=100, anchor='center')
        self.product_table.column('qty', width=100, anchor='center')
        self.product_table.column('total', width=100, anchor='center')
        
        # setup heading
        self.product_table.heading('#0', text='', anchor='center')
        self.product_table.heading('id', text='ID', anchor='center')
        self.product_table.heading('name', text='Name', anchor='center')
        self.product_table.heading('price', text='Price', anchor='center')
        self.product_table.heading('qty', text='Qty', anchor='center')
        self.product_table.heading('total', text='Total', anchor='center')
        
        self.table_len = 0
        
        self.product_table.pack(side='left', expand=True, fill='both')
        transaction_frame.pack(side='top', expand=True, fill='both')
    
    def add_product_menu(self) :
        self.search_item = tk.StringVar()
        menu = ttk.Toplevel(self)
        menu.title('Add Product')
        menu.geometry(self.middle_cordinate(600,500))
        
        # search product
        search_frame = ttk.Frame(menu)
        search_frame.pack(side='top', fill='both')
        search_input = ttk.Entry(search_frame, width=60, textvariable=self.search_item)
        search_input.bind('<Any-KeyRelease>', lambda event : self.search_product(self.search_item.get(), selected_product))
        search_input.pack(side='top', pady=5)
        
        # table product (id,name,price)
        selected_product = ttk.Treeview(search_frame, columns=('id', 'name', 'price'))
        selected_product.column('#0', width=0, stretch='no')
        selected_product.column('id', width=100, anchor='center')
        selected_product.column('name', width=200, anchor='center')
        selected_product.column('price', width=100, anchor='center')
        
        selected_product.heading('#0', text='', anchor='center')
        selected_product.heading('id', text='ID', anchor='center')
        selected_product.heading('name', text='Name', anchor='center')
        selected_product.heading('price', text='Price', anchor='center')
        
        selected_product.pack(side='top', expand=True, fill='both')
        selected_product.bind('<<TreeviewSelect>>', lambda event : self.select_product(selected_product, menu))
        
        menu.protocol("WM_DELETE_WINDOW", lambda : menu.destroy())

    def select_product(self, table : ttk.Treeview, master : ttk.Toplevel) :
        # get selected product
        product = table.selection()[0]
        product = table.item(product)['values']
        id, name, price = product
        product = {
            'id' : id,
            'name' : name,
            'price' : price
        }
        self.add_product_to_table(master ,product)
            
    
    def add_product_to_table(self, prev_menu : ttk.Toplevel , product : dict) :
        prev_menu.destroy()
        quantity = tk.StringVar()
        menu = ttk.Toplevel(self) 
        menu.title('Add Product')
        menu.geometry(self.middle_cordinate(600,500))
        id, name, price = product['id'], product['name'], product['price']
        ttk.Label(menu, text=f'{id}').pack(pady=5)
        ttk.Label(menu, text=f'{name}').pack(pady=5)
        ttk.Label(menu, text=f'{price}').pack(pady=5)
        
        ttk.Label(menu, text='Quantity').pack(pady=5)
        ttk.Entry(menu, width=60, textvariable=quantity).pack(pady=5)
        
        ttk.Button(menu, text='Add', command=lambda : self.add_product(menu,product,quantity.get())).pack(pady=5)
        
        menu.protocol("WM_DELETE_WINDOW", lambda : menu.destroy())
           
     
    def search_product(self, input : str, table : ttk.Treeview) :
        
        # sql query to search product using regex in mysql
        sql = f'SELECT * FROM products WHERE product_name REGEXP "{input}"'
        
        # clear table
        for row in table.get_children():
            table.delete(row)
            
        
        # list tuple to list dictonary
        list_product = []
        try:
            for product in self.get_data(sql):
                list_product.append({
                    'id' : product[0],
                    'name' : product[1],
                    'price' : product[2]
                })
        except mysql.connector.errors.DatabaseError:
            # error when input not found in database
            pass
        
        # insert new search result
        for product in list_product:
            table.insert(parent='', index=0, iid=product['id'], text='', values=(product['id'], product['name'], product['price']))

    
    # Database section
    # get data from database
    def get_data(self, query : str) :
        mydb_cursor = self.mydb.cursor()
        mydb_cursor.execute(query)
        return  mydb_cursor.fetchall()
    
    # send data to database
    def send_data(self, query : str): 
        self.mydb.cursor().execute(query)
    
    # setup mysql connector
    def connect_db(self) :
        return mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME'), 
    )
    
        
        
app = App()
