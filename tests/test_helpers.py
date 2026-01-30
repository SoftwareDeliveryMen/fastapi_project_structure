"""Tests for utility helper functions"""
import pytest
from datetime import datetime
from app.utils.helpers import (
    is_valid_email,
    is_strong_password,
    sanitize_string,
    format_datetime,
    parse_datetime
)


class TestEmailValidation:
    """Test email validation helper"""
    
    def test_valid_emails(self):
        """Test valid email formats"""
        assert is_valid_email("user@example.com")
        assert is_valid_email("test.user@example.co.uk")
        assert is_valid_email("user+tag@example.com")
        assert is_valid_email("user123@test-domain.com")
    
    def test_invalid_emails(self):
        """Test invalid email formats"""
        assert not is_valid_email("invalid")
        assert not is_valid_email("@example.com")
        assert not is_valid_email("user@")
        assert not is_valid_email("user @example.com")
        assert not is_valid_email("user@.com")


class TestPasswordStrength:
    """Test password strength validation"""
    
    def test_strong_passwords(self):
        """Test passwords that meet all requirements"""
        assert is_strong_password("Password123")
        assert is_strong_password("MyP@ssw0rd")
        assert is_strong_password("Str0ngP@ss!")
    
    def test_weak_passwords(self):
        """Test passwords that don't meet requirements"""
        # Too short
        assert not is_strong_password("Pass1")
        # No uppercase
        assert not is_strong_password("password123")
        # No lowercase
        assert not is_strong_password("PASSWORD123")
        # No number
        assert not is_strong_password("PasswordABC")
        # Empty
        assert not is_strong_password("")


class TestStringSanitization:
    """Test string sanitization helper"""
    
    def test_sanitize_removes_harmful_chars(self):
        """Test that harmful characters are removed"""
        assert sanitize_string("hello<script>") == "helloscript"
        assert sanitize_string("user{name}") == "username"
        assert sanitize_string("test>value") == "testvalue"
        assert sanitize_string("normal text") == "normal text"
    
    def test_sanitize_preserves_safe_chars(self):
        """Test that safe characters are preserved"""
        assert sanitize_string("user_name-123") == "user_name-123"
        assert sanitize_string("test@example.com") == "test@example.com"


class TestDateTimeFormatting:
    """Test datetime formatting helpers"""
    
    def test_format_datetime(self):
        """Test datetime to ISO string conversion"""
        dt = datetime(2026, 1, 30, 12, 30, 45)
        formatted = format_datetime(dt)
        assert isinstance(formatted, str)
        assert "2026-01-30" in formatted
    
    def test_parse_datetime_valid(self):
        """Test parsing valid ISO datetime strings"""
        dt_str = "2026-01-30T12:30:45"
        parsed = parse_datetime(dt_str)
        assert parsed is not None
        assert isinstance(parsed, datetime)
        assert parsed.year == 2026
        assert parsed.month == 1
        assert parsed.day == 30
    
    def test_parse_datetime_invalid(self):
        """Test parsing invalid datetime strings"""
        assert parse_datetime("not a date") is None
        assert parse_datetime("2026-13-45") is None
        assert parse_datetime("") is None
    
    def test_datetime_roundtrip(self):
        """Test formatting and parsing roundtrip"""
        original = datetime(2026, 1, 30, 12, 30, 45)
        formatted = format_datetime(original)
        parsed = parse_datetime(formatted)
        assert parsed is not None
        assert parsed.year == original.year
        assert parsed.month == original.month
        assert parsed.day == original.day
