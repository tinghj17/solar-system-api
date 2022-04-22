from flask import Blueprint, jsonify

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

