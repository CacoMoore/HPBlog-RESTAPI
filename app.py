from flask import Flask,request, jsonify
from models import db, User, Character, Favorite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

@app.route("/")
def home():
    return "Hello there! from Caro Moore"

#USERS

@app.route("/users", methods=["POST"])
def create_user():
    user = User()
    user.username = request.json.get("username")
    user.password = request.json.get("password")
    user.age = request.json.get("age")

    db.session.add(user)
    db.session.commit()

    return "Usuario guardado", 200

@app.route("/users/list", methods=["GET"])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.serialize())
    return jsonify(result)

@app.route("/users/<int:id>", methods=["PUT", "DELETE"])
def update_user(id):
    user = User.query.get(id)
    if user is not None:
        if request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()

            return jsonify("Eliminado"), 204
        else:
            user.age = request.json.get("age")
            
            db.session.commit()
            
            return jsonify("Usuario actualizado"), 200
    
    return jsonify("Usuario no encontrado muAjajaja i'm a teapot"), 418

# CHARACTER

@app.route("/characters", methods=["POST"])
def create_character():
    character = Character()
    character.name = request.json.get("name")
    character.alternate_name = request.json.get("alternate_name")
    character.house = request.json.get("house")
    character.species = request.json.get("species")
    character.date_of_birth = request.json.get("date_of_birth")
    character.ancestry = request.json.get("ancestry")
    character.wand = request.json.get("wand")
    character.patronus = request.json.get("patronus")

    db.session.add(character)
    db.session.commit()

    return "Personaje guardado", 200

@app.route("/characters/list", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    result = []
    for character in characters:
        result.append(character.serialize())
    return jsonify(result)

@app.route("/characters/<int:id>", methods=["PUT", "DELETE"])
def update_characters(id):
    character = Character.query.get(id)
    if character is not None:
        if request.method == "DELETE":
            db.session.delete(character)
            db.session.commit()

            return jsonify("Personaje Eliminado"), 204
        else:
            character.patronus = request.json.get("patronus")
            
            db.session.commit()
            
            return jsonify("Personaje actualizado"), 200
    
    return jsonify("Personaje no encontrado muAjajaja i'm a teapot"), 418

# FAVORITES

@app.route("/favorites", methods=["POST"])
def create_favorite():
    favorite = Favorite()
    favorite.username = request.json.get("username")
    favorite.chacrater_name = request.json.get("chacrater_name")
    
    db.session.add(favorite)
    db.session.commit()

    return "Favorito guardado", 200

@app.route("/favorites/list", methods=["GET"])
def get_favorites():
    favorites = Favorite.query.all()
    result = []
    for favorite in favorites:
        result.append(favorite.serialize())
    return jsonify(result)

@app.route("/favorites/<int:id>", methods=["PUT", "DELETE"])
def update_favorite(id):
    favorite = Favorite.query.get(id)
    if favorite is not None:
        db.session.delete(favorite)
        db.session.commit()

        return jsonify("Favorito Eliminado"), 204
    else:
        return jsonify("Usuario no encontrado muAjajaja i'm a teapot"), 418

with app.app_context():
    db.create_all()


app.run(host="localhost", port="8080")