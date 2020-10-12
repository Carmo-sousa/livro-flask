from model.User import User


class UserController:
    def __init__(self):
        self.user_model = User()

    def login(self, email, password):
        self.user_model.email = email
        result = self.user_model.get_user_by_email()

        if result is not None:
            res = self.user_model.verify_password(password, result.password)
            return result if res else {}
        return {}

    def recovery(self, email):
        return ""

    def get_user_by_id(self, user_id):
        result = {}

        try:
            self.user_model.id = user_id
            res = self.user_model.get_user_by_id()
            result = {
                "id": res.id,
                "name": res.username,
                "email": res.email,
                "date_created": res.date_created,
            }
            status = 200

        except Exception as e:
            print(e)
            result = []
            status = 400

        finally:
            return {"result": result, "status": status}
