from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse


class MessagesView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        return render(request, 'text_messages/messages_create.html')
