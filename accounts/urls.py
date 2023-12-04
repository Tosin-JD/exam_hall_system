from django.urls import path
from .views import StudentSignUpView, InvigilatorSignUpView, CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/invigilator/', InvigilatorSignUpView.as_view(), name='invigilator_signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # Add other URLs as needed
]