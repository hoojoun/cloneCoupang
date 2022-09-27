"""
My module
~~~~~~~
"""

from django.apps import AppConfig

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    """두 개의 int 값을 입력받아 다양한 연산을 할 수 있도록 하는 클래스.
    """
    def ready(self):
        import account.signal
