from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger, swag_from
from random import choice
from utils import lst_users_data


# instancia flask, cors y swagger
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# configuracion swagger
app.config['SWAGGER'] = {"title": "API Rest"}
swagger_conf = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}
swagger = Swagger(app, config=swagger_conf)


# mostrar endpoints de api
@app.route('/', methods=['GET'])
def get_endpoints():
    return jsonify({
        "endpoints": [
            "/swagger",
            "/users",
            "/user/min_followers"
        ]
    }), 200


# obtener todos los usuarios
@app.route('/users', methods=['GET'])
@swag_from('swagger_conf.yml')
def get_users():
    if not lst_users_data():
        return jsonify({"error": "No users available"}), 404
    return jsonify(lst_users_data()), 200


# obtener todos usuario con menor cantidad de seguidores
@app.route('/user/min_followers', methods=['GET'])
@swag_from('swagger_conf.yml')
def get_user_with_min_followers():
    if not lst_users_data():
        return jsonify({"error": "No users available"}), 404

    # inicializa con el primer usuario
    min_followers_users = [lst_users_data()[0]]

    # comienzo a iterar despues del primer item
    for user_data in lst_users_data()[1:]:
        # comparo iteracion con primer item
        
        if len(user_data['users_following']) < len(min_followers_users[0]['users_following']):
            min_followers_users = [user_data]
        elif len(user_data['users_following']) == len(min_followers_users[0]['users_following']):
            min_followers_users.append(user_data)

    # selecciono un usuario random con el minimo de seguidores
    selected_user = choice(min_followers_users)

    # retorno el id del usuario y cantidad de seguidores
    return_data = {
        "user_id": selected_user["user_id"],
        "amount_of_followers": len(selected_user["users_following"])
    }
    return jsonify(return_data), 200