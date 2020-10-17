from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import models

User = get_user_model()


class Auth(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user')
    confirmation_code = models.CharField('confirmation_code',
                                         max_length=128)
    email = models.EmailField('email',
                              unique=True,
                              null=False,
                              blank=False)

    def __str__(self):
        return self.email

    def set_confirmation_code(self, raw_confirmation_code):
        self.confirmation_code = make_password(raw_confirmation_code)

    def check_confirmation_code(self, raw_confirmation_code):
        return check_password(raw_confirmation_code, self.confirmation_code)

    def send_email(self, email, raw_confirmation_code):
        send_mail(
            'Yamdb registration',
            f'You confirmation code is <b>{raw_confirmation_code}</b>',
            'yamdb@support.com',
            [f'{email}'],
            fail_silently=False,
        )
