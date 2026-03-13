def test_get_activities(client):
    """Test retrieving all activities"""
    # Arrange - activities are reset to initial state by fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Should have 9 activities
    assert "Chess Club" in data

    # Check structure of one activity
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == f"Signed up {email} for {activity_name}"

    # Verify the student was added
    response2 = client.get("/activities")
    activities = response2.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate(client):
    """Test signing up for an activity when already enrolled"""
    # Arrange
    email = "michael@mergington.edu"  # Already enrolled in Chess Club
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == f"Already signed up for {activity_name}"


def test_signup_invalid_activity(client):
    """Test signing up for a non-existent activity"""
    # Arrange
    email = "test@mergington.edu"
    activity_name = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Activity not found"


def test_unregister_success(client):
    """Test successful unregistration from an activity"""
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == f"Unregistered {email} from {activity_name}"

    # Verify the student was removed
    response2 = client.get("/activities")
    activities = response2.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_not_enrolled(client):
    """Test unregistering from an activity when not enrolled"""
    # Arrange
    email = "notenrolled@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == f"Not signed up for {activity_name}"


def test_unregister_invalid_activity(client):
    """Test unregistering from a non-existent activity"""
    # Arrange
    email = "test@mergington.edu"
    activity_name = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Activity not found"


def test_root_redirect(client):
    """Test root endpoint redirects to static index"""
    # Arrange - no special setup needed

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"