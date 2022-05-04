import re
from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")
# POST route
@planets_bp.route("", methods=["POST"])
def handle_planets():
    request_body = request.get_json()
    new_planet = Planet(
        name = request_body["name"],
        description = request_body["description"],
        radius_mi = request_body["radius_mi"]
    )

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} successfully created with ID {new_planet.id}", 201)

@planets_bp.route("",methods=["GET"])
def give_planets():
    name_query = request.args.get("name")
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    else:
        planets = Planet.query.all()
    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "radius_mi": planet.radius_mi
            }
        )
    return jsonify(planets_response)

# class Planet:
#     def __init__(self, id, name, description, radius_mi):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.radius_mi = radius_mi

# # create a list of planet instances
# planets = [
#     Planet(1, "Earth", "amazing", 3958),
#     Planet(2, "Mercury","beautiful",1516),
#     Planet(3, "Venus", "bright", 3760)
# ]

# @planets_bp.route("",methods=["GET"])
# def give_planets():
#     planets_response = []
#     for planet in planets:
#         planets_response.append(
#             {
#                 "id": planet.id,
#                 "name": planet.name,
#                 "description": planet.description,
#                 "radius_mi": planet.radius_mi
#             }
#         )
#     return jsonify(planets_response)

# def validate_planet(planet_id):
#     # Want to return a valid planet object
#     # If invalid integer ID, we want to print out some error message with 404
#     # If noninteger ID, we want to print out some error message with 400
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         abort(make_response({'msg': f"ID:{planet_id} invalid. Input an integer."}, 400))
    
#     for planet in planets:
#         if planet_id == planet.id:
#             return planet

#     abort(make_response({'msg': f'Planet {planet_id} not found'}, 404))



# @planets_bp.route("/<planet_id>", methods=["GET"])
# def get_one_planet(planet_id):
#     planet = validate_planet(planet_id)
#     planet = {
#                 "id": planet.id,
#                 "name": planet.name,
#                 "description": planet.description,
#                 "radius_mi": planet.radius_mi
#             }
#     return planet, 200

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"}, 400))

    planet = Planet.query.get(planet_id)

    if planet is None:
        abort(make_response({'msg': f'Planet {planet_id} not found'}, 404))

    return planet


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    
    chosen_planet = validate_planet(planet_id)

    return {
                "id": chosen_planet.id,
                "name": chosen_planet.name,
                "description": chosen_planet.description,
                "radius_mi": chosen_planet.radius_mi
            }

@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_one_planet(planet_id):
    
    chosen_planet = validate_planet(planet_id)
    request_body = request.get_json()

    if "name" not in request_body or \
        "description" not in request_body or \
        "radius_mi" not in request_body:
        return jsonify ({'msg': f"Request must include name, description, and radius_mi."}), 400

    chosen_planet.name = request_body["name"]
    chosen_planet.description = request_body["description"]
    chosen_planet.radius_mi = request_body["radius_mi"]

    db.session.commit()

    return f"Planet {planet_id} updated successfully."

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    chosen_planet = validate_planet(planet_id)
    db.session.delete(chosen_planet)
    db.session.commit()

    return f"Planet {planet_id} deleted successfully."




