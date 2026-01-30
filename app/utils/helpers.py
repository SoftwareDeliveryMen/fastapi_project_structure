from typing import Any, Dict, Optional
from datetime import datetime
import re

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password: str) -> bool:
    """Check if password is strong enough"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

def sanitize_string(text: str) -> str:
    """Remove potentially harmful characters"""
    return re.sub(r'[<>{}]', '', text)

def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat()

def parse_datetime(dt_str: str) -> Optional[datetime]:
    """Parse ISO datetime string"""
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return None