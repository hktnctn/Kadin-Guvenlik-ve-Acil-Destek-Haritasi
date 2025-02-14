from flask import Blueprint, request, jsonify
from shapely.geometry import Point
from geoalchemy2.shape import from_shape
from models import db, UnsafeLocation, SafeLocation

# Blueprint
# app.py içinde
routes = Blueprint("safe_locations", __name__)


# Tehlikeli konum ekleme
@routes.route("/add_location", methods=["POST"])
def add_location():
    data = request.get_json()
    description = data.get("description")
    lat = data.get("lat")
    lon = data.get("lon")

    if not all([description, lat, lon]):
        return jsonify({"error": "Eksik veri"}), 400

    point = from_shape(Point(lon, lat), srid=4326)
    new_location = UnsafeLocation(description=description, location=point)

    try:
        db.session.add(new_location)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Tehlikeli konum başarıyla eklendi"}), 201


# Tehlikeli konumları listeleme
@routes.route("/get_locations", methods=["GET"])
def get_locations():
    locations = UnsafeLocation.query.all()
    result = [{
        "id": loc.id,
        "description": loc.description,
        "lat": loc.get_location().y,
        "lon": loc.get_location().x
    } for loc in locations]

    return jsonify(result), 200


# Güvenli konum ekleme
@routes.route("/add_safe_location", methods=["POST"])
def add_safe_location():
    data = request.get_json()
    name = data.get("name")
    category = data.get("category")  # Örn: "Hastane", "Kadın Sığınma Evi"
    lat = data.get("lat")
    lon = data.get("lon")

    if not all([name, category, lat, lon]):
        return jsonify({"error": "Eksik veri"}), 400

    point = from_shape(Point(lon, lat), srid=4326)
    new_safe_location = SafeLocation(name=name, category=category, location=point)

    try:
        db.session.add(new_safe_location)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Güvenli konum başarıyla eklendi"}), 201


@routes.route("/get_safe_locations_by_category/<category>", methods=["GET"])
def get_safe_locations_by_category(category):
    try:
        print(category)  # Kategoriyi konsola yazdır (debug için)
        locations = SafeLocation.query.filter_by(category=category).all()
        if not locations:
            return jsonify({"error": "Bu kategoriye ait konum bulunamadı"}), 404

        result = [{
            "id": loc.id,
            "name": loc.name,
            "category": loc.category,
            "lat": loc.get_location().y,  # Latitude (enlem)
            "lon": loc.get_location().x  # Longitude (boylam)
        } for loc in locations]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# En yakın güvenli konumu bulma
@routes.route("/get_nearest_safe_location", methods=["POST"])
def get_nearest_safe_location():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")
    category = data.get("category")  # Kullanıcının istediği kategori (Hastane, Sığınma Evi, vb.)

    if not all([lat, lon, category]):
        return jsonify({"error": "Eksik veri"}), 400

    # Kullanıcının gönderdiği koordinat
    user_point = Point(lon, lat)

    # Kategoriye göre güvenli konumları alıyoruz
    locations = SafeLocation.query.filter_by(category=category).all()

    if not locations:
        return jsonify({"error": "Kategoriye göre güvenli konum bulunamadı"}), 404

    # En yakın güvenli konumu hesaplamak
    nearest_location = None
    min_distance = float('inf')

    for loc in locations:
        # Veritabanındaki güvenli konumun geometrisini alıyoruz
        safe_location_point = loc.get_location()

        # İki nokta arasındaki mesafeyi hesaplıyoruz
        distance = user_point.distance(safe_location_point)

        if distance < min_distance:
            min_distance = distance
            nearest_location = loc

    if nearest_location:
        # En yakın güvenli konum bulundu, bilgilerini döndürüyoruz
        result = {
            "id": nearest_location.id,
            "name": nearest_location.name,
            "category": nearest_location.category,
            "lat": nearest_location.get_location().y,
            "lon": nearest_location.get_location().x,
            "distance": min_distance
        }
        return jsonify(result), 200

    return jsonify({"error": "En yakın güvenli konum bulunamadı"}), 404