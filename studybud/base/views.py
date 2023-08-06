from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

rooms = [
  {'id': 1, 'name': 'Lets learn python!'},
  {'id': 2, 'name': 'Design with Me'},
  {'id': 3, 'name': 'Frontend Developers'},
]

def home(request):
  context = {'rooms': rooms}
  return render(request, 'base/home.html', context)

def room(request, pk):
  room = None
  for r in rooms:
    if r['id'] == int(pk):
      room = r
  context = {'room': room}
  return render(request, 'base/room.html', context)
