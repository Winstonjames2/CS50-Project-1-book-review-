import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from models import *

engine=create_engine('--DATABASE URI--')
db =scoped_session(sessionmaker(bind=engine))

def main():
    f=open(r"--book_details.csv--")
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
