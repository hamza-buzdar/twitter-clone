
import re
from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
from datetime import timedelta
app = Flask(__name__)
app.secret_key='hums'
app.config["MYSQL_HOST"]='localhost'
app.config["MYSQL_USER"]='root'
app.config["MYSQL_PASSWORD"]="KoniMani.212"
app.config["MYSQL_DB"]="lab5ex1"
mysql=MySQL(app)

@app.route('/testDatabase')
def testDatabase():
    '''


    :return:
      '''
    return 'Database Passed!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods=['Get','Post'])
def signup():
    msg=''
    if request.method=='POST':
        user_details=request.form
        name=user_details['name']
        password=user_details['password']
        confirmpassword=user_details['confirmpassword']
        if password==confirmpassword and len(name)!= 0 and len(password) !=0:
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO lab5ex1(name,password) VALUES(%s,%s)",(name,password))
            mysql.connection.commit()
            cur.close()
            return redirect('login')
        else:
            msg ='kindly try again your some field is missing'
    return render_template('signup.html',msg=msg)


@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Lab5ex1")
    if app.permanent_session_lifetime <= timedelta(minutes=10) :
        return render_template('dashboard.html', username=session['username'], password=session['password'])
    elif app.permanent_session_lifetime > timedelta(minutes=10):
        return(redirect(url_for('login')))
@app.route('/login', methods = ['GET','POST'])
def login():
    msg=''
    if request.method=='POST':

        logindetails=request.form
        name=logindetails['name']
        password=logindetails['password']


        cur = mysql.connection.cursor()
        cur.execute('select * from lab5ex1 where name=%s and password=%s', (name, password))
        user = cur.fetchone()
        

        if user:
            session['loggedin'] = True
            session['username'] = user[0]
            session['password'] = user[1]
            session['personid'] = user[2]
            return redirect('dashboard')
        else:
            msg='Either password or name is wrong'
    
    return render_template('login.html',msg=msg)
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        post_details=request.form
        name=post_details['title']
        postcontent=post_details['postcontent']
        cur=mysql.connection.cursor()

        personid = session['personid']

        cur.execute("INSERT INTO post(posttitle,postcontent,Personid) VALUES(%s,%s,%s)",(name,postcontent,personid))
        mysql.connection.commit()
        cur.close()
        # return redirect(url_for(".display_post", title=title))
    return render_template("newpost.html")
@app.route("/following",methods=["GET","POST"])
def following():
    if request.method=="POST":
        username=request.form
        name=username["Username"]
        cur=mysql.connection.cursor()
        personid = session['personid']
        print(personid)
        cur.execute("select name from lab5ex1 where name=%s",(name,))
        user=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        print(user)
        length1=0
        namee=[]
        for i in range(len(user)):
            namee.append(user[0][0])
            length1+=1

        return render_template("follow.html",name=namee,length=length1)


    return render_template("following.html")
@app.route("/follow",methods=["GET","POST"])
def follow():
    if request.method=="POST":
        follower = request.form
        followerName = follower['name[i]']  
        print(followerName)

        cur=mysql.connection.cursor()
        personid = session['personid']
        print(personid)
    
        followerid = cur.execute("Select Personid from lab5ex1 where name=%s", (followerName))
        cur.execute("Insert into following (Personid , folowerid) Values(%d,%d)", (personid,followerid))
        mysql.connection.commit()
        cur.close()


    return render_template("follow.html")
@app.route("/showtweet")

def showtweet():
    cur=mysql.connection.cursor()
    a=session["personid"]
    # print(a)
    cur.execute("select * from post where Personid=%s", (a,))

    user=cur.fetchall()
    mysql.connection.commit()
    cur.close()

    title,content = [],[]
    for i in range(len(user)):
        title.append(user[i][1])
        print(title)
        content.append(user[i][2])
    length = len(content)
    return render_template ("showtweet.html",title=title, content= content,length= length, range = range)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)

# @app.tweets
# def tweets_to_make():
