from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# 특정 이벤트가 발생했을때 자동으로 실행되는 함수, 사용자가 생성될 때마다 해당 사용자에 대한 인증 토큰을 자동으로 생성
@receiver(post_save, sender=User) # post_save 신호 발생할때 sender인 User 모델을 DB에 저장후 아래 함수를 발생 시킴
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created: # User 인스턴스가 생성된 경우에만 실행됨
        Token.objects.create(user=instance)