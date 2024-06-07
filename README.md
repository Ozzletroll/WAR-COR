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
    .
    <a href="https://github.com/Ozzletroll/WAR-COR/milestones">Roadmap</a>
    ·
    <a href="https://github.com/Ozzletroll/WAR-COR/issues/new?assignees=Ozzletroll&labels=&projects=&template=bug_report.md&title=%5BBUG%5D">Report Bug</a>
    ·
    <a href="https://github.com/Ozzletroll/WAR-COR/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=%5BFEATURE%5D">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## Features
WAR/COR is a dynamic timeline creator, for structured, military-style RPG combat reporting and campaign logging.

- Dynamic timeline creation
    - One-click event placement
    - Freeform event layout using dynamic fields
    - Non-standard calendar support
    - Save/load templates for easy reuse
    - Group events into custom epochs
- Collaborate with players
    - Share editing privileges
    - Set custom callsigns
    - Leave comments
- Locally backup/restore campaign data

### Built With

- Python
- Flask
- Jinja2
- SQLAlchemy
- HTML
- CSS
- Javascript

### Extensions

- Flask-APScheduler
- Flask-Caching
- Flask-Limiter
- Flask-Login
- Flask-Migrate
- Flask-SQLAlchemy
- Flask-WTF
- nh3
- Pytest
- Summernote


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/Ozzletroll/WAR-COR.git
   ```
2. Install with pip:
   ```sh
   pip install -r requirements.txt
   ```
3. Set environment variables:

    ```
    SECRET_KEY=YOUR_SECRET_KEY_HERE
    FLASK_APP=main.py
    ```

4. Run:
   ```sh
   flask --app main run 
   ```

<br>
<br>

  By default, WAR/COR will create a local SQLite database for use during development. However, to more closely mirror the production environment, a PostgreSQL database can be used by updating the environment:

  ```
  POSTGRESQL_DATABASE_URI=postgresql://DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME
  ```



<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Testing
  
1. Setup local PostgreSQL database:

    <a href="https://www.postgresql.org/docs/current/tutorial-install.html">How to install PostgreSQL</a>
    

2. Set environment variables:

    ```
    SECRET_KEY=YOUR_SECRET_KEY_HERE
    FLASK_APP=main.py
    POSTGRESQL_DATABASE_URI=postgresql://DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME
    ```

3. Run pytest:
   ```sh
   pytest .\app\tests\  
   ```

<br>
<br>

  By default, WAR/COR requires a local PostgreSQL database during testing to better match the production environment. If necessary, this can be changed to a local SQLite database by updating your environment:

  ```
  TESTING_USE_SQLITE=True
  ```
  NOTE: Some test cases may behave differently on SQLite.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
