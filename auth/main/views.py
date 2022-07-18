import json

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from main.producer import publish
from main.serializers import RegisterSerializer, MyTokenObtainPairSerializer, ContactSerializer
from main.utils import perform_excel, group_contacts


class RegisterView(APIView):
    """API for registration"""
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyObtainTokenPairView(TokenObtainPairView):
    """API to retrieve Token for login credentials"""
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class AddContact(APIView):
    """API to add contact for user"""

    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            data['username'] = request.user.username
            request_contact = publish('contact_create', data)
            if request_contact is None:
                return Response({"message": "Some error occurred!"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": json.loads(request_contact.decode("utf-8"))}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetContactByUser(APIView):
    "API to get contacts of exact user"
    def get(self, request, id):
        if not id is None:
            data = {'id': id}
            request_contact = publish('contact_get_by_user', data)
            if request_contact is None:
                return Response({"message": "Some error occurred!"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(json.loads(request_contact.decode("utf-8")), status=status.HTTP_200_OK)
        return Response({"message": "id is not set in params!"}, status=status.HTTP_400_BAD_REQUEST)


class GetAllContacts(APIView):
    "API to retrieve all users with contacts"
    def get(self, request):
        data = {}
        request_contact = publish('contact_get_all', data)
        if request_contact is None:
            return Response({"message": "Some error occurred!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(json.loads(request_contact.decode("utf-8")), status=status.HTTP_200_OK)


class ExportExcelContacts(APIView):
    "API to export to xlsx all users with contacts"
    def get(self, request):
        data = {}
        columns = ['Username', 'Email', 'Name', 'Surname', 'Phone', 'Instagram', 'Telegram']
        request_contact = publish('contact_export_all', data)
        if request_contact is None:
            return Response({"message": "Some error occurred!"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = json.loads(request_contact.decode("utf-8"))
        result = group_contacts(queryset)
        return perform_excel(result, columns, 'contacts')