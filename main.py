from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"

db = SQLAlchemy()
db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()

# all_books = []


@app.route('/')
def home():
    result = db.session.execute(db.select(Book))
    all_books = result.scalars()
    # if not all_books:
    #     # for book in all_books:
    #     #     print(book.title)
    #     print("book is not empty")
    print(all_books)
    print(type(all_books))
    # return render_template('index.html')
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        print('post request')
        with app.app_context():
            book = Book(title=request.form['name'], author=request.form['author'], rating=request.form['rating'])
            db.session.add(book)
            db.session.commit()


        # book = {
        #     "title": request.form['name'],
        #     "author": request.form['author'],
        #     "rating": request.form['rating'],
        # }
        # all_books.append(book)
        # print(all_books)
        return redirect(url_for('home'))

@app.route("/edit", methods=['POST', 'GET'])
def edit():
    id = request.args.get('id')
    if request.method == 'GET':
        book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        return render_template('edit.html', book=book)
    elif request.method == 'POST':
        book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        book_to_update.rating = float(request.form['rating'])
        db.session.commit()
        return redirect(url_for('home'))



@app.route('/delete')
def delete():
    id = request.args.get('id')
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    # or book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

