from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("postgres://qglciaoydkelng:a920e6b381ffaa4d62fe4e504fa58fa4436557e33b98d4c1833812ae4f97b9bd@ec2-35-153-12-59.compute-1.amazonaws.com:5432/d1p6jq117pi1j4",echo=True)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home", methods=["POST"])
def home():
    email = request.form.get("email")
    password = request.form.get("password")

    if db.execute("SELECT * FROM login WHERE email_id=:email_id AND password=:password",
    {"email_id": email, "password": password}).rowcount == 0:
        return render_template("error.html",message="Not found")

    else:
        name = db.execute("SELECT name FROM login WHERE email_id=:email_id",{"email_id":email}).fetchone()
        person = name[0].title()
        
        return render_template("home.html",user=person)

@app.route("/signup", methods=["GET","POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    check_user = db.execute("SELECT * FROM login WHERE email_id=:email_id",{"email_id":email}).fetchall()

    if check_user:
        return render_template("error.html",message="You are already registered. <br> Please login")

    else:
        db.execute("INSERT INTO login (name,email_id,password) VALUES (:name,:email_id,:password)",
        {"name":name, "email_id":email, "password":password})
        db.commit()
        return render_template("index.html",text="Successful registration. Please go to login page and login")

app.run()
