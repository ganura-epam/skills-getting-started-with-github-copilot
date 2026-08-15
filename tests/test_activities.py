"""Tests for GET /activities endpoint."""
import pytest


class TestGetActivities:
    """Test suite for fetching activities."""
    
    def test_get_activities_returns_success(self, client, reset_activities):
        """
        Arrange: Make a GET request to /activities
        Act: Call the endpoint
        Assert: Verify status code is 200
        """
        # Arrange & Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        Arrange: GET /activities endpoint
        Act: Call the endpoint
        Assert: Verify response contains all 9 activities
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
        assert "Basketball Team" in activities
        assert "Tennis Club" in activities
        assert "Art Studio" in activities
        assert "Drama Club" in activities
        assert "Debate Team" in activities
        assert "Science Club" in activities
    
    def test_activity_has_required_fields(self, client, reset_activities):
        """
        Arrange: GET /activities endpoint
        Act: Call the endpoint
        Assert: Verify each activity has required fields (description, schedule, max_participants, participants)
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert: Check Chess Club as representative example
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
    
    def test_participants_is_list(self, client, reset_activities):
        """
        Arrange: GET /activities endpoint
        Act: Call the endpoint
        Assert: Verify participants field is a list
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity in activities.items():
            assert isinstance(activity["participants"], list), \
                f"{activity_name} participants should be a list"
    
    def test_participants_contain_emails(self, client, reset_activities):
        """
        Arrange: GET /activities endpoint
        Act: Call the endpoint
        Assert: Verify participants list contains email addresses
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert: Chess Club has 2 participants
        chess_club_participants = activities["Chess Club"]["participants"]
        assert len(chess_club_participants) == 2
        assert "michael@mergington.edu" in chess_club_participants
        assert "daniel@mergington.edu" in chess_club_participants
    
    def test_max_participants_is_integer(self, client, reset_activities):
        """
        Arrange: GET /activities endpoint
        Act: Call the endpoint
        Assert: Verify max_participants is an integer
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity in activities.items():
            assert isinstance(activity["max_participants"], int), \
                f"{activity_name} max_participants should be an integer"
            assert activity["max_participants"] > 0
