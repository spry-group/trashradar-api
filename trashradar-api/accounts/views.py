import datetime
import uuid

from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from accounts import models, serializers
from accounts.permissions import IsAdminOrAccountOwner
from rest_framework.views import APIView
from utils.tasks.common import send_mail


class AccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Accounts
    """
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
    requires_authentication = ['list', 'retrieve', 'change_password']

    def get_permissions(self):
        """
        Returns a boolean value if the User has permissions on the ViewSet
        :return: (boolean) If the user has permissions
        """
        if self.action in self.requires_authentication:
            return (IsAdminOrAccountOwner(),)

        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (IsAdminOrAccountOwner(),)

    def create(self, request, *args, **kwargs):
        """
        Create an account.
        ---
        parameters_strategy:
            form: replace

        parameters:
            - name: username
              description: Account username
              required: true
              type: string
            - name: full_name
              description: Account full name
              required: true
              type: string
            - name: email
              description: Account email
              required: true
              type: email
            - name: phone
              description: Account phone
              required: true
              type: string

        serializer: serializers.AccountSerializer
        """
        response = super(AccountViewSet, self).create(request, *args, **kwargs)
        if response.status_code == 201:
            account = models.Account.objects.get(username=request.data.get('username'))
            email_response = self._send_token_email(request, account, 'verify')
            if email_response.status_code != 204:
                return email_response

        return response

    def list(self, request, *args, **kwargs):
        """
        Retrieve authenticated user if user is not superuser, if is
        superuser retrieves all users

        ---

        response_serializer: serializers.AccountSerializer
        responseMessages:
            - code: 403
              message: Forbidden

        """
        user = request.user
        if user.is_superuser:
            return super(AccountViewSet, self).list(request, *args, **kwargs)

        serialized_user = self.serializer_class(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve authenticated user

        ---

        response_serializer: serializers.AccountSerializer
        responseMessages:
            - code: 403
              message: Forbidden

        """
        retrieved_user = self.get_object()
        user = request.user
        if user.is_superuser or retrieved_user == user:
            return super(AccountViewSet, self).retrieve(request, *args, **kwargs)

        return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to perform this action.'
            }, status=status.HTTP_403_FORBIDDEN)

    @list_route(methods=['post'])
    def reset_password(self, request, *args, **kwargs):
        """
        Reset user password.

        ---
        parameters_strategy:
            form: replace
        parameters:
            - name: username
              description: Account username
              required: true
              type: string

        response_serializer: serializers.AccountSerializer
        responseMessages:
            - code: 400
              message: Bad request

        """
        username = request.data.get('username')
        if not username:
            return Response({'errors': {'username': ['This field is required.']}}, status.HTTP_400_BAD_REQUEST)

        try:
            account = models.Account.objects.get(username=username)
        except models.Account.DoesNotExist:
            return Response({
                'status': 'Not Found',
                'message': 'User does not exist.'
            }, status.HTTP_404_NOT_FOUND)

        email_response = self._send_token_email(request, account, 'reset')

        return email_response

    @list_route(methods=['post'])
    def change_reset_password(self, request, *args, **kwargs):
        """
        Change the password of the user.

        ---
        parameters_strategy:
            form: replace
        parameters:
            - name: username
              description: Account username
              required: true
              type: string
            - name: password
              description: Account password
              required: true
              type: string
            - name: token
              description: Token associated to the account
              required: true
              type: string

        response_serializer: serializers.AccountSerializer
        responseMessages:
            - code: 400
              message: Bad request

        """
        username = request.data.get('username')
        password = request.data.get('password')
        token = request.data.get('token')

        if not username:
            return Response({'errors': {'username': ['This field is required.']}}, status.HTTP_400_BAD_REQUEST)

        if not token:
            return Response({'errors': {'token': ['This field is required.']}}, status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'errors': {'password': ['This field is required.']}}, status.HTTP_400_BAD_REQUEST)

        try:
            account = models.Account.objects.get(username=username)
        except models.Account.DoesNotExist:
            return Response({
                'status': 'Not Found',
                'message': 'User does not exist.'
            }, status.HTTP_404_NOT_FOUND)

        if not token or account.activation_key != token:
            return Response({
                'status': 'Bad request',
                'message': 'Token does not match with the user.'
            }, status.HTTP_404_NOT_FOUND)

        account.set_password(password)
        account.activation_key = ''
        account.key_expires = None
        account.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['post'])
    def verify(self, request, *args, **kwargs):
        """
        Verify the user.

        ---
        parameters_strategy:
            form: replace
        parameters:
            - name: username
              description: Account username
              required: true
              type: string
            - name: token
              description: Token associated to the account
              required: true
              type: string

        response_serializer: serializers.AccountSerializer
        responseMessages:
            - code: 400
              message: Bad request

        """
        username = request.data.get('username')
        token = request.data.get('token')

        if not username:
            return Response({'errors': {'username': ['This field is required.']}}, status.HTTP_400_BAD_REQUEST)

        if not token:
            return Response({'errors': {'token': ['This field is required.']}}, status.HTTP_400_BAD_REQUEST)

        try:
            account = models.Account.objects.get(username=username)
        except models.Account.DoesNotExist:
            return Response({
                'status': 'Not Found',
                'message': 'User does not exist.'
            }, status.HTTP_404_NOT_FOUND)

        if not token or account.activation_key != token:
            return Response({
                'status': 'Bad request',
                'message': 'Token does not match with the user.'
            }, status.HTTP_404_NOT_FOUND)

        account.is_verified = True
        account.activation_key = ''
        account.key_expires = None
        account.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['put'], permission_classes=[IsAdminOrAccountOwner])
    def change_password(self, request, *args, **kwargs):
        """
        Change the password of the user

        ---

        parameters_strategy:
            form: replace
        parameters:
            - name: old_password
              description: Old user username
              required: true
              type: string
            - name: new_password
              description: New user password
              required: true
              type: string

        response_serializer: serializers.AccountSerializer
        responseMessages:
            - code: 400
              message: Bad request

        """
        account = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not account.check_password(old_password):
            return Response({
                'status': 'Bad request',
                'message': 'Current password does not match.'
            }, status=status.HTTP_400_BAD_REQUEST)

        account.set_password(new_password)
        account.save(update_fields=['password', 'updated_at'])

        return Response({}, status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _send_token_email(request, account, token_type):
        if account.key_expires and account.key_expires > timezone.now():
            return Response({
                'status': 'Bad request',
                'message': 'We already sent a link.'
            }, status.HTTP_400_BAD_REQUEST)

        account.activation_key = uuid.uuid4().hex
        account.key_expires = timezone.now() + datetime.timedelta(days=4)
        account.save()

        url = '{}/login/{}/{}/{}'.format(
            request.META.get('HTTP_ORIGIN', 'https://trashradar.com/'),
            token_type, account.username, account.activation_key
        )
        data = {
            'url': url,
            'username': account.username
        }
        send_mail.delay([account.email], token_type, data)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    """
    Login View
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Authenticate the user

        ---

        parameters:
            - name: username
              description: Account username
              required: true
              type: string
            - name: password
              description: Account password
              required: true
              type: string

        response_serializer: serializers.AccountSerializer
        responseMessages:
            - code: 401
              message: Unauthorized

        """
        data = request.data

        username = str(data.get('username')).lower()
        password = data.get('password')

        account = authenticate(username=username, password=password)

        if account:
            if account.is_active:
                if account.is_verified:
                    login(request, account)
                    serialized_account = serializers.AccountSerializer(account)
                    data = serialized_account.data

                    return Response(data)
                else:
                    return Response({
                        'status': 'Unauthorized',
                        'message': 'You need to verify you account first.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'Your account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Logout View
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Remove authentication to the user

        ---
        response_serializer: serializers.AccountSerializer
        responseMessages:
            - code: 403
              message: Forbidden

        """
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
