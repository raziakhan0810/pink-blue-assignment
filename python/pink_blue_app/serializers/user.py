from django.contrib.auth.models import User, Permission
from rest_framework import serializers

from pink_blue_app.models import Inventory


class LoginStatusSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'password', 'name', 'first_name', 'last_name', 'email', 'groups',
                  'is_active', 'last_login', 'date_joined', 'permissions')

    def get_name(self, user):
        return "{} {}".format(user.first_name, user.last_name)

    def get_permissions(self, user):
        permissions = user.user_permissions.all() | Permission.objects.filter(group__user=user)
        if user.is_superuser:
            permissions = Permission.objects.all()
        return [x.codename for x in permissions]

    def get_groups(self, user):
        return [group.name for group in user.groups.all()]


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ('id', 'product_name', 'vendor', 'mrp', 'batch_number', 'batch_date', 'quantity', 'status')
