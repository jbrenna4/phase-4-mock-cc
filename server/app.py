#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# @app.route('/')
# def home():
#     return ''



class Heroes(Resource):
    def get(self):

        heroes_list = [hero.to_dict() for hero in Hero.query.all()]

        response = make_response(heroes_list, 200)

        return response
    
api.add_resource(Heroes, '/heroes')

class HeroById(Resource):
    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first().to_dict()

        if not hero:
            return make_response({
                "error": "Hero not found"
            }, 404)

        response = make_response(hero, 200)

        return response

api.add_resource(HeroById, '/heroes/<int:id>')


class Powers(Resource):
    def get(self):

        powers_list = [power.to_dict() for power in Power.query.all()]

        response = make_response(powers_list, 200)

        return response
    
api.add_resource(Powers, '/powers')

class PowerById(Resource):
    def get(self, id):
        power = Power.query.filter(Power.id == id).first().to_dict()

        if not power:
            return make_response({
                "error": "Power not found"
            }, 404)

        response = make_response(power, 200)

        return response
    

    def patch(self, id):

        power = Power.query.filter(Power.id == id).first()


        # do i have to import abort??? 
        if not power:
            return make_response({
                "error": "Power not found"
            }, 404)

        request_json = request.get_json()
        for key in request_json():
            setattr(power, key,request_json[key])
        
        db.session.add(power)
        db.session.commit()

        response = make_response(power.to_dict(), 200)

        return response

api.add_resource(PowerById, '/powers/<int:id>')


# POST /hero_powers ....woof, not sure about this one but i'll try!
# really need to go over Post...not sure about a lot of this one...
# not sure where to put my error...or why not abort?

class HeroPowers(Resource):
    def get(self):

        hero_powers_list = [hero_powers.to_dict() for hero_powers in HeroPower.query.all()]

        response = make_response(hero_powers_list, 200)

        return response
    
    def post(self):
        request_json = request.get_json()


        new_hero_power = HeroPower(
            strength=request_json['strength'],
            hero_id=request_json['hero_id'],
            power_id=request_json['power_id']
        )

        if not new_hero_power:
            return make_response({
                "error": "Invalid input"
            }, 404)

        db.session.add(new_hero_power)
        db.session.commit()


        response = make_response(new_hero_power.to_dict(), 201)

        return response




api.add_resource(HeroPowers, '/hero_powers')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
