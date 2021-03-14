from rest_framework import status
from rest_framework.response import Response


def save_serializer(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_serializer(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def round_to_10_sig(func):
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        return round(val, 10)

    return wrapper
