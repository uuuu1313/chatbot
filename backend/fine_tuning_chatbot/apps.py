from django.apps import AppConfig


class FineTuningChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # 자동 증가 필드 설정
    name = 'fine_tuning_chatbot' # 앱 이름 설정

    def ready(self): # django가 앱을 로드한 후에 실행되는 초기화 메서드
        import fine_tuning_chatbot.signals  # 앱이 로드 될때 fine_tuning_chatbot의 signals.py를 임포트함