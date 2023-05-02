from flask import Flask,request, jsonify
from models import db, User, Character, Favorite
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = "ultra-secret"                   #la llave secreta no debería estar en el código, sino que en guardado en variables de entorno
db.init_app(app)

migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    return "Hello there! from Caro Moore"

#USERS

@app.route("/users", methods=["POST"])
def create_user():
    user = User()
    user.username = request.json.get("username")
    user.age = request.json.get("age")

    password = request.json.get("password")
    password_hash = generate_password_hash(password)
    user.password = password_hash
    

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "msg":"User have been created"
    }), 200

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()              #chequea que el usuario exista
    if user is not None:
        is_valid = check_password_hash(user.password, password)         #chequea que la constraseña es válida
        if is_valid:                                                    #ahora generamos token
            access_token = create_access_token (identity=username)      #identity irá en el payload
            return jsonify({
                "token": access_token
            }), 200
    else: jsonify({                                                     #si la contraseña no es válida, enviamos mensaje
        "msg": "User does not exist or info is invalid"
    }), 400                                                             #mejor 400 que 404, es mejor no dar más información para el usuario (caso de hackers)


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

if __name__ == "__main__":
    app.run(host="localhost", port="8080")