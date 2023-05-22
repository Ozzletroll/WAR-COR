from app import create_app
from routes import configure_routes

flask_app = create_app()
configure_routes(flask_app)

if __name__ == "__main__":
    flask_app.run(debug=False)

