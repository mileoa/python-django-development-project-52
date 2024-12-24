from django.views.generic import TemplateView
from django.shortcuts import render

class MainIndexView(TemplateView):

    def get(self, request):
        return render(request, 'index.html')