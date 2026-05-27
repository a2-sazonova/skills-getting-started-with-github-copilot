"""
Tests for the participants endpoint (DELETE /activities/{activity_name}/participants).
"""

import pytest


class TestRemoveParticipant:
    """Test cases for DELETE /activities/{activity_name}/participants endpoint."""

    def test_remove_participant_success(self, client):
        """
        Test successful removal of a participant from an activity.
        
        Arrange: Get an existing participant from an activity
        Act: Make a DELETE request to remove the participant
        Assert: Verify success response and participant removed
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"  # Exists in Chess Club
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants", params={"email": email_to_remove})
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email_to_remove in response.json()["message"]
        
        # Verify participant was removed
        verify_response = client.get("/activities")
        new_count = len(verify_response.json()[activity_name]["participants"])
        assert new_count == initial_count - 1
        assert email_to_remove not in verify_response.json()[activity_name]["participants"]

    def test_remove_nonexistent_participant(self, client):
        """
        Test that removal fails when participant is not in the activity.
        
        Arrange: Use an email that is not a participant in the activity
        Act: Attempt to remove non-existent participant
        Assert: Verify 404 error response
        """
        # Arrange
        activity_name = "Soccer Team"
        email_not_in_activity = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants", params={"email": email_not_in_activity})
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_remove_from_invalid_activity(self, client):
        """
        Test that removal fails for non-existent activity.
        
        Arrange: Use an activity name that doesn't exist
        Act: Attempt to remove participant from invalid activity
        Assert: Verify 404 error response
        """
        # Arrange
        invalid_activity = "Fake Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{invalid_activity}/participants", params={"email": email})
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_response_structure(self, client):
        """
        Test that removal response has correct structure.
        
        Arrange: Get an existing participant
        Act: Make a DELETE request
        Assert: Verify response contains expected message field
        """
        # Arrange
        activity_name = "Programming Class"
        email_to_remove = "emma@mergington.edu"  # Exists in Programming Class
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants", params={"email": email_to_remove})
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert isinstance(response_data["message"], str)

    def test_remove_participant_twice_fails(self, client):
        """
        Test that removing the same participant twice fails on the second attempt.
        
        Arrange: Remove a participant once (success)
        Act: Attempt to remove the same participant again
        Assert: Verify error response on second removal
        """
        # Arrange
        activity_name = "Swimming Club"
        email = "oliver@mergington.edu"  # Exists in Swimming Club
        
        # First removal - should succeed
        first_response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
        assert first_response.status_code == 200
        
        # Act - Second removal attempt
        second_response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
        
        # Assert
        assert second_response.status_code == 404
        assert "Participant not found" in second_response.json()["detail"]
