from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    FineTunedModelViewSet,
    TrainingDataViewSet,
)

router = DefaultRouter()    # DefaultRouter의 인스턴스를 생성, DRF 라우터 클래스 중 하나로, 뷰셋을 자동으로 URL 패턴에 매핑해줌
# FineTunedModelViewSet 뷰셋을 fine_tuned_models 경로에 등록함, fine_tuned_models/ 경로에 대한 CRUD엔트포인트가 자동생성됨
router.register(r'fine_tuned_models', FineTunedModelViewSet)
# TrainingDataViewSet 뷰셋을 training_data 경로에 등록함, training_data/ 경로에 대한 CRUD 엔드포인트가 자동으로 생성됨
router.register(r'training_data', TrainingDataViewSet)

urlpatterns = [
    path('hello/', views.hello_world),
    path('', include(router.urls)), # ''경로에 대해 router.urls를 포함함, 현재는 fine_tuned_models/ 경로와 training_data/ 경로
]