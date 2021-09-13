from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse

from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.models import User
from chat.models import Room, Message
from .forms import RegisterUserForm, LoginUserForm

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import MessageListSerializers, MessageViewSerializers, MessageCreateSerializers
from .paginations import CustomPagination


class MessageListView(APIView):
    def get(self, request, pk):
        messag = Message.objects.get(id=pk)
        serialz = MessageListSerializers(messag)
        return Response(serialz.data)


class MessageView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = MessageViewSerializers

    def get_queryset(self):
        return Message.objects.all().order_by('date')


class MessageCreate(APIView):
    def post(self, request):
        messag = MessageCreateSerializers(data=request.data)
        if messag.is_valid():
            messag.save()
        return Response(status=201)


class RegisterUserView(CreateView):
    model = User
    template_name = "register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("home")
    success_msg = "Create new user"

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        aut_user = authenticate(username=username, password=password, email=email)
        login(self.request, aut_user)
        return form_valid


class CreateLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('home')


def home(request):
    room = Room.objects.all()

    return render(request, "home.html", {'room': room})


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message,
                                         user=username,
                                         room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
