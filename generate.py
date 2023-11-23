from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random

fake = Faker('ro_RO')

Base = declarative_base()

class Produs(Base):
    __tablename__ = 'produse'
    ProdusID = Column(Integer, Sequence('produs_id_seq'), primary_key=True)
    DenumireProdus = Column(String(50))
    Descriere = Column(String(200))
    Pret = Column(Float)
    Stoc = Column(Integer)

class Furnizor(Base):
    __tablename__ = 'furnizori'
    FurnizorID = Column(Integer, Sequence('furnizor_id_seq'), primary_key=True)
    NumeFurnizor = Column(String(50))
    Contact = Column(String(50))
    Adresa = Column(String(200))

class Client(Base):
    __tablename__ = 'clienti'
    ClientID = Column(Integer, Sequence('client_id_seq'), primary_key=True)
    Nume = Column(String(50))
    Prenume = Column(String(50))
    Email = Column(String(50))
    Telefon = Column(String(50))
    Adresa = Column(String(200))

class Comanda(Base):
    __tablename__ = 'comenzi'
    ComandaID = Column(Integer, Sequence('comanda_id_seq'), primary_key=True)
    ClientID = Column(Integer, ForeignKey('clienti.ClientID'))
    DataComanda = Column(DateTime)
    TotalPlata = Column(Float)

class DetaliiComanda(Base):
    __tablename__ = 'detaliicomanda'
    DetaliiID = Column(Integer, Sequence('detalii_id_seq'), primary_key=True)
    ComandaID = Column(Integer, ForeignKey('comenzi.ComandaID'))
    ProdusID = Column(Integer, ForeignKey('produse.ProdusID'))
    Cantitate = Column(Integer)

engine = create_engine('sqlite:///maya.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

for _ in range(50):
    new_furnizor = Furnizor(
    NumeFurnizor=fake.company(),
    Contact=fake.name(),
        Adresa=fake.address()
    )
    session.add(new_furnizor)
    
    new_client = Client(
        Nume=fake.first_name(),
        Prenume=fake.last_name(),
        Email=fake.email(),
        Telefon=fake.phone_number(),
        Adresa=fake.address()
    )
    session.add(new_client)

session.commit()

for _ in range(50):
    new_produs = Produs(
        DenumireProdus=fake.word(),
        Descriere=fake.text(max_nb_chars=100),
        Pret=round(random.uniform(10.0, 1000.0), 2),
        Stoc=random.randint(1, 100)
    )
    session.add(new_produs)

    new_comanda = Comanda(
        ClientID=random.randint(1, 50),
        DataComanda=fake.date_time_this_year(),
        TotalPlata=round(random.uniform(100.0, 5000.0), 2)
    )
    session.add(new_comanda)

session.commit()

for _ in range(50):
    new_detalii_comanda = DetaliiComanda(
        ComandaID=random.randint(1, 50),
        ProdusID=random.randint(1, 50),
        Cantitate=random.randint(1, 10)
    )
    session.add(new_detalii_comanda)

session.commit()

session.close()

print("Done!")
