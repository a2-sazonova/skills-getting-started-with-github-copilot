"""
Tests for the activities endpoint (GET /activities).
"""

import pytest


class TestGetActivities:
    """Test cases for GET /activities endpoint."""

    def test_get_all_activities(self, client):
        """
        Test that GET /activities returns all available activities.
        
        Arrange: Prepare the test client
        Act: Make a GET request to /activities
        Assert: Verify response contains activities with correct structure
        """
        # Arrange
        # Client is already prepared by the fixture
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0

    def test_activities_have_required_fields(self, client):
        """
        Test that each activity has all required fields.
        
        Arrange: Prepare the test client
        Act: Make a GET request to /activities
        Assert: Verify each activity contains required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str), "Activity name should be a string"
            assert isinstance(activity_data, dict), "Activity data should be a dictionary"
            for field in required_fields:
                assert field in activity_data, f"Missing field '{field}' in activity '{activity_name}'"

    def test_activities_structure_validity(self, client):
        """
        Test that activity structure has valid data types.
        
        Arrange: Prepare the test client
        Act: Make a GET request to /activities
        Assert: Verify data types of activity fields
        """
        # Arrange
        # Client is already prepared by the fixture
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
            assert activity_data["max_participants"] > 0

    def test_activities_participants_are_emails(self, client):
        """
        Test that all participants in activities have email addresses.
        
        Arrange: Prepare the test client
        Act: Make a GET request to /activities
        Assert: Verify all participants appear to be email addresses
        """
        # Arrange
        # Client is already prepared by the fixture
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant, f"Participant '{participant}' in '{activity_name}' doesn't appear to be an email"
