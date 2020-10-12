import os


class Config:
    CSRF_ENABLED = True
    SECRET = r"ysb_92=qe#djf8%ng+a*#4rt#5%3*4k5%i2bck*gn@w3@f&-&"
    TEMPLATE_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates"
    )
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://romulo:199718@localhost:3306/livro_flask"


class DeveloperConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = "localhost"
    PORT_HOST = 8000
    URL_MAIN = f"http://{IP_HOST}:{PORT_HOST}"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = "localhost"
    PORT_HOST = 5000
    URL_MAIN = f"http://{IP_HOST}:{PORT_HOST}"


class ProductConfig(Config):
    TESTING = False
    DEBUG = False
    IP_HOST = "localhost"
    PORT_HOST = 8080
    URL_MAIN = f"http://{IP_HOST}:{PORT_HOST}"


app_config = {
    "development": DeveloperConfig(),
    "testing": TestingConfig(),
    "production": ProductConfig(),
}

app_active = os.getenv("FLASK_ENV")
