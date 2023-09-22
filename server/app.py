#!/usr/bin/env python3

from urllib import response
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False
app.json_as_ascii = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data["name"],
            image=data["image"],
            price=data["price"],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, "/plants")


class PlantByID(Resource):
    # GET
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        if plant:
            return make_response(jsonify(plant), 200)
        else:
            return make_response(jsonify({"message": "Plant not found"}), 404)

    # PATCH
    def patch(self, id):
        plant = Plant.query.get(id)

        if not plant:
            return make_response(jsonify({"message": "Plant not found"}), 404)

        data = request.get_json()

        if "is_in_stock" in data:
            plant.is_in_stock = bool(data["is_in_stock"])

            db.session.commit()

        return make_response(jsonify(plant.to_dict()), 200)

    # DELETE
    def delete(self, id):
        plant = Plant.query.get(id)

        if not plant:
            return make_response(jsonify({"message": "Plant not found"}), 404)

        db.session.delete(plant)
        db.session.commit()

        return make_response(jsonify({"message": "Plant record successfully deleted"}), 200)


api.add_resource(PlantByID, "/plants/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
