from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from rest_framework.serializers import ModelSerializer

from django.contrib.auth import authenticate, get_user_model


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserRegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request=request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid email or password'})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserLogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)
