from flask import Flask, render_template , redirect , request , url_for
import sqlite3 as sql
from datetime import date
today = date.today().strftime("%Y-%m-%d")
app = Flask(__name__)
db_filename = 'Ini.db'
def sql_normal(time,price,item):
    with sql.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM normal  ORDER BY num DESC LIMIT 0 , 1")
        try:
            num = cursor.fetchall()[0][3]
            #print(num)
            num+=1
        except:
            num=1
        #print(num)
        act = '''INSERT INTO normal VALUES ("{}",{},"{}",{})'''.format(time,int(price),item,num)
        cursor.execute(act)
        return num

def sql_large(time,price,item):
    with sql.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM large  ORDER BY num DESC LIMIT 0 , 1")
        try:
            num = cursor.fetchall()[0][3]
            #print(num)
            num+=1
        except:
            num=1
        #print(num)
        act = '''INSERT INTO large VALUES ("{}",{},"{}",{})'''.format(time,int(price),item,num)
        cursor.execute(act)

        return num #流水號

def sql_buy(weight,Class,price,time):
        total = int(weight)*int(price)
        with sql.connect(db_filename) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM buy  ORDER BY num DESC LIMIT 0 , 1")
                try:
                        num = cursor.fetchall()[0][5]
                        #print(num)
                        num+=1
                except:
                        num=1
                #print(num)
                act = '''INSERT INTO buy VALUES ("{}",{},"{}",{},{},{})'''.format(time,int(weight),Class,int(price),int(total),num)
                cursor.execute(act)

def sql_sell(weight,Class,price,time,company):
    total = int(weight)*int(price)
    with sql.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sell  ORDER BY num DESC LIMIT 0 , 1")
        try:
            num = cursor.fetchall()[0][6]
            #print(num)
            num+=1
        except:
            num=1

        act = '''INSERT INTO sell VALUES ("{}",{},"{}",{},{},"{}",{})'''.format(time,int(weight),Class,int(price),int(total),company,num)
        cursor.execute(act)
        #cursor.fetchall()

def sql_search(time,table,company):
    print(time,table,company)
    if time == "":
        time = "%"
    if company == "全部":
        company = "%"
    print(time,table,company)
    with sql.connect(db_filename) as conn:
        cursor = conn.cursor()
        sell = '''SELECT * FROM sell WHERE day LIKE "{}" AND company LIKE "{}" '''.format(time,company)
        buy = '''SELECT * FROM buy WHERE day LIKE "{}" '''.format(time)
        large = '''SELECT * FROM large WHERE day LIKE "{}" '''.format(time)
        normal = '''SELECT * FROM normal WHERE day LIKE "{}"'''.format(time)

        if table == "全部":
            cursor.execute(sell)
            sell = cursor.fetchall()
            cursor.execute(buy)
            buy = cursor.fetchall()
            cursor.execute(large)
            large = cursor.fetchall()
            cursor.execute(normal)
            normal = cursor.fetchall()

            return sell,buy,large,normal

        if table == "賣出":
            cursor.execute(sell)
            sell = cursor.fetchall()

            return sell,[],[],[]

        if table == "買入":
            cursor.execute(buy)
            buy = cursor.fetchall()

            return [],buy,[],[]

        if table == "大筆支出":
            cursor.execute(large)
            large = cursor.fetchall()

            return [],[],large,[]

        if table == "日常支出":
            cursor.execute(normal)
            normal = cursor.fetchall()

            return [],[],[],normal

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update',methods = ['GET','POST'])
def update():

    table = request.form['table']
    time = request.form['time']
    num = request.form['num']

    if table == "large" or table == "normal":
        price = request.form['price']
        item = request.form['item']

        return render_template("update.html",time=time,price=price,item=item,num=num,table=table)
    if table == "buy":
       weight = request.form['weight']
       Class = request.form['Class']
       price = request.form['price']

       return render_template("update.html",time=time,price=price,weight=weight,Class=Class,num=num,table=table)

    if table == "sell":
       weight = request.form['weight']
       Class = request.form['Class']
       price = request.form['price']
       total = request.form['total']
       company = request.form['company']

       return render_template("update.html",time=time,price=price,weight=weight,Class=Class,total=total,company=company,num=num,table=table)

@app.route('/updateact',methods = ['GET','POST'])
def updateact():
    table = request.form['table']
    time = request.form['time']
    num = request.form['num']

    if table == "large" or table == "normal":
        price = request.form['price']
        item = request.form['item']

    if table == "buy":
       weight = request.form['weight']
       Class = request.form['Class']
       price = request.form['price']

    if table == "sell":
       weight = request.form['weight']
       Class = request.form['Class']
       price = request.form['price']
       total = request.form['total']
       company = request.form['company']

    return '''<h1>這裡是Updateact :)<h1>'''

@app.route('/account',methods = ['GET','POST'])
def account():
    return render_template('account.html',time = today)

@app.route('/large',methods = ['GET','POST'])
def large():
    return render_template('large.html',time = today)

@app.route('/largeact',methods = ['GET','POST'])
def largeact():
    try:
        time = request.form['time']
        price = request.form['price']
        item = request.form['item']
        #print(time,price,item)
    except:
        return render_template('large.html',time = today,msg="有未輸入選項")

    num = sql_large(time,price,item)
    manufactor = today + price + item + str(num)
    return render_template('large.html',time = today,manu = manufactor,price=price,item=item,num=num)

@app.route('/normal',methods = ['GET','POST'])
def normal():
    return render_template('normal.html',time = today)

@app.route('/normalact',methods = ['GET','POST'])
def normalact():
    try:
        time = request.form['time']
        price = request.form['price']
        item = request.form['item']
        #print(time,price,item)
    except:
        return render_template('normal.html',time = today,msg="有未輸入選項")
    num = sql_normal(time,price,item)
    manufactor = today + '  ' + price + '  ' + item + '  ' + str(num)
    return render_template('normal.html',time = today,manu = manufactor,price=price,item=item,num=num)

@app.route('/search',methods = ['GET','POST'])
def search():
    return render_template('search.html',time = today)

@app.route('/searchact',methods = ['GET','POST'])#search 處理頁面
def searchact():
    try:
        time = request.form['time']
        table = request.form['table']
    except:
        return render_template('search.html',time = today,msg="未選擇表單")
    company = ""
    if table == "賣出" or  table == "全部":
        try:
                company = request.form['company']
        except:
                return render_template('search.html',time = today,msg="買家未輸>入")
    #print(time,table,company)
    sell,buy,large,normal = sql_search(time,table,company)
    msg = ""
    if (table == "賣出" or  table == "全部") and sell == []:
        msg = "查無資料"
    if sell==[] and buy==[] and large==[] and normal == []:
        msg = "查無資料"

    money = [0,0,0,0] # buy,sell,large,normal
    for i in buy:
        money[0] += i[4]
    for i in sell:
        money[1] += i[4]
    for i in large:
        money[2] += i[1]
    for i in normal:
        money[3] += i[1]

    return render_template('search.html',time = today,msg=msg,money = money,sell=sell,buy=buy,large=large,normal=normal)


@app.route('/product',methods = ['GET','POST'])
def product():
    return render_template('product.html')

@app.route('/buy',methods = ['GET','POST'])
def buy():
    return render_template('buy.html',time = today)#給預設time

@app.route('/buyact',methods = ['GET','POST'])#buy 處理頁面
def buyact():
    weight = request.form['weight']
    Class = request.form['Class']
    price = request.form['price']
    time = request.form['time']

    #print(weight,Class,price,time)
    sql_buy(weight,Class,price,time)

    return redirect(url_for('buy'))

@app.route('/sell',methods = ['GET','POST'])
def sell():
    return render_template('sell.html',time = today)

@app.route('/sellact',methods = ['GET','POST'])#sell 處理頁面
def sellact():
    weight = request.form['weight']
    Class = request.form['Class']
    price = request.form['price']
    company = request.form['company']
    time = request.form['time']

    #print(weight,Class,price,company,time)
    sql_sell(weight,Class,price,time,company)

    return redirect(url_for('sell'))