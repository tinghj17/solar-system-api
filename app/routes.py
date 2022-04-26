from flask import Blueprint, jsonify, abort, make_response

class Planet:
    def __init__(self, id, name, description, radius_mi):
        self.id = id
        self.name = name
        self.description = description
        self.radius_mi = radius_mi

# create a list of planet instances
planets = [
    Planet(1, "Earth", "amazing", 3958),
    Planet(2, "Mercury","beautiful",1516),
    Planet(3, "Venus", "bright", 3760)
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")
@planets_bp.route("",methods=["GET"])
def give_planets():
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

def validate_planet(planet_id):
    # Want to return a valid planet object
    # If invalid integer ID, we want to print out some error message with 404
    # If noninteger ID, we want to print out some error message with 400
    try:
        planet_id = int(planet_id)
    except ValueError:
        abort(make_response({'msg': f"ID:{planet_id} invalid. Input an integer."}, 400))
    
    for planet in planets:
        if planet_id == planet.id:
            return planet

    abort(make_response({'msg': f'Planet {planet_id} not found'}, 404))



@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    planet = {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "radius_mi": planet.radius_mi
            }
    return planet, 200



# @planets_bp.route("/<planet_id>", methods=["GET"])
# def get_one_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         return {'msg': f"ID:{planet_id} invalid. Input an integer."}, 400
#     chosen_planet = None
#     for planet in planets:
#         if planet_id == planet.id:
#             chosen_planet = {
#                 "id": planet.id,
#                 "name": planet.name,
#                 "description": planet.description,
#                 "radius_mi": planet.radius_mi
#             }
#     if chosen_planet is None:
#         return {'msg': f'Planet {planet_id} not found'}, 404
#     return chosen_planet, 200

