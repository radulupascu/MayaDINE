from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maya.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produs(db.Model):
    __tablename__ = 'produse'
    ProdusID = db.Column(db.Integer, primary_key=True)
    DenumireProdus = db.Column(db.String(128))
    Descriere = db.Column(db.String(512))
    Pret = db.Column(db.Float)
    Stoc = db.Column(db.Integer)
    FurnizorID = db.Column(db.Integer, db.ForeignKey('furnizori.FurnizorID'))

class Furnizor(db.Model):
    __tablename__ = 'furnizori'
    FurnizorID = db.Column(db.Integer, primary_key=True)
    NumeFurnizor = db.Column(db.String(128))
    Contact = db.Column(db.String(128))
    Adresa = db.Column(db.String(512))

class Client(db.Model):
    __tablename__ = 'clienti'
    ClientID = db.Column(db.Integer, primary_key=True)
    Nume = db.Column(db.String(128))
    Prenume = db.Column(db.String(128))
    Email = db.Column(db.String(128))
    Telefon = db.Column(db.String(64))
    Adresa = db.Column(db.String(512))

class Comanda(db.Model):
    __tablename__ = 'comenzi'
    ComandaID = db.Column(db.Integer, primary_key=True)
    ClientID = db.Column(db.Integer, db.ForeignKey('clienti.ClientID'))
    DataComanda = db.Column(db.DateTime)
    TotalPlata = db.Column(db.Float)

class DetaliiComanda(db.Model):
    __tablename__ = 'detaliicomanda'
    DetaliiID = db.Column(db.Integer, primary_key=True)
    ComandaID = db.Column(db.Integer, db.ForeignKey('comenzi.ComandaID'))
    ProdusID = db.Column(db.Integer, db.ForeignKey('produse.ProdusID'))
    Cantitate = db.Column(db.Integer)

@app.route('/')
def index():
    furnizori = Furnizor.query.all()
    print(f"Furnizori: {furnizori}")  
    return render_template('index.html', furnizori=furnizori)


@app.route('/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        nume_furnizor = request.form.get('nume')
        contact = request.form.get('contact')
        adresa = request.form.get('adresa')
        
        furnizor = Furnizor(NumeFurnizor=nume_furnizor, Contact=contact, Adresa=adresa)
        db.session.add(furnizor)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_supplier.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
