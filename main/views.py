from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    
class AboutView(TemplateView):
    template_name = 'about.html'
    
    
class ContactView(TemplateView):
    template_name = 'contact.html'
    
    
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
