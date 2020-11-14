# _*_ coding: utf-8 _*_

from functools import wraps

from flask import Flask, Response, abort, json, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from admin.Admin import start_views
from config import app_active, app_config
from controller.Product import ProductController
from controller.User import UserController

config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__, template_folder="templates")
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FLASK_ADMIN_SWATCH"] = "paper"

    Bootstrap(app)

    db = SQLAlchemy(config.APP)
    start_views(app, db)

    db.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("access-Control-Allow-Headers", "Content-Type")
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args, **kwargs):
            user = UserController()

            try:
                result = user.verify_auth_token(request.headers["access_token"])

                if result["status"] == 200:
                    return f(*args, **kwargs)

                else:
                    abort(result["status"], result["message"])

            except KeyError as e:
                abort(401, "Você precisa enviar um token de acesso")

        return verify_token

    @app.route("/")
    def index():
        return "Hello world!"

    # Login
    @app.route("/login")
    def login():
        return render_template(
            "login.html", message="Essa é uma mensagem que veio da rota"
        )

    @app.route("/login", methods=["POST"])
    def login_post():
        user = UserController()
        email = request.form["email"]
        password = request.form["password"]
        result = user.login(email, password)

        if result:
            return redirect("/admin")
        else:
            return render_template(
                "login.html",
                data={"status": 401, "msg": "Dados incorretos", "type": None},
            )

    # Produtos
    @app.route("/product", methods=["POST"])
    def save_products():
        product = ProductController()
        result = product.save_product(request.form)
        message = "Inserido" if result else "Não inserido"

        return message

    @app.route("/product", methods=["PUT"])
    def update_products():
        product = ProductController()
        result = product.update_product(request.form)
        message = "Editado" if result else "Não editado"

        return message

    # Recuperação de senha
    @app.route("/recovery-password")
    def recovery_password():
        return "Aqui entrará a tela de recuperar senha"

    @app.route("/recovery-password/", methods=["POST"])
    def send_recovery_password():
        user = UserController()
        result = user.recovery(request.form["email"])

        if result:
            return render_template(
                "recovery.html",
                data={
                    "status": 200,
                    "msg": "E-mail de recuperação enviado com sucesso",
                },
            )

        else:
            return render_template(
                "recovery.html",
                data={"status": 401, "msg": "Erro ao enviar o e-mail de recuperação"},
            )

    @app.route("/products", methods=["GET"])
    @app.route("/products/<limit>", methods=["GET"])
    @auth_token_required
    def get_products(limit=None):
        header = {"access_token": request.headers["access_token"], "token_type": "JWT"}

        product = ProductController()
        response = product.get_products(limit=limit)

        return (
            Response(
                json.dumps(response, ensure_ascii=False), mimetype="application/json"
            ),
            response["status"],
            header,
        )

    @app.route("/product/<product_id>", methods=["GET"])
    @auth_token_required
    def get_product(product_id):
        header = {"access_token": request.headers["access_token"], "token_type": "JWT"}

        product = ProductController()
        response = product.get_product_by_id(product_id=product_id)

        return (
            Response(
                json.dumps(response, ensure_ascii=False), mimetype="application/json"
            ),
            response["status"],
            header,
        )

    @app.route("/user/<user_id>", methods=["GET"])
    @auth_token_required
    def get_user_profile(user_id):
        header = {"access_token": request.headers["access_token"], "token_type": "JWT"}

        user = UserController()
        response = user.get_user_by_id(user_id=user_id)

        return (
            Response(
                json.dumps(response, ensure_ascii=False), mimetype="application/json"
            ),
            response["status"],
            header,
        )

    @app.route("/login_api", methods=["POST"])
    def login_api(self):
        header = {}
        user = UserController()

        email = request.json["email"]
        password = request.json["password"]

        result = user.login(email, password)
        code = 401

        response = {"message": "Usuário não autorizado", "result": []}

        if result:
            if result.active:
                result = {
                    "id": result.id,
                    "username": result.username,
                    "email": result.email,
                    "date_created": result.date_created,
                    "active": result.active,
                }

                header = {
                    "access_token": user.generate_auth_token(result),
                    "token_type": "JWT",
                }

                code = 200
                response["message"] = "Login realizado com sucesso"
                response["result"] = result

                return (
                    Response(
                        json.dumps(response, ensure_ascii=False),
                        mimetype="application/json",
                    ),
                    code,
                    header,
                )

    return app
