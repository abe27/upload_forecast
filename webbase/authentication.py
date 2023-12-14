from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class LoginBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("Authenticating")
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        print("Getting user")
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
            # request_validation.change_app_name(user)
            return user
        except UserModel.DoesNotExist:
            return None
