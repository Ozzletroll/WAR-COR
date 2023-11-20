from warcor.app import create_app
from config import ProductionConfig

app = create_app()


# Development
if __name__ == "__main__":
    app.run(debug=True)

# Production
# If using gunicorn, bind using:
# gunicorn --bind 127.0.0.1:5000 appserver:production_app

else:
    production_app = create_app()
