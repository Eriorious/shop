import tkinter
import sqlite3
import datetime
global product
# ----------------- create users table -------------

cnt=sqlite3.Connection("myshop.db")
##print("connect to database")
##
##query="""CREATE TABLE users
##   ( ID INTEGER PRIMARY KEY,
##   user CHAR(20) NOT NULL,
##  pass CHAR(20) NOT NULL,
##  addr CHAR(50) NOT NULL,
##  ordered int NOT NULL )"""
##cnt.execute(query)
##cnt.close()

 #------------------create product table --------------
##query="""CREATE TABLE products
##   ( ID INTEGER PRIMARY KEY,
##   name CHAR(20) NOT NULL,
##   price int NOT NULL,
##   qnt int NOT NULL,
##   ordered int NOT NULL,
##   date CHAR(10) NOT NULL,
##   comment TEXT )"""
##cnt.execute(query)
##cnt.close()

#----------------- init products table -------------
##query="""INSERT INTO products (name,price,qnt,ordered,date)
##VALUES ('hat',100,20, 0 ,' ') """
##cnt.execute(query)
##cnt.commit()
####cnt.close()     
##
#####----------------- init users table -------------
##query="""INSERT INTO users (user,pass,addr,ordered)
##      VALUES ('erisa','123456789','london',0) """
##cnt.execute(query)
##cnt.commit()
##cnt.close()     

# ----------------- functions ----------------


def login():
    user=user_txt.get()
    pas=pas_txt.get()
    
    if user=="" or pas=="":  # if len(user)==0 or len(pas)==0
        msg_lbl.configure(text="please fill the blanks!",fg="red")
        return
    
    query='''SELECT * from users WHERE user=? AND pass=?'''
    result=cnt.execute(query,(user,pas))
    rows=result.fetchall()
    if len(rows)==0:
        msg_lbl.configure(text="wrong username or pass",fg="red")
        return
    else:
        msg_lbl.configure(text="welcome to your account",fg="green")
        user_txt.delete(0,"end")
        pas_txt.delete(0,"end")
        if user=="admin":
            AdminPanel_btn.configure(state="active")
        login_btn.configure(state="disabled")
        logout_btn.configure(state="active")
        shop_btn.configure(state="active")


def logout():
    AdminPanel_btn.configure(state="disabled")
    login_btn.configure(state="active")
    logout_btn.configure(state="disabled")
    shop_btn.configure(state="disabled")
    msg_lbl.configure(text="you are logged out!",fg="green")

def final_submit():
    user=user1_txt.get()
    pas=pas1_txt.get()
    addr=addr1_txt.get()
    
    # -------------------- validation -----------------
    
    if user=="" or pas=="" or addr=="" :
        msg1_lbl.configure(text="fill all the blanks!",fg="red")
        return
    
    if len(pas)<8:
        msg1_lbl.configure(text="pass length error!",fg="red")
        return
    
    query='''SELECT id FROM users WHERE user=?'''
    result=cnt.execute(query,(user,))
    rows=result.fetchall()
    if len(rows)!=0:
        msg1_lbl.configure(text="username already exist!",fg="red")
        return
    
    query='''INSERT INTO users (user,pass,addr)
           VALUES (?,?,?) '''
    cnt.execute(query,(user,pas,addr))
    cnt.commit()
    msg1_lbl.configure(text="submit done successfully!",fg="green")
    user1_txt.delete(0,"end")
    pas1_txt.delete(0,"end")  
    addr1_txt.delete(0,"end")      
    

def submit():
    global user1_txt,pas1_txt,addr1_txt,msg1_lbl
    win_submit=tkinter.Toplevel(win)
    win_submit.title("Submit")
    win_submit.geometry("200x200")
    
    # ---------------------- widgets ---------------------
    user1_lbl=tkinter.Label(win_submit,text="username: ")
    user1_lbl.pack()

    user1_txt=tkinter.Entry(win_submit,width=20)
    user1_txt.pack()

    pas1_lbl=tkinter.Label(win_submit,text="password: ")
    pas1_lbl.pack()

    pas1_txt=tkinter.Entry(win_submit,width=20)
    pas1_txt.pack()
    
    addr1_lbl=tkinter.Label(win_submit,text="address: ")
    addr1_lbl.pack()

    addr1_txt=tkinter.Entry(win_submit,width=20)
    addr1_txt.pack()

    msg1_lbl=tkinter.Label(win_submit,text="")
    msg1_lbl.pack()

    login1_btn=tkinter.Button(win_submit,text=" submit now! ",command=final_submit)
    login1_btn.pack()
    
    
    # ----------------------------------------------------
    win_submit.mainloop()

def shop():

    win_shop=tkinter.Toplevel(win)
    win_shop.title("shop")
    win_shop.geometry("400x400")
    lstbox=tkinter.Listbox(win_shop,width=40)
    lstbox.pack()

    query='''SELECT * FROM products '''
    result=cnt.execute(query,)
    rows=result.fetchall()
    
    for products in rows:
        # mystr=str(products[0])+" "+product[1]+" "+str(product[2])
        mystr=f"id: {products[0]}  name: {products[1]}  price: {products[2]}  qnt: {products[3]} ordered:{products[4]}  "
        lstbox.insert(0, mystr)
    prdct_lbl=tkinter.Label(win_shop,text=" pruduct id :  ")
    prdct_lbl.pack()
    prdct_txt=tkinter.Entry(win_shop,width=20)
    product=prdct_txt.get()
    order_btn=tkinter.Button(win_shop,text=" buy ",command=order(product))
    prdct_txt.pack()
    order_btn.pack()
    if len(product)!=0:
        msg2_lbl=tkinter.Label(win_shop,text="added to your list")
        msg2_lbl.pack()
    win_shop.mainloop()
    print(product) 
    
# -------------------admin_panel--------------------------
def info():
    win_info=tkinter.Toplevel(win)
    win_info.title("report")
    win_info.geometry("500x400")
    users_btn=tkinter.Button(win_info,text="users",command=userslist)
    users_btn.pack()

    product_btn=tkinter.Button(win_info,text="products",command=productslist)
    product_btn.pack()

    OutOfStock_btn=tkinter.Button(win_info,text="out of stock",command=outofstock)
    OutOfStock_btn.pack()

    BestSeller_btn=tkinter.Button(win_info,text="best seller",command=bestseller)
    BestSeller_btn.pack()

    WorstSeller_btn=tkinter.Button(win_info,text="worst seller",command=worstseller)
    WorstSeller_btn.pack()

    date_btn=tkinter.Button(win_info,text=" date ",command=date)
    date_btn.pack()

    BestCostumer_btn=tkinter.Button(win_info,text="best costumer ",command=bestcostumer)
    BestCostumer_btn.pack()

#-----------------------------info_functions----------------------
def userslist():
    win_users=tkinter.Toplevel(win)
    win_users.title("users")
    win_users.geometry("400x400")
    userbox=tkinter.Listbox(win_users,width=100,height=50)
    userbox.pack()
    
    query = '''SELECT user FROM users '''
    result=cnt.execute(query,)
    rows=result.fetchall()
    for users in rows :
        userbox.insert(0,users)
    win_users.mainloop()
    
def productslist():
    win_product=tkinter.Toplevel(win)
    win_product.title("product")
    win_product.geometry("400x400")
    ProductBox=tkinter.Listbox(win_product,width=100,height=50)
    ProductBox.pack()
    
    query = '''SELECT name FROM products '''
    result=cnt.execute(query,)
    rows=result.fetchall()
    for products in rows :
        ProductBox.insert(0,products)
    win_product.mainloop()
    
def outofstock():
    win_outofstock=tkinter.Toplevel(win)
    win_outofstock.title("out of stock")
    win_outofstock.geometry("400x400")
    OutOfStockBox=tkinter.Listbox(win_outofstock,width=100,height=50)
    OutOfStockBox.pack()
    
    query = '''SELECT name FROM products WHERE qnt=0 '''
    result=cnt.execute(query,)
    rows=result.fetchall()
    for outofstock in rows :
        OutOfStockBox.insert(0,outofstock)
    win_outofstock.mainloop()

def bestseller():
    win_bestseller=tkinter.Toplevel(win)
    win_bestseller.title("best seller")
    win_bestseller.geometry("400x400")
    BestSellerBox=tkinter.Listbox(win_bestseller,width=100,height=50)
    BestSellerBox.pack()
    query=''' SELECT name FROM products ORDER BY ordered'''
    result=cnt.execute(query,)
    rows=result.fetchall()
    bestseller=rows[0]
    BestSellerBox.insert(0,bestseller)
    win_bestseller.mainloop()
def worstseller():
    win_worstseller=tkinter.Toplevel(win)
    win_worstseller.title("worst seller")
    win_worstseller.geometry("400x400")
    WorstSellerBox=tkinter.Listbox(win_worstseller,width=100,height=50)
    WorstSellerBox.pack()
    query=''' SELECT name FROM products ORDER BY ordered DESC'''
    result=cnt.execute(query,)
    rows=result.fetchall()
    worstseller=rows[0]
    WorstSellerBox.insert(0,worstseller)
    win_worstseller.mainloop()
def date():
    global daydate
    win_date=tkinter.Toplevel(win)
    win_date.title("date:" )
    win_date.geometry("400x400")
    date_lbl=tkinter.Label(win_date,text="date :")
    date_lbl.pack()
    date_txt=tkinter.Entry(win_date,width=20)
    date_txt.pack()
    daydate=date_txt.get()
    date_btn=tkinter.Button(win_date,text=" done ",command=showdate)
    date_btn.pack()
    win_date.mainloop()
def showdate():
    win_date=tkinter.Toplevel(win)
    win_date.title("products" )
    win_date.geometry("400x400")
    query = '''SELECT name FROM products WHERE date= ? '''
    result=cnt.execute(query,(date,))
    rows=result.fetchall()
    datebox=tkinter.Listbox(win_date,width=100,height=50)
    datebox.pack()
    for product1 in rows :
         datebox.insert(0,product1)
    win_date.mainloop()
def bestcostumer():
    win_bestcostumer=tkinter.Toplevel(win)
    win_bestcostumer.title("best costumer" )
    win_bestcostumer.geometry("400x400")
    BestCostumerBox=tkinter.Listbox(win_bestcostumer,width=100,height=50)
    BestCostumerBox.pack()
    query=''' SELECT user FROM users ORDER BY ordered'''
    result=cnt.execute(query,)
    rows=result.fetchall()
    user=rows[0]
    BestCostumerBox.insert(0,user)
    win_bestcostumer.mainloop()
    
def order(prdct):
    pass
    product=prdct
    #decreasing quantity of product
    query=''' SELECT qnt FROM products WHERE id=?'''
    result=cnt.execute(query,(product,))
    rows=result.fetchall()
    newqnt1=rows[0]
    newqnt=int(newqnt1[0])
    query=''' UPDATE products SET qnt=? WHERE id=?'''
    cnt.execute(query,(newqnt,product))
    cnt.commit()
    ##adding to ordered product
    query=''' SELECT ordered FROM products WHERE id=?'''
    result=cnt.execute(query,(product,))
    rows=result.fetchall()
    rows1=rows[0]
    rows2=int(rows1[0])
    product_order=rows2+1
    query='''UPDATE  products SET ordered=? where id=?'''
    cnt.execute(query,(product_order,product))
    cnt.commit()
    ##adding order to costumers list
    query=''' select ordered from users WHERE id=?'''
    result=cnt.execute(query,(product,))
    rows=result.fetchall()
    rows1=rows[0]
    rows2=int(rows1[0])
    users_order=rows2+1
    query='''update users set ordered=? where id=?'''
    cnt.execute(query,(users_order,product))
    cnt.commit()
    ##adding date of purchased in table
    today_date=datetime.date.today()
    query=''' update products set date=? where id=?'''
    cnt.execute(query,(today_date,product))
    cnt.commit()




#-----------------------------------------------
win=tkinter.Tk()
win.title("main")
win.geometry("300x300")

# ------------------ widgets------------
user_lbl=tkinter.Label(text="username: ")
user_lbl.pack()

user_txt=tkinter.Entry(width=20)
user_txt.pack()

pas_lbl=tkinter.Label(text="password: ")
pas_lbl.pack()

pas_txt=tkinter.Entry(width=20)
pas_txt.pack()

msg_lbl=tkinter.Label(text="")
msg_lbl.pack()

login_btn=tkinter.Button(text="login",command=login)
login_btn.pack()

logout_btn=tkinter.Button(text="logout",state="disabled" ,command=logout)
logout_btn.pack()

submit_btn=tkinter.Button(text="submit" ,command=submit)
submit_btn.pack()

shop_btn=tkinter.Button(text="shop",state="disabled" ,command=shop)
shop_btn.pack()

AdminPanel_btn=tkinter.Button(text="admin panel",state="disabled",command=info)
AdminPanel_btn.pack()

win.mainloop()
