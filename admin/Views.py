# _*_ coding: utf-8 _*_

from config import app_active, app_config
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from model.Category import Category
from model.Product import Product
from model.User import User

config = app_config[app_active]


class HomeView(AdminIndexView):
    extra_css = [
        config.URL_MAIN + "/static/css/home.css",
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    ]

    @expose("/")
    def index(self):
        user_model = User()
        product_model = Product()
        category_model = Category()

        users = user_model.get_total_users()
        products = product_model.get_total_products()
        categories = category_model.get_total_categories()
        last_products = product_model.get_last_products()

        return self.render(
            "home_admin.html",
            report={
                "users": 0 if not users else users[0],
                "products": 0 if not products else products[0],
                "categories": 0 if not categories else categories[0],
            },
            last_products=last_products,
        )


class UserView(ModelView):
    form_excluded_columns = ["last_update", "recovery_code"]
    column_exclude_list = ["password", "recovery_code"]
    column_searchable_list = ["username", "email"]
    column_filters = ["username", "email", "funcao"]
    column_editable_list = ["username", "email", "funcao", "active"]
    column_sortable_list = ["username"]
    column_details_exclude_list = ["password", "recovery_mode"]
    column_export_exclude_list = ["password", "recovery_mode"]
    column_default_sort = ("username", True)
    export_types = ["json", "yaml", "csv", "xls", "df"]

    create_modal = True
    edit_modal = True
    can_set_page_size = True
    can_view_details = True
    can_export = True

    form_widget_args = {"password": {"type": "password"}}

    column_labels = {
        "funcao": "Função",
        "username": "Nome de usuário",
        "email": "E-mail",
        "date_created": "Data de criação",
        "last_update": "Última atualisação",
        "active": "Ativo",
        "password": "Senha",
    }

    column_descriptions = {
        "funcao": "Função no painel administrativo",
        "username": "Nome de usuário no sistema",
        "email": "E-mail do  usuário no sistema",
        "date_created": "Data de criação do usuário no sistema",
        "last_update": "Última atualisação desse usuário no sistema",
        "active": "Estado ativo ou inativo no sistema",
        "password": "Senha do usuário no sistema",
    }

    def on_model_change(self, form, User, is_created):
        if "password" in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password
