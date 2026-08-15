"""Shared pytest fixtures for FastAPI tests."""
import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module
from src.app import app


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for testing."""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Provide a deep copy of activities for each test.
    Ensures test isolation - changes in one test don't affect others.
    """
    return copy.deepcopy(app_module.activities)


@pytest.fixture
def reset_activities(fresh_activities):
    """
    Reset the activities dict to a fresh state before each test.
    This allows the app to use the fresh copy during the test.
    """
    # Store original activities
    original = copy.deepcopy(app_module.activities)
    
    # Replace with fresh copy
    app_module.activities.clear()
    app_module.activities.update(fresh_activities)
    
    yield  # Test runs here
    
    # Restore original state after test
    app_module.activities.clear()
    app_module.activities.update(original)


# Test data: Common email addresses used across tests
TEST_EMAIL_NEW = "newstudent@mergington.edu"
TEST_EMAIL_EXISTING = "michael@mergington.edu"  # Already in Chess Club
TEST_EMAIL_EXISTING_2 = "daniel@mergington.edu"  # Already in Chess Club


@pytest.fixture
def new_email():
    """Provide a test email address not registered for any activity."""
    return TEST_EMAIL_NEW


@pytest.fixture
def existing_email():
    """Provide a test email address already registered in an activity."""
    return TEST_EMAIL_EXISTING


@pytest.fixture
def existing_email_2():
    """Provide another test email address already registered in an activity."""
    return TEST_EMAIL_EXISTING_2
