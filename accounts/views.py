from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth import login, authenticate

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            # return redirect()
            pass
    def post(self, request):
        pass
