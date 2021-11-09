from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registered_at = db.Column(db.DateTime)
    phone = db.Column(db.String)
    postal_code = db.Column(db.String)
    name = db.Column(db.String)