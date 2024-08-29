from datetime import datetime

from flask import Blueprint, render_template, app, request, send_file, g
from sqlalchemy import func

from Ibook.Forms import SyncBooks, ExportNotes
from Ibook.Extension import db
from Ibook.Models import Books, Notes
import openpyxl
# from sqlalchemy import func
# from Forms import

import sqlite3
import pandas as pd

import os
from glob import glob

ibook_bp = Blueprint('ibook', 'iBook', template_folder='Ibook/template', url_prefix='/ibook')


@ibook_bp.route('/', methods=['GET', 'POST'])
def choose_books():
    sync_form = SyncBooks()
    export_notes_form = ExportNotes()
    # local db path
    if sync_form.validate_on_submit():
        home_directory = os.path.expanduser('~')
        db_path = os.path.join(home_directory, 'Library', 'Containers',
                               'com.apple.iBooksX', 'Data', 'Documents')
        book_parent_path = os.path.join(db_path, 'BKLibrary')
        notation_parent_path = os.path.join(db_path, 'AEAnnotation')

        book_db_path = glob(os.path.join(book_parent_path, '*.sqlite'))[0]
        notation_db_path = glob(os.path.join(notation_parent_path, '*.sqlite'))[0]

        # print(book_db_path, notation_db_path)

        # connect to local db
        conn_book = sqlite3.connect(book_db_path)
        conn_notation = sqlite3.connect(notation_db_path)
        # Create a cursor object
        cursor_book = conn_book.cursor()
        cursor_notation = conn_notation.cursor()
        # book db: title, id, author, type:3(pdf),1(book)
        df_book = pd.read_sql_query('''SELECT ZTITLE, ZASSETID, ZAUTHOR, ZCONTENTTYPE 
                                            FROM ZBKLIBRARYASSET ORDER BY ZTITLE;''', conn_book)
        # note db
        df_notation = pd.read_sql_query('''SELECT ZANNOTATIONSELECTEDTEXT, ZANNOTATIONNOTE, ZANNOTATIONASSETID, 
                                                ZANNOTATIONSTYLE, ZANNOTATIONMODIFICATIONDATE
                                                FROM ZAEANNOTATION 
                                                WHERE ZANNOTATIONDELETED=0 AND ZANNOTATIONSELECTEDTEXT IS NOT NULL 
                                                ORDER BY ZANNOTATIONMODIFICATIONDATE DESC;''',
                                        conn_notation)
        # Remove old data
        books_remove = Books.query.all()
        for b in books_remove:
            db.session.delete(b)

        notes_remove = Notes.query.all()
        for b in notes_remove:
            db.session.delete(b)
        db.session.commit()

        for b in df_book.values:
            book = Books(bookname=b[0], assetid=b[1], author=b[2], type=b[3])
            db.session.add(book)
        for b in df_notation.values:
            note = Notes(highlights=b[0], style=b[3], notes=b[1], updatetime=b[4], bookid=b[2])
            db.session.add(note)

        db.session.commit()

        # book_query = Books.query.with_entities(Books.id, Books.bookname, Books.author, Books.type, Books.assetid).all()

        book_query = db.session.query(Books.id, Books.bookname,
                                      Books.author, Books.type,
                                      Books.assetid,
                                      func.count(Notes.id).label('note_num')
                                      ).outerjoin(Notes, Books.assetid == Notes.bookid).group_by(
            Books.assetid).order_by(Books.id).all()
        # print(book_query)

        book_data = pd.DataFrame(book_query, columns=['id', 'bookname', 'author', 'type', 'assetid', 'note_num'])
        book_data['type'] = book_data['type'].map({1: 'Book', 3: 'pdf'})
        book_data['note_num'] = book_data['note_num'].astype(int).apply(lambda x: '-' if x == 0 else x)
        # print(book_data)
        return render_template('choose_book.html', sync_form=sync_form, export_form=export_notes_form,
                               book_data=book_data)

    return render_template('choose_book.html', sync_form=sync_form, export_form=export_notes_form, book_data=None)


@ibook_bp.route('/export', methods=['GET', 'POST'])
def export():
    book_id = request.args.getlist('book_id')
    print(book_id)
    export_notes_query = db.session.query(
        Notes.highlights,
        Notes.notes,
        Notes.style,
        Notes.updatetime,
        Books.bookname
    ).outerjoin(Books, Books.assetid == Notes.bookid).filter(Notes.bookid.in_(book_id))
    # print(export_notes_query)
    export_notes = pd.DataFrame(export_notes_query, columns=['highlights', 'notes', 'style', 'updatetime', 'bookname'])
    export_notes['style'] = export_notes['style'].map({0: 'Underline',
                                                       1: 'Green',
                                                       2: 'Blue',
                                                       3: 'Yellow',
                                                       4: 'Pink',
                                                       5: 'Purple'})
    datediff = (datetime(2001, 1, 1) - datetime(1970, 1, 1)).days
    export_notes['updatetime'] = export_notes['updatetime'].apply(
        lambda x: (pd.Timestamp(x, unit='s') + pd.Timedelta(days=datediff, hours=8)).strftime('%Y-%m-%d %H:%M'))
    print(export_notes)
    export_notes.to_excel(g.file_name, index=False)
    return render_template('export_notes.html')


@ibook_bp.before_request
def before_request():
    g.export_date = datetime.today().strftime('%Y%m%d%H%M')
    g.file_name = os.path.join(os.getcwd(), f'Highlights Export-{g.export_date}.xlsx')


@ibook_bp.route('/download', methods=['GET', 'POST'])
def download():
    return send_file(g.file_name, as_attachment=True)
