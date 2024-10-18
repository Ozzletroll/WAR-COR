from flask_minify import Minify
from app import create_app
from config import ProductionConfig

# Production
# If using gunicorn, bind using:
# gunicorn --bind 0.0.0.0:5000 wsgi:production_app

production_app = create_app(ProductionConfig)
Minify(app=production_app, html=True, js=True, cssless=True)
