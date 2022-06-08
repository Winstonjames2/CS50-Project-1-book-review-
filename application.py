from flask import Flask, redirect, render_template,request,session, url_for
from flask_session import Session
from models import *
import requests

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='--DATABASE URI--'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
db.init_app(app)

@app.route("/")
def index():
    if not session.get("username"):
        return redirect("/login")
    else:
        user=session["username"]
        return render_template("index.html",user=user)

@app.route("/register",methods=["POST","GET"])
def register():
    username=request.form.get("username")
    password=request.form.get("password")
    password1=request.form.get("password1")
    if request.method=="POST":
        if username!="" or password!="":
            if password==password1:
                username_database=User.query.filter_by(username=username).first()
                if username_database:
                    return render_template("register.html",message_f="Username Already Exists!")
                else:
                    user=User(username=username,password=password)
                    db.session.add(user)
                    db.session.commit()
                    return redirect("/")
            else:
                return render_template("register.html",message_f="Password Does Not Match!")
        else:
            return render_template("register.html",message_f="Error, Credentials Invalid!")
    return render_template("register.html")

@app.route("/login",methods=["POST","GET"])
def login():
    username=request.form.get("username")
    password=request.form.get("password")
    if request.method=="POST":
        user_database=User.query.filter_by(username=username,password=password).first()
        if user_database:
            session["username"]=user_database.username
            session["user_id"]=user_database.id
            print(user_database.id)
            return redirect("/")
        else:
            return render_template("login.html",message_f="Username Does Not Exist or Password Incorrect")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["username"]=None
    return redirect("/")

@app.route("/search",methods=["POST","GET"])
def search():
    if not session.get("username"):
        return redirect("/login")
    message_f=None
    isbn=request.form.get("isbn",None)
    title=request.form.get("title",None)
    author=request.form.get("author",None)
    user=session["username"]
    data_list=[]
    if request.method=="POST":
        isbn=isbn.lower()
        title=title.lower()
        author=author.lower()
        if isbn:
            data=Book.query.filter_by(isbn=isbn).first()
        elif title:
            data=Book.query.filter(Book.title.like(f"%{title}%")).all()
        else:
            data=Book.query.filter(Book.author.like(f"%{author}%")).all()
        print(data)
        if data is not None and data !=[]:
            for d in data:
                d.title=d.title.title()
                d.author=d.author.title()
                data_list.append(d)
            return render_template("index.html",books=data_list,user=user)
    return render_template("index.html",user=user,message_f="Not Found For: {}{}{}".format(author,title,isbn))

@app.route("/review/<int:code>")
def review(code):
    if not session.get("username"):
        return redirect("/login")
    book=Book.query.get(code)
    book.title=book.title.title()
    book.author=book.author.title()
    book.isbn=book.isbn.title()
    session["book"]=book
    revi_url=requests.get("https://www.goodreads.com/book/review_counts.json?isbns="+session["book_isbn"])
    data=revi_url.json()
    for data in data["books"]:
        review=data
    review_data=Review.query.filter_by(book_id=session["book"].isbn).order_by(Review.id.desc())
    return render_template("review.html",user=session["username"],book=book,review=review,review_data=review_data,message_f="Error, Please Write Review First!")

@app.route("/submit_review",methods=["POST"])
def submit_review():
    if not session.get("username"):
        return redirect("/login")
    rev=request.form.get("reviews")
    if rev !="":
        r=Review(book_id=session["book"].isbn,review=rev,acc_id=session["user_id"])
        db.session.add(r)
        db.session.commit()
    return redirect(url_for("review",code=session["book"].id))
