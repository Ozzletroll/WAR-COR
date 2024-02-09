<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Ozzletroll/WAR-COR">
    <img src="./app/static/images/logo-red.png" alt="Logo" width="45" height="40">
  </a>

<h3 align="center">WAR/COR</h3>

  <p align="center">
    Sci-fi Military RPG Campaign Logger
    <br />
    <a href="https://war-cor.com/">Live Site</a>
    ·
    <a href="https://github.com/Ozzletroll/WAR-COR/issues/new?assignees=Ozzletroll&labels=&projects=&template=bug_report.md&title=%5BBUG%5D">Report Bug</a>
    ·
    <a href="https://github.com/Ozzletroll/WAR-COR/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=%5BFEATURE%5D">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## Features
WAR/COR is a dynamic timeline creator app, for structured, military-style RPG combat reporting and campaign logging.

- Dynamic timeline creation
    - One-click event creation
    - Non-standard calendar support
    - Group events into custom epochs
- Collaborate with players
    - Share editing privileges
    - Set custom callsigns
    - Leave comments

### Built With

- Python
- Flask
- Jinja2
- SQLAlchemy
- HTML
- CSS
- Javascript

### Extensions

- Flask-Login
- Flask-APScheduler
- Flask-Migrate
- Flask-SQLAlchemy
- Flask-WTF
- Pytest


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Ozzletroll/WAR-COR.git
   ```
2. Install with pip:
   ```sh
   pip install -r requirements.txt
   ```
3. Set environment variables:

    .env:
    ```
    SECRET_KEY=YOUR_SECRET_KEY_HERE
    APP_CONFIG_FILE=config.py
    FLASK_APP=main.py
    POSTGRESQL_DATABASE_URI=postgresql://DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME
    ```

    VSCode launch.json:
   ```js
    "APP_CONFIG_FILE": "config.py",
    "FLASK_APP": "main.py",
    "SECRET_KEY": "YOUR_SECRET_KEY_HERE",
    "POSTGRESQL_DATABASE_URI": "postgresql://DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME",
   ```
4. Run:
   ```sh
   flask run --app main
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Testing
  
1. Setup local PostgreSQL database:

    <a href="https://www.postgresql.org/docs/current/tutorial-install.html">How to install PostgreSQL</a>
    

2. Set environment variables:

    .env:
    ```
    SECRET_KEY=YOUR_SECRET_KEY_HERE
    APP_CONFIG_FILE=config.py
    FLASK_APP=main.py
    FLASK_DEBUG=1
    TESTING_USE_POSTGRESQL=True
    POSTGRESQL_DATABASE_URI=postgresql://DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME
    ```

    launch.json:
   ```js
    {
      "name": "Python: Flask Testing",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": [
        "${workspaceFolder}/app/tests"
      ],
      "env": {
        "APP_CONFIG_FILE": "config.py",
        "FLASK_APP": "main.py",
        "SECRET_KEY": "YOUR_SECRET_KEY_HERE",
        "FLASK_DEBUG": "1",
        "TESTING_USE_POSTGRESQL": "POSTGRESQL",
        "POSTGRESQL_DATABASE_URI": "postgresql://DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME",
      }
    }
   ```
3. Run pytest:
   ```sh
   pytest .\app\tests\  
   ```

By default, WAR/COR uses a local PostgreSQL db during testing to better match the production environment. If necessary, this can be changed to a local SQLite instance by updating your environment:

```
TESTING_USE_POSTGRESQL=False
```
NOTE: Some test cases may behave differently on SQLite.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
