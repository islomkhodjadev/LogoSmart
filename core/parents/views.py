from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .models import Parent
from .serializers import (
    UserSerializer,
    ParentSerializer,
    ChildSerializer,
    CitySerializer,
    ChildLevelSerializer,
)
from .utils.otp import OTP
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from .models import Child, City, ChildLevels
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import (
    IsOwnerOrReadOnlyPostFree,
    IsAuthenticatedOrPostOnly,
    IsOwnerChildPermission,
    IsOwnerParent,
)
from rest_framework.exceptions import NotFound, PermissionDenied
from django.contrib.auth import get_user_model
import random
import string
from rest_framework.parsers import JSONParser

from .serializers import PhoneNumberSerializer
from django.core.cache import cache


class RegisterByPhone(APIView):

    def get_object(self, phoneNumber):
        """
        This method is created to verify and get the user object
        :param phoneNumber:
        :return: the object of use
        """
        try:
            user = get_user_model().objects.get(username=phoneNumber)
            self.check_object_permissions(
                self.request, user
            )  # Check object-level permissions
            return user
        except get_user_model().DoesNotExist:
            raise NotFound("User not found or you do not have permission to access it.")

    def post(self, request, phoneNumber=None):
        """
        This method is implemented to perform creation of the user
        via phone Number

        :param request:
        * if user is being created the first time then in the request post method the "first" data
        should be passed, and phoneNumber. it will create a user with username - phoneNumber and random password
        * To activate the user it will send OTP verification.  And by requesting again with phoneNumber and Code
        you will be able to activate user.
        * To continue registration and to provide username and password it should be sent by post request
        username, password, phoneNumber the previous one.

        :param phoneNumber:
        * everytime it should be valid uzbek number with +999 .. ... .. ..

        :return:

        """
        code = request.data.pop("code", False)
        data = request.data
        if phoneNumber is not None and code:

            user = self.get_object(phoneNumber=phoneNumber)
            result = OTP.verify(user, code)
            if result is None:
                return Response(
                    {"result": "code is inpired"}, status=status.HTTP_205_RESET_CONTENT
                )
            elif result:
                return Response(
                    {"result": f"user {user.username} activated"},
                    status=status.HTTP_201_CREATED,
                )

            return Response({"result": "wrong code"}, status=status.HTTP_204_NO_CONTENT)

        elif "first" in data and "phoneNumber" in data:

            data["password"] = "".join(
                random.choices(string.ascii_letters + string.digits, k=12)
            )
            data["username"] = data["phoneNumber"]
            user = UserSerializer(data=data)
            if get_user_model().objects.filter(username=data["phoneNumber"]).exists():
                user = get_user_model().objects.get(username=data["phoneNumber"])
                otp = OTP(
                    username=user.username, phone_number=user.phoneNumber.raw_input
                )
                otp.send_code()
                return Response(
                    UserSerializer(instance=user).data, status=status.HTTP_200_OK
                )
            elif user.is_valid(raise_exception=True):

                user = user.save()
                otp = OTP(
                    username=user.username, phone_number=user.phoneNumber.raw_input
                )
                otp.send_code()
                return Response(
                    UserSerializer(instance=user).data, status=status.HTTP_200_OK
                )

        elif "phoneNumber" in data and "username" in data and "password" in data:
            user = self.get_object(data["phoneNumber"])

            user = UserSerializer(instance=user, data=data)
            if user.is_valid(raise_exception=True):

                user = user.save()
                return Response(
                    UserSerializer(instance=user).data, status=status.HTTP_200_OK
                )
        return Response({"result": "wrong credentials"})

    def get(self, request, phoneNumber=None):
        """
        * This method only used to resend OTP verification.
        :param request:

        :param phoneNumber:
        :return:
        """

        if get_user_model().objects.filter(username=phoneNumber).exists():

            user = get_user_model().objects.get(username=phoneNumber)
            result = OTP(username=phoneNumber, phone_number=user.phoneNumber.raw_input)
            result.send_code()

            return Response({"result": "code sent"})

        return Response({"result": "wrong username"})


class GetToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """
        * This method is used to create and send the Token to the user

        :param request:
         - In request data The login and Password should be sent
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        if Token.objects.filter(user=user).exists():
            Token.objects.filter(user=user).delete()

        token = Token.objects.create(user=user)

        return Response(
            {"user_id": user.pk, "token": str(token), "username": user.username}
        )


class ChangePhoneNumber(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        """
        * This method used to change user's phoneNumber,
        To do so user should send post request with phoneNumber and in headers there should be Token.
        The OTP verification will be sent
        * To perform change of phoneNumber user should send post Request with code.

        :param request:
        :return:
        """
        user = request.user
        phoneNumber = request.data.get("phoneNumber", False)
        code = request.data.get("code", False)

        if phoneNumber:
            serializer = PhoneNumberSerializer(request.data)
            if serializer.is_valid(raise_exception=True):
                otp = OTP(
                    request.user.username, serializer.validated_data["phoneNumber"]
                )

                otp.send_code()
                cache.set(
                    request.user.phoneNumber.raw_input,
                    serializer.validated_data["phoneNumber"],
                )
                return Response(data={"result": "code sent"})
        elif code:

            result = OTP.verify(request.user, code)
            phoneNumber = cache.get(request.user.phoneNumber.raw_input)

            if result is None:
                return Response(
                    {"result": "code is inpired"}, status=status.HTTP_204_NO_CONTENT
                )
            elif result:
                from phonenumber_field.phonenumber import PhoneNumber

                phoneNumber = PhoneNumber.from_string(phoneNumber)
                user = request.user
                user.phoneNumber = phoneNumber
                user.save()
                return Response(
                    UserSerializer(instance=user).data, status=status.HTTP_201_CREATED
                )

            return Response({"result": "wrong code"}, status=status.HTTP_204_NO_CONTENT)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
          * This method is to change the user credentials username and password
        :param request:
        :return:
        """
        user = request.user

        serializer = UserSerializer(instance=user, partial=True, data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                UserSerializer(instance=user).data, status=status.HTTP_200_OK
            )

        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ParentView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request):
        parent = getattr(request.user, "parent", None)
        if parent is None:
            return Response({"detail": "Parent not found"}, status=404)
        return Response(ParentSerializer(parent).data)

    def post(self, request):
        """
        * This will create the parent

        :param request:
        * In request there should be sent
        name, city, region, age
        :return:
        """

        data = request.data

        user = request.user

        data["user"] = user.id

        serializer = ParentSerializer(data=data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        * This method is used to change all credentials of parent at once

        :param request:
        :return:
        """
        parent = request.user.parent

        serializer = ParentSerializer(
            parent, data=request.data, context={"partial": False}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        * This method is to perform partial change in parent

        :param request:
        :return:
        """
        parent = request.user.parent

        serializer = ParentSerializer(parent, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildAPIView(APIView):

    permission_classes = [IsAuthenticated, IsOwnerChildPermission]

    def get_object(self, pk):
        try:
            child = Child.objects.get(pk=pk)
            self.check_object_permissions(self.request, child)
            return child
        except Child.DoesNotExist:
            raise NotFound(
                "Child not found or you do not have permission to access it."
            )

    def get(self, request):
        return Response(
            ChildSerializer(
                Child.objects.filter(parent__user=request.user), many=True
            ).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """
        * This method is to create Child

        :param request:
          - In request data  'gender' = M or F, 'name', 'age', 'image' should be sent
        :return:
        """

        data = request.data
        data["parent"] = request.user.parent.pk

        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        * This method is to perform partial update in child
        :param request:
        :param pk:
        :return:
        """

        child = self.get_object(pk)
        if child is None:
            return Response(
                {"error": "Child not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChildSerializer(child, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        * This method is to perform full update
        :param request:
        :param pk:
        :return:
        """
        child = self.get_object(pk)
        if child is None:
            return Response(
                {"error": "Child not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChildSerializer(child, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityListView(APIView):

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChildLevel(APIView):
    permission_classes = [IsAuthenticated, IsOwnerChildPermission]
    parser_classes = [JSONParser]

    def get_objects(self, pk=None, multiple=False):
        """
        * This method is used to get the object of childLevel
        if multiple is True it returns all levels of the child
        if not then it returns The give pk childLevel instance

        :param pk:
        :param multiple:
        :return:
        """
        if multiple:
            return ChildLevels.objects.filter(child__parent__user=self.request.user)
        try:
            child = ChildLevels.objects.get(pk=pk)
            self.check_object_permissions(self.request, child)
            return child
        except ChildLevels.DoesNotExist:
            raise NotFound(
                "ChildLevel not found or you do not have permission to access it."
            )

    def get(self, request):
        """
        This method is to return the child all levels
        :param request:
        :return:
        """

        childlevels = self.get_objects(multiple=True)
        data = ChildLevelSerializer(childlevels, many=True)

        return Response(data=data.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
            * This method is to create the new levels which child is participated.
        :param request:
        :return:
        """

        data = request.data
        many = data.get("many", False)
        levels = data.get("levels", False)

        if many and levels and isinstance(levels, list):
            serializer = ChildLevelSerializer(data=levels, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            pk = data.get("child", None)
            if not pk:
                return Response(
                    {"detail": "Child with this id not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check permissions and existence
            self.get_objects(pk)

            serializer = ChildLevelSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        * This method is used to update the ChildLevel

        :param request:
        :return:
        """
        data = request.data
        if "id" in data:
            level = self.get_objects(pk=data["id"])

            serializer = ChildLevelSerializer(instance=level, data=data, partial=True)

            if serializer.is_valid(raise_exception=True):
                level = serializer.save()
                return Response(data=level.data, status=status.HTTP_200_OK)

        return Response(
            {"result": "you should provide id of the level"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class Test(APIView):

    def post(self, request):
        return Response(data={"code": f"{request.user}"})
