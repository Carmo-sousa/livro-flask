# _*_ coding: utf-8 _*_

from config import app_active, app_config
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

config = app_config[app_active]


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('home_admin.html', data={'username': 'Metatron'})


class UserView(ModelView):
    form_excluded_columns = ['last_update', 'recovery_code']
    column_exclude_list = ['password', 'recovery_code']
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email', 'funcao']
    column_editable_list = ['username', 'email', 'funcao', 'active']
    column_sortable_list = ['username']
    column_details_exclude_list = ['password', 'recovery_mode']
    column_export_exclude_list = ['password', 'recovery_mode']
    column_default_sort = ('username', True)
    export_types = ['json', 'yaml', 'csv', 'xls', 'df']

    create_modal = True
    edit_modal = True
    can_set_page_size = True
    can_view_details = True
    can_export = True

    form_widget_args = {
        'password': {
            'type': 'password'
        }}

    column_labels = {
        'funcao': 'Função',
        'username': 'Nome de usuário',
        'email': 'E-mail',
        'date_created': 'Data de criação',
        'last_update': 'Última atualisação',
        'active': 'Ativo',
        'password': 'Senha'
    }

    column_descriptions = {
        'funcao': 'Função no painel administrativo',
        'username': 'Nome de usuário no sistema',
        'email': 'E-mail do  usuário no sistema',
        'date_created': 'Data de criação do usuário no sistema',
        'last_update': 'Última atualisação desse usuário no sistema',
        'active': 'Estado ativo ou inativo no sistema',
        'password': 'Senha do usuário no sistema'
    }

    def on_model_change(self, form, User, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password
