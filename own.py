import time,qrcode,image

from flask import (
    Flask,render_template,request,url_for,redirect,session,flash
)

from flask_mysqldb import MySQL

app =  Flask (__name__)

# app.secret_key="Sri@Love!"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ownapi"
app.config["MYSQL_CURSORCLASS"] = ""
app.secret_key = "I love you"
mysql = MySQL(app)

#  Register page code
@app.route("/",methods = ['GET','POST'])
@app.route("/index")
@app.route("/reg")
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        p1 = request.form["p1"]
        p2 = request.form["p2"]
        print(f"{name},{email},{p1},{p2}")

        if p1 == p2:
            cs = mysql.connection.cursor()
            q = "insert into reg(name,email,p1,p2) value(%s,%s,%s,%s)"
            cs.execute(q,(name,email,p1,p2))
            mysql.connection.commit()
            time.sleep(2)
        else:
            return "Invalid data"
        return redirect(url_for("log",name=name))
    return render_template("index.html")

# Login page block
@app.route("/log",methods = ['GET','POST'])
def log():
    msg = ""
    if request.method == 'POST':
        email = request.form['email']
        p2 = request.form['p2']
        print(email,p2)

#        q = f'SELECT email FROM reg WHERE p2 = {p2}'
        cur = mysql.connection.cursor()
#        cur.execute()
        cur.execute('SELECT * FROM reg WHERE email=%s AND p2=%s',(email,p2))
        rec = cur.fetchone()
        print(rec)
        if rec:
            session['log'] = True
            time.sleep(2)
            session['name'] = rec[1]
            flash("You are logged in Successfully !")
            return redirect(url_for('menu'))
            
        else:
            msg = "Invalid Username or Password and Try again"
    return render_template('log.html',msg=msg)

# Log out
@app.route('/logout')
def logout():
    session.pop('log',None)
    session.pop('email',None)
    return redirect(url_for('log'))

# Menu Page
@app.route("/menu")
def menu():
    time.sleep(3)
    return render_template("menu.html",name = session['name'])

# QR code Detail getting page
@app.route("/det",methods=["POST","GET"])
def main():
    if request.method == "POST":
        name = session['name']
        uqrn = request.form['uqrn']
        insta = request.form['insta']
        yt = request.form['yt']
        lkd = request.form['lkd']
        fb = request.form['fb']
        git = request.form['git']
        whp = request.form['whp']
        uqrcn = request.form['qrname']


        # Detail part qury code Section
        dc = mysql.connection.cursor()
        dq = "insert into det(name,uqrn,insta,yt,lkd,fb,git,whp) value(%s,%s,%s,%s,%s,%s,%s,%s)"
        dc.execute(dq,(name,uqrn,insta,yt,lkd,fb,git,whp))
        mysql.connection.commit()
        dc.close()


        #return redirect(url_for('gen'))
        i = qrcode.make(f"""
        \n\t Here in {uqrn} Detail's !
        \n Instagram : {insta} 
        \n Whats app : {whp}
        \n Facebook  : {fb}
        \n LinkDin   : {lkd}
        \n Gitup     : {git}
        \n Youtube   : {yt}
        """)
        i.save(f"{uqrn}.PNG")
        return redirect('myqr')
    return render_template("det.html",name = session['name'])


# Web page contained qr page
@app.route('/qrweb',methods = ['POST','GET'])
def qrweb():
    msgp = ""
    qr = mysql.connection.cursor()
    qr.execute("SELECT uqrn FROM det")
    qrn = qr.fetchall()

    if request.method == 'POST':
        name = session['name']
        uqrn = request.form['uqrn']
        print(uqrn)

        curs = mysql.connection.cursor()
        curs.execute("SELECT * FROM det WHERE name = %s AND uqrn = %s ",(name,uqrn))

        app.config["MYSQL_CURSORCLASS"] = "DictCursor"
        cr = curs.fetchall()

        print(qrn)
        print(cr)
        if cr:
            return render_template("qrweb.html",name=session['name'],uqrn=uqrn,cr=cr,qrn=qrn)
    return render_template("qrpopname.html",name=session['name'])

# My Qr page ( Pending )
@app.route('/myqr')
def myqr():
    return render_template("qrdisp.html",name=session['name'])

# Generated Qr code page ( Process going on )
@app.route("/gen",methods=['POST','GET'])
def gen():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM det"                                                                       
    con.execute(sql)
    re = con.fetchall()
    print(re)
    name = session['name']
    if re:
        return f"Hello {name} sorry for the issue process going on to rectify this error !"
    con.close()
    return render_template('qrgen.html',datas = re )


# Admin pannel
@app.route("/admin")
def admin():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM reg"
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"
    con.execute(sql)
    res = con.fetchall()
    print(res)
    con.close()
    return render_template("home.html",datas = res )


# Exit Option
@app.route("/exit")
def exit():
    return """
    <center><h1>Thank you for Using Smartipie (* _ *) !<h1></center>
    """
    quit()

if __name__ == "__main__":
    app.run(debug=True,port=5003)