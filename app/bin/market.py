from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
db=SQLAlchemy(app)

class Item(db.Model):
    name=db.Column(db.String(length=30))
    
    
    
@app.route('/market')
def goto_market():
    return render_template('hello.html',name='kim')
