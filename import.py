import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from models import *

engine=create_engine('postgresql://nbuqpztkyejtia:8bc6f4b9bcd80bfacc004fd9d9b2f3fa2c43944cacdc6f77029e0097ce4b14ab@ec2-52-3-2-245.compute-1.amazonaws.com:5432/d2u1tj44hb629j')
db =scoped_session(sessionmaker(bind=engine))

def main():
    f=open(r"C:\Personal Files\Programming\Visual Studio Code\Flask\CS50-Project1(library)\book_details.csv")
    file=csv.reader(f)
    for isbn,title,author,year in file:
        isbn=isbn.lower()
        title=title.lower()
        author=author.lower()
        book=Book(title=title,author=author,isbn=isbn,public_year=year)
        db.add(book)
        db.commit()
        print("success: "+author)
if __name__=="__main__":
    
    main()