from db import db
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

class UnsafeLocation(db.Model):
    __tablename__ = 'unsafe_locations'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    def __init__(self, description, location):
        self.description = description
        self.location = location

    # Location'ı Shapely Point formatında almak için yardımcı metot
    def get_location(self):
        return to_shape(self.location)


class SafeLocation(db.Model):
    __tablename__ = 'safe_locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    def __init__(self, name, category, location):
        self.name = name
        self.category = category
        self.location = location

    def get_location(self):
        return to_shape(self.location)