"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup).
"""

import pytest


class TestSignupForActivity:
    """Test cases for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """
        Test successful signup for an activity.
        
        Arrange: Prepare a new email for signup to an existing activity
        Act: Make a POST request to signup
        Assert: Verify success response and participant added
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "new_student@mergington.edu"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert new_email in response.json()["message"]
        
        # Verify participant was added
        verify_response = client.get("/activities")
        new_count = len(verify_response.json()[activity_name]["participants"])
        assert new_count == initial_count + 1
        assert new_email in verify_response.json()[activity_name]["participants"]

    def test_signup_duplicate_email(self, client):
        """
        Test that signup fails when student already signed up.
        
        Arrange: Sign up a student, then attempt signup again
        Act: Attempt to sign up the same student twice
        Assert: Verify error response on second attempt
        """
        # Arrange
        activity_name = "Drama Club"
        duplicate_email = "duplicate_test@mergington.edu"
        
        # Sign up the student first time - should succeed
        first_response = client.post(f"/activities/{activity_name}/signup", params={"email": duplicate_email})
        assert first_response.status_code == 200
        
        # Act - Attempt to sign up again
        response = client.post(f"/activities/{activity_name}/signup", params={"email": duplicate_email})
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_invalid_activity(self, client):
        """
        Test that signup fails for non-existent activity.
        
        Arrange: Use an activity name that doesn't exist
        Act: Attempt to sign up to invalid activity
        Assert: Verify 404 error response
        """
        # Arrange
        invalid_activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_to_full_activity(self, client):
        """
        Test signup behavior when activity reaches max capacity.
        
        Arrange: Find or create an activity near max capacity, then add students
        Act: Sign up students until capacity is reached, then try one more
        Assert: Verify signup succeeds even if exceeds max (system allows overfilling)
        """
        # Arrange
        # Using a small activity: Math Olympiad has max_participants=12
        activity_name = "Math Olympiad"
        
        # Get current participants
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]
        max_capacity = initial_response.json()[activity_name]["max_participants"]
        
        # Act - signup new students up to and beyond capacity
        emails_to_add = [f"overflow_student_{i}@mergington.edu" for i in range(max_capacity)]
        
        for email in emails_to_add:
            response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
            # Note: API allows exceeding max capacity without error (no validation on max)
            assert response.status_code == 200
        
        # Assert - all signups were successful
        verify_response = client.get("/activities")
        final_participants = verify_response.json()[activity_name]["participants"]
        assert len(final_participants) == len(initial_participants) + len(emails_to_add)

    def test_signup_response_structure(self, client):
        """
        Test that signup response has correct structure.
        
        Arrange: Prepare a new email
        Act: Make a POST request to signup
        Assert: Verify response contains expected message field
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "response_test@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert isinstance(response_data["message"], str)
