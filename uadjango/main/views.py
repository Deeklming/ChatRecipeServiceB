from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse


class Index(View):
    def get(self, req):
        return HttpResponse("Hello, world. Test OK!")