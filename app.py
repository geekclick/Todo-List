import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)

    def __repr__(self) -> str:
        return f'{self.title} - {self.desc}'

@app.route('/', methods=['GET','POST'])
def home():
    data = Todo.query.all()
    return render_template('index.html', data=data)

@app.route('/add-todo', methods=['GET','POST'])
def add_todo():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        date=datetime.date.today()
        sentToDb = Todo(title=title, desc=desc, date=date)
        db.session.add(sentToDb)
        db.session.commit()
        return redirect('/')
    return render_template('index.html')

@app.route('/edit/<string:sno>', methods=['GET','POST'])
def edit_todo(sno):
    if request.method=='POST':
            title = request.form['title']
            desc = request.form['desc']
            date = datetime.date.today()
            data = Todo.query.filter_by(sno=sno).first()
            data.title = title
            data.desc = desc
            data.date = date
            db.session.commit()
            return redirect('/')
    data = Todo.query.filter_by(sno=sno).first()
    return render_template('edit.html',data=data, sno=sno)

@app.route('/delete/<int:sno>', methods=["GET","POST"])
def delete(sno):
    data = Todo.query.filter_by(sno=sno).first()
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)