from django.urls import path
from . import views


urlpatterns = [
    path("", views.RegisterUserView.as_view(), name="register"),
    path("login", views.CreateLoginView.as_view(), name="login"),
    path("logout", views.LogoutUserView.as_view(), name="logout"),
    path("home/", views.home, name="home"),
    path("api/messages/single/<int:pk>/", views.MessageListView.as_view()),
    path("api/messages/list/", views.MessageView.as_view({"get": "list"})),
    path("api/messages/create/", views.MessageCreate.as_view()),
    path("<str:room>/", views.room, name="room"),
    path("home/checkview", views.checkview, name="checkview"),
    path("send", views.send, name="send"),
    path("getMessages/<str:room>/", views.getMessages, name="getMessages"),
]
