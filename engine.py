from flask import Flask, render_template, request, redirect,jsonify,session
import pymysql.cursors
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chapilovesocy'


@app.route("/handle")
def handle():
 if 'serverid' and 'clientmail' in session:
  
  db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='capi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)   
  conn = db.cursor()
  conn.execute("SELECT * FROM message WHERE mesfrom = %s AND mesto= %s OR mesfrom=%s AND mesto=%s",(session['clientmail'],session['serverid'],session['serverid'],session['clientmail']))
  messages = conn.fetchall()
    
  return render_template("handler.html", messages=messages)
 else :
   return '<center>Invalid Request</center>'   
 
   

@app.route("/chat/<string:serverid>",methods=['GET','POST'])
def chat(serverid):
 db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='capi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

 conn = db.cursor()
 conn.execute('SELECT * FROM users WHERE email = %s ', (serverid))
 user = conn.fetchone()
 if user:  

  session['serverid']=serverid    
  if request.method =='POST':
     if  'clientmail' in session: 
       
       db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='capi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)  

       mesfrom= session['clientmail']
       message= request.form.get('message')
       conn = db.cursor()
      
      
       conn.execute("INSERT INTO message (mesfrom,message,mesto,ip) VALUES (%s, %s,%s,%s)", (mesfrom, message, serverid,session['remoteip']))
       conn.connection.commit()
      
     else:
       session['remoteip']=request.remote_addr
       session['clientmail']=request.form.get('email')
       return render_template("dialog.html" ,tag="card card-prirary cardutline direct-chat direct-chat-primary",display="",serverid=serverid)

  else:
    if  'clientmail' in session: 
      return render_template("dialog.html" ,tag="card card-prirary cardutline direct-chat direct-chat-primary",display="",serverid=serverid)
    else:
      return render_template("dialog.html" ,tag="card card-prirary cardutline direct-chat direct-chat-primary direct-chat-contacts-open",display="display:none;",serverid=serverid) 
 else:
  return 'yanlış'
@app.route("/dashhandler-chat",methods=['GET','POST'])
def dashandler_chat():
 
  if request.method=="POST":  
     
     session['clientmaildash']= request.form.get('clientmail') 
     db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='capi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
      
      
     conn = db.cursor()
     conn.execute("UPDATE message SET unreaded=%s WHERE mesfrom=%s",("0",session['clientmaildash']))
     conn.connection.commit()
     conn.execute("SELECT * FROM message WHERE mesfrom = %s AND mesto= %s OR mesfrom=%s AND mesto=%s",(session['clientmaildash'],session['serverid_dash'],session['serverid_dash'],session['clientmaildash']))
     meesages=conn.fetchall()
     
     return render_template("dashhandler-chat.html",messages=meesages)
     
     
  else :
     if 'clientmaildash' in session:
      db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='capi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
      conn = db.cursor()
      conn.execute("SELECT * FROM message WHERE mesfrom = %s AND mesto= %s OR mesfrom=%s AND mesto=%s",(session['clientmaildash'],session['serverid_dash'],session['serverid_dash'],session['clientmaildash']))
      meesages=conn.fetchall()
     
      return render_template("dashhandler-chat.html",messages=meesages)
     else:
         return "mail sec" 
     

@app.route("/dashhandler",methods=['GET','POST'])
def dashandler():
    db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='capi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
      
      
    conn = db.cursor()
      
      
    conn.execute("select mesfrom , sum(unreaded) as unreaded from message where mesto =%s group by mesfrom",session['serverid_dash'])

      
    listed=conn.fetchall()
    return render_template("dashhandler.html",listed=listed)

@app.route("/auth/login",methods=['POST','GET'])
def login():
  if request.method == 'POST':
    
    db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='capi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    conn = db.cursor()
    email= request.form.get('email')
    password= request.form.get('password')
    conn.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
    user = conn.fetchone()
    if user:
      session['serverid_dash']=email
      return redirect("/dashboard") 
    else:
      return render_template("login.html", msg="HATA" )     
  else:
     return render_template("login.html",msg="")    

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
 if request.method =='POST' : 
   db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='capi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)  

    
   message= request.form.get('message')
    
   conn = db.cursor()
      
      
   conn.execute("INSERT INTO message (mesfrom,message,mesto) VALUES (%s, %s,%s)", (session['serverid_dash'], message, session['clientmaildash']))
   conn.connection.commit()
 else:
    if 'serverid_dash' in session:
     
     return render_template("dashboard.html")
    else:
        return redirect("/auth/login") 

@app.route("/dash/logout")
def dashout():
 session.clear()

 return redirect("/auth/login")    

if __name__ == "__main__":    
 app.run(debug=True, port=1999)
