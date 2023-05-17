from app import create_app
from routes import configure_routes

# Initial setup:
# TODO: Create and style page templates
#     TODO: Create index.html
#     TODO: Create register.html
#     TODO: Create login.html
#     TODO: Create user_settings.html
#     TODO: Create timeline.html
#     TODO: Create new_campaign.html
#     TODO: Create edit_campaign.html
#     TODO: Create event.html
#     TODO: Create new_event.html
#     TODO: Create edit_event.html

# TODO: Implement basic page navigation
# TODO: Implement user login/logout functionality

# TODO: Main functionality
#   TODO: Add campaign creation
#   TODO: Add campaign viewing
#   TODO: Add campaign editing
#   TODO: Add campaign deletion
#   TODO: Add campaign user invitation

#   TODO: Add event creation
#   TODO: Add event viewing
#   TODO: Add event editing
#   TODO: Add event deletion
#   TODO: Add event commenting

flask_app = create_app()
configure_routes(flask_app)

if __name__ == "__main__":
    flask_app.run(debug=False)

