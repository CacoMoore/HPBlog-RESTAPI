from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    

    def serialize(self):
        return {
            "username": self.username,
            "id": self.id,
            "age": self.age
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    alternate_name = db.Column(db.String(50))
    house = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(50))
    ancestry = db.Column(db.String(50))
    wand = db.Column(db.String(200))
    patronus = db.Column(db.String(50))
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "alternate_name": self.alternate_name,
            "house": self.house,
            "species": self.species,
            "date_of_birth": self.date_of_birth,
            "ancestry": self.ancestry,
            "wand": self.wand,
            "patronus": self.patronus,
        }
    
class Favorite(db.Model):
    __tablename__= 'favorite'
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.id'))
    chacrater_name = db.Column (db.String(50), db.ForeignKey('character.id'))

    def serialize(self):
        return {
            "username": self.username,
            "chacrater_name": self.chacrater_name,                
        }