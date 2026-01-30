"""Tests for custom exception classes"""
import pytest
from fastapi import status
from app.utils.exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    ConflictException
)


class TestNotFoundException:
    """Test NotFoundException custom exception"""
    
    def test_default_message(self):
        """Test exception with default message"""
        exc = NotFoundException()
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.detail == "Resource not found"
    
    def test_custom_message(self):
        """Test exception with custom message"""
        exc = NotFoundException("User not found")
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.detail == "User not found"


class TestBadRequestException:
    """Test BadRequestException custom exception"""
    
    def test_default_message(self):
        """Test exception with default message"""
        exc = BadRequestException()
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Bad request"
    
    def test_custom_message(self):
        """Test exception with custom message"""
        exc = BadRequestException("Invalid input")
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Invalid input"


class TestUnauthorizedException:
    """Test UnauthorizedException custom exception"""
    
    def test_default_message(self):
        """Test exception with default message"""
        exc = UnauthorizedException()
        assert exc.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.detail == "Unauthorized"
        assert exc.headers == {"WWW-Authenticate": "Bearer"}
    
    def test_custom_message(self):
        """Test exception with custom message"""
        exc = UnauthorizedException("Invalid token")
        assert exc.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.detail == "Invalid token"
        assert exc.headers == {"WWW-Authenticate": "Bearer"}


class TestForbiddenException:
    """Test ForbiddenException custom exception"""
    
    def test_default_message(self):
        """Test exception with default message"""
        exc = ForbiddenException()
        assert exc.status_code == status.HTTP_403_FORBIDDEN
        assert exc.detail == "Forbidden"
    
    def test_custom_message(self):
        """Test exception with custom message"""
        exc = ForbiddenException("Access denied")
        assert exc.status_code == status.HTTP_403_FORBIDDEN
        assert exc.detail == "Access denied"


class TestConflictException:
    """Test ConflictException custom exception"""
    
    def test_default_message(self):
        """Test exception with default message"""
        exc = ConflictException()
        assert exc.status_code == status.HTTP_409_CONFLICT
        assert exc.detail == "Resource conflict"
    
    def test_custom_message(self):
        """Test exception with custom message"""
        exc = ConflictException("Email already exists")
        assert exc.status_code == status.HTTP_409_CONFLICT
        assert exc.detail == "Email already exists"


class TestExceptionRaising:
    """Test that exceptions can be raised and caught properly"""
    
    def test_raise_not_found(self):
        """Test raising NotFoundException"""
        with pytest.raises(NotFoundException) as exc_info:
            raise NotFoundException("Item not found")
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Item not found"
    
    def test_raise_unauthorized(self):
        """Test raising UnauthorizedException"""
        with pytest.raises(UnauthorizedException) as exc_info:
            raise UnauthorizedException("Token expired")
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Token expired"
    
    def test_raise_forbidden(self):
        """Test raising ForbiddenException"""
        with pytest.raises(ForbiddenException) as exc_info:
            raise ForbiddenException("No permission")
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "No permission"
    
    def test_raise_conflict(self):
        """Test raising ConflictException"""
        with pytest.raises(ConflictException) as exc_info:
            raise ConflictException("Duplicate entry")
        assert exc_info.value.status_code == 409
        assert exc_info.value.detail == "Duplicate entry"
