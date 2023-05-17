from flask import Flask, render_template, redirect, request, url_for, flash, abort, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import UserMixin, login_user, login_required, current_user, logout_user
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

import forms
import models
from app import create_app
from app import db
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

