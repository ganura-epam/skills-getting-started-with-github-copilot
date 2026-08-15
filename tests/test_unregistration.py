"""Tests for POST /activities/{activity_name}/unregister endpoint."""
import pytest


class TestUnregister:
    """Test suite for activity unregistration functionality."""
    
    def test_unregister_valid_activity_and_email_returns_success(self, client, reset_activities, existing_email):
        """
        Arrange: Valid activity and email that is registered
        Act: POST to /activities/Chess Club/unregister
        Assert: Verify status code is 200 and success message returned
        """
        # Arrange
        activity = "Chess Club"
        # existing_email ("michael@mergington.edu") is already in Chess Club
        
        # Act
        response = client.post(f"/activities/{activity}/unregister", params={"email": existing_email})
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
    
    def test_unregister_removes_participant_from_activity(self, client, reset_activities, existing_email):
        """
        Arrange: Valid activity and registered email, unregister user
        Act: GET /activities and check participants
        Assert: Verify participant no longer appears in participants list
        """
        # Arrange
        activity = "Chess Club"
        # existing_email ("michael@mergington.edu") is already in Chess Club
        
        # Act: Unregister
        client.post(f"/activities/{activity}/unregister", params={"email": existing_email})
        
        # Act: Fetch activities
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        participants = activities[activity]["participants"]
        assert existing_email not in participants
    
    def test_unregister_email_not_registered_returns_400(self, client, reset_activities, new_email):
        """
        Arrange: Valid activity but email not registered
        Act: Try to unregister an email that's not in the activity
        Assert: Verify status code is 400 and error about not being registered
        """
        # Arrange
        activity = "Chess Club"
        # new_email is not registered for any activity
        
        # Act
        response = client.post(f"/activities/{activity}/unregister", params={"email": new_email})
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Not registered" in data["detail"]
    
    def test_unregister_activity_not_found_returns_404(self, client, reset_activities, existing_email):
        """
        Arrange: Nonexistent activity name
        Act: Try to unregister from nonexistent activity
        Assert: Verify status code is 404 and activity not found error
        """
        # Arrange
        activity = "Nonexistent Activity"
        
        # Act
        response = client.post(f"/activities/{activity}/unregister", params={"email": existing_email})
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_unregister_missing_email_param_returns_422(self, client, reset_activities):
        """
        Arrange: Valid activity but missing email query parameter
        Act: Try to unregister without email parameter
        Assert: Verify status code is 422 (validation error)
        """
        # Arrange
        activity = "Chess Club"
        
        # Act
        response = client.post(f"/activities/{activity}/unregister")
        
        # Assert
        assert response.status_code == 422
    
    def test_unregister_other_participants_remain(self, client, reset_activities, existing_email, existing_email_2):
        """
        Arrange: Activity with multiple participants, unregister one
        Act: Unregister one participant
        Assert: Verify other participants remain in the list
        """
        # Arrange
        activity = "Chess Club"
        # existing_email ("michael@mergington.edu") is in Chess Club
        # existing_email_2 ("daniel@mergington.edu") is also in Chess Club
        
        # Act: Unregister first email
        client.post(f"/activities/{activity}/unregister", params={"email": existing_email})
        
        # Act: Fetch activities
        response = client.get("/activities")
        activities = response.json()
        
        # Assert: First email should be gone, second should remain
        participants = activities[activity]["participants"]
        assert existing_email not in participants
        assert existing_email_2 in participants
    
    def test_signup_then_unregister_workflow(self, client, reset_activities, new_email):
        """
        Arrange: New student signs up for activity
        Act: Sign up, verify in list, then unregister
        Assert: Verify student is removed from activity
        """
        # Arrange
        activity = "Chess Club"
        email = new_email
        
        # Act: Sign up
        client.post(f"/activities/{activity}/signup", params={"email": email})
        
        # Act: Verify signup
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]
        
        # Act: Unregister
        unregister_response = client.post(f"/activities/{activity}/unregister", params={"email": email})
        assert unregister_response.status_code == 200
        
        # Act: Verify unregister
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]
    
    def test_unregister_from_different_activities(self, client, reset_activities, new_email):
        """
        Arrange: Student signed up for multiple activities
        Act: Unregister from one activity, verify stays in others
        Assert: Student only removed from the specified activity
        """
        # Arrange
        email = new_email
        activity_1 = "Chess Club"
        activity_2 = "Programming Class"
        
        # Act: Sign up for both
        client.post(f"/activities/{activity_1}/signup", params={"email": email})
        client.post(f"/activities/{activity_2}/signup", params={"email": email})
        
        # Act: Unregister from activity 1
        client.post(f"/activities/{activity_1}/unregister", params={"email": email})
        
        # Act: Fetch activities
        response = client.get("/activities")
        activities = response.json()
        
        # Assert: Removed from activity 1, but still in activity 2
        assert email not in activities[activity_1]["participants"]
        assert email in activities[activity_2]["participants"]
