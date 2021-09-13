from rest_framework import serializers
from .models import Message


class MessageListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("value", "date", "user", "room")


class MessageViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("value", "date", "user", "room")


class MessageCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("value", "user", "room")
