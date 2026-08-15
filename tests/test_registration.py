"""Tests for POST /activities/{activity_name}/signup endpoint."""
import pytest


class TestSignup:
    """Test suite for activity signup functionality."""
    
    def test_signup_valid_activity_and_email_returns_success(self, client, reset_activities, new_email):
        """
        Arrange: Valid activity name and new student email
        Act: POST to /activities/Chess Club/signup with new email
        Assert: Verify status code is 200 and message is returned
        """
        # Arrange
        activity = "Chess Club"
        
        # Act
        response = client.post(f"/activities/{activity}/signup", params={"email": new_email})
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert new_email in data["message"]
        assert activity in data["message"]
    
    def test_signup_adds_participant_to_activity(self, client, reset_activities, new_email):
        """
        Arrange: Valid activity and new email, signup user
        Act: GET /activities and check the activity's participants
        Assert: Verify new participant appears in participants list
        """
        # Arrange
        activity = "Chess Club"
        
        # Act: Sign up
        client.post(f"/activities/{activity}/signup", params={"email": new_email})
        
        # Act: Fetch activities
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        participants = activities[activity]["participants"]
        assert new_email in participants
    
    def test_signup_duplicate_email_returns_400(self, client, reset_activities, existing_email):
        """
        Arrange: Valid activity with participant already signed up
        Act: Try to sign up the same email again
        Assert: Verify status code is 400 and error message about already signed up
        """
        # Arrange
        activity = "Chess Club"
        # existing_email ("michael@mergington.edu") is already in Chess Club
        
        # Act
        response = client.post(f"/activities/{activity}/signup", params={"email": existing_email})
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Already signed up" in data["detail"]
    
    def test_signup_activity_not_found_returns_404(self, client, reset_activities, new_email):
        """
        Arrange: Nonexistent activity name
        Act: Try to sign up for nonexistent activity
        Assert: Verify status code is 404 and activity not found error
        """
        # Arrange
        activity = "Nonexistent Activity"
        
        # Act
        response = client.post(f"/activities/{activity}/signup", params={"email": new_email})
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_signup_missing_email_param_returns_422(self, client, reset_activities):
        """
        Arrange: Valid activity but missing email query parameter
        Act: Try to sign up without email parameter
        Assert: Verify status code is 422 (validation error)
        """
        # Arrange
        activity = "Chess Club"
        
        # Act
        response = client.post(f"/activities/{activity}/signup")
        
        # Assert
        assert response.status_code == 422
    
    def test_signup_multiple_students_same_activity(self, client, reset_activities, new_email):
        """
        Arrange: Multiple different students signing up for same activity
        Act: Sign up multiple new emails for Chess Club
        Assert: Verify all participants are in the list
        """
        # Arrange
        activity = "Chess Club"
        email_1 = "student1@mergington.edu"
        email_2 = "student2@mergington.edu"
        
        # Act: Sign up both emails
        client.post(f"/activities/{activity}/signup", params={"email": email_1})
        client.post(f"/activities/{activity}/signup", params={"email": email_2})
        
        # Act: Fetch activities
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        participants = activities[activity]["participants"]
        assert email_1 in participants
        assert email_2 in participants
        # Original participants should still be there
        assert "michael@mergington.edu" in participants
        assert "daniel@mergington.edu" in participants
    
    def test_signup_different_activities_same_email(self, client, reset_activities, new_email):
        """
        Arrange: Same student signing up for multiple activities
        Act: Sign up same email for Chess Club and Programming Class
        Assert: Verify student appears in both activities
        """
        # Arrange
        email = new_email
        activity_1 = "Chess Club"
        activity_2 = "Programming Class"
        
        # Act: Sign up for both activities
        client.post(f"/activities/{activity_1}/signup", params={"email": email})
        client.post(f"/activities/{activity_2}/signup", params={"email": email})
        
        # Act: Fetch activities
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email in activities[activity_1]["participants"]
        assert email in activities[activity_2]["participants"]
