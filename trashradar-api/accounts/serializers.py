from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Account Serializer
    """
    token = serializers.SerializerMethodField('get_user_token')

    class Meta:
        model = Account
        fields = (
            'id', 'username', 'email', 'full_name', 'phone',
            'created_at', 'updated_at', 'token'
        )
        read_only_fields = ('token', 'created_at', 'updated_at')

    @staticmethod
    def get_user_token(user):
        token, created = Token.objects.get_or_create(user=user)
        return str(token)

    def create(self, validated_data):
        password = self.context['request'].data.get('password')
        if not password:
            raise serializers.ValidationError({'password': ['This field is required.']})

        return Account.objects.create_user(
            password=password,
            **validated_data
        )
