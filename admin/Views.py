# -*- coding: utf-8 -*-

from config import app_active, app_config
from flask_admin.contrib.sqla import ModelView

config = app_config[app_active]


class UserView(ModelView):
    column_exclude_list = ['password', 'recovery_code']
    form_excluded_columns = ['last_update', 'recovery_code']

    form_widget_args = {'password': {
        'type': 'password'
    }}

    def on_model_change(self, form, User, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password
