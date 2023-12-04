from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser, Student, Invigilator

# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + ("custom_field",)

        
class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields
        
        
class InvigilatorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Invigilator
        fields = UserCreationForm.Meta.fields