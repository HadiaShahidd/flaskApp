from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///firstapp.db"
with app.app_context():
    db = SQLAlchemy(app)

class FirstApp(db.Model):
    sno=db.Column(db.Integer,primary_key=True,autoincrement=True)
    fname=db.Column(db.String(100), nullable=False)
    lname=db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    
    def _repr_(self):
        return f"{self.sno} - {self.fname}"

@app.route('/', methods = {'GET','POST'})
def hello_world():
    if request.method=='POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')

        if fname and lname and email:
            firstapp = FirstApp(fname=fname,lname=lname,email=email)
            db.session.add(firstapp)
            db.session.commit()


    allpeople = FirstApp.query.all()

    return render_template('Index.html',allpeople=allpeople)
    #return 'Hello, World! This is Hadia Shahid'

@app.route('/home')
def home():
    return 'Welcome to the Home Page of my WEB APP'

@app.route('/delete/<int:sno>')
def delete(sno):
    allpeople = FirstApp.query.filter_by(sno=sno).first()
    db.session.delete(allpeople)
    db.session.commit()

    return redirect("/")

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        
        if fname and lname and email:
            #create & commit new records to the database
            firstapp = FirstApp(fname=fname, lname=lname, email=email)
            db.session.add(firstapp)
            db.session.commit()
            
    allpeople = FirstApp.query.filter_by(sno=sno).first()
    
    return render_template('update.html', allpeople=allpeople)


if __name__ == "__main__":
    app.run(debug=True)