from django.shortcuts import render
from django.views import View

class IndexView(View):

    def get(self,request,*args,**kwargs):
        return render(request,"chat/index.html")

index   = IndexView.as_view()

class RoomView(View):

    def get(self,request, room_name, *args,**kwargs):
        context = {}
        context["room_name"]    = room_name

        return render(request,"chat/room.html",context)

room    = RoomView.as_view()

