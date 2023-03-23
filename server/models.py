from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='hero')

    serialize_rules = ('-hero_powers.hero', '-powers.heroes', '-created_at', '-updated_at')

    # honestly not sure if we need this, what it does or how to write it (might need to be a tuple if it's single argument)!
    # association_proxy(table name, column name)
    #activities = association_proxy('hero_powers', 'power')

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='power')

    serialize_rules = ('-hero_powers',  '-heroes.powers', '-created_at', '-updated_at')

    @validates('description')  
    def validate_description(self, key, description):
        if not description:
            raise ValueError('Description must be present.')
        
        if len(description) < 20:
            raise ValueError('the description must be at least 20 characters')
        return description


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    #hero = db.relationship('Hero', back_populates='hero_powers')
    #power = db.relationship('Power', back_populates='hero_powers')

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers', '-created_at', '-updated_at')



    # not 100% sure this is how you write this if statement!
    @validates('strength')  
    def validate_strength(self, key, strength):
        if strength != 'Strong' and strength != 'Weak' and strength != 'Average':
            raise ValueError('that is not a valid strength rating')
        return strength 