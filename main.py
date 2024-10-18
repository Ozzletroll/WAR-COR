from app import create_app
from flask_minify import Minify


app = create_app()
Minify(app=app, html=True, js=True, cssless=True)

# Development
if __name__ == "__main__":
    app.run(debug=True)
