"""
Tests for the root endpoint (GET /).
"""

import pytest


class TestRoot:
    """Test cases for GET / endpoint."""

    def test_root_redirect(self, client):
        """
        Test that the root endpoint redirects to /static/index.html.
        
        Arrange: Prepare the test client
        Act: Make a GET request to /
        Assert: Verify redirect status code and location
        """
        # Arrange
        # Client is already prepared by the fixture
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code in [307, 308]  # Temporary or permanent redirect
        assert "/static/index.html" in response.headers.get("location", "")

    def test_root_response_with_follow_redirects(self, client):
        """
        Test that following the redirect from root returns the HTML file.
        
        Arrange: Prepare the test client
        Act: Make a GET request to / and follow redirects
        Assert: Verify successful response
        """
        # Arrange
        # Client is already prepared by the fixture
        
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
