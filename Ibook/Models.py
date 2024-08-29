from Ibook.Extension import db
import pandas as pd


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(80), nullable=False)
    assetid = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80))
    type = db.Column(db.Integer, nullable=False)
    notes = db.relationship('Notes', backref='books')



class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    highlights = db.Column(db.Text, nullable=True)
    style = db.Column(db.Integer)
    notes = db.Column(db.Text)
    updatetime = db.Column(db.Integer)
    bookid = db.Column(db.String(80), db.ForeignKey('books.assetid'))