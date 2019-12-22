import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pink_blue_app.models import Inventory
from pink_blue_app.serializers.user import LoginStatusSerializer, InventorySerializer

logger = logging.getLogger(__name__)


def get_user_info(user):
    data = LoginStatusSerializer(user).data
    return data


def get_inventory_info(inventory_info):
    data = InventorySerializer(inventory_info).data
    return data


def create_inventory(batch_date, batch_number, inventory_status, mrp, product_name, quantity, vendor):
    return Inventory.objects.create(
        product_name=product_name,
        vendor=vendor,
        mrp=mrp,
        batch_number=batch_number,
        batch_date=batch_date,
        quantity=quantity,
        status=inventory_status
    )


def update_inventory_info(update_inventory, batch_date, batch_number, inventory_status, mrp, product_name, quantity,
                          vendor):
    update_inventory.product_name = product_name
    update_inventory.vendor = vendor
    update_inventory.mrp = mrp
    update_inventory.batch_number = batch_number
    update_inventory.batch_date = batch_date
    update_inventory.quantity = quantity
    update_inventory.status = inventory_status
    return update_inventory


class Login(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        inventory_data = []
        try:
            user = authenticate(username=username, password=password, email=email)
            if user is not None:
                login(request, user)
                user_pro = get_user_info(user)
                if user_pro['groups'][0] == 'store_manager':
                    get_inventory_records = Inventory.objects.filter(status=0)
                    for item in get_inventory_records:
                        inventory_data.append(get_inventory_info(item))
                else:
                    get_inventory_records = Inventory.objects.filter(status=1)
                    for item in get_inventory_records:
                        inventory_data.append(get_inventory_info(item))
                return Response({'Success': user_pro, 'inventory': inventory_data}, status=status.HTTP_200_OK)
            else:
                logger.debug("Invalid password !")
                return Response({"Message": "Invalid password !"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception('Error while login - {}'.format(e))
            return Response({'Message': 'Error while login - {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


class InventoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(email=request.query_params.get('email'))
            user_pro = get_user_info(user)
            if user_pro['groups'][0] == 'store_manager':
                get_inventory_records = Inventory.objects.filter(status=0)
            else:
                get_inventory_records = Inventory.objects.filter(status=1)

            if get_inventory_records is not None:
                inventory_info = get_inventory_info(get_inventory_records)
                return Response({'Success': inventory_info}, status=status.HTTP_200_OK)
            else:
                logger.debug('Records not found!')
                return Response({"Message": "Records not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception('Error while fetching data - {}'.format(e))
            return Response({'Message': 'Error while fetching data - {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        product_name = request.data.get('product_name')
        vendor = request.data.get('vendor')
        mrp = request.data.get('mrp')
        batch_number = request.data.get('batch_number')
        batch_date = request.data.get('batch_date')
        quantity = request.data.get('quantity')
        inventory_status = 'PENDING'
        try:
            user = User.objects.get(email=request.user.email)
            user_pro = get_user_info(user)
            if user['groups'][0] == 'store_manager' or user_pro['groups'][0] == 'inventory_access_permission':
                inventory_status = 'APPROVED'
                inventory = create_inventory(batch_date, batch_number, inventory_status, mrp, product_name, quantity, vendor)
                inventory.save()
                return Response({'Success': 'Records added/updated successfully!'}, status=status.HTTP_200_OK)
            else:
                inventory = create_inventory(batch_date, batch_number, inventory_status, mrp, product_name, quantity, vendor)
                inventory.save()
                return Response({'Success': 'Sent for approval!'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Error while adding data - {}'.format(e))
            return Response({'Message': 'Error while adding data - {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        product_id = request.data.get('product_id') if request.data.get('product_id') in request.data else ''
        product_name = request.data.get('product_name') if request.data.get('product_name') in request.data else ''
        vendor = request.data.get('vendor') if request.data.get('vendor') in request.data else ''
        mrp = request.data.get('mrp') if request.data.get('mrp') in request.data else ''
        batch_number = request.data.get('batch_number') if request.data.get('batch_number') in request.data else ''
        batch_date = request.data.get('batch_date') if request.data.get('batch_date') in request.data else ''
        quantity = request.data.get('quantity') if request.data.get('quantity') in request.data else ''
        inventory_status = 'PENDING'
        try:
            update_inventory = Inventory.objects.get(id=product_id)
            user = User.objects.get(email=request.user.emil)
            user_pro = get_user_info(user)
            if user['groups'][0] == 'store_manager' or user_pro['groups'][0] == 'inventory_access_permission':
                inventory_status = 'APPROVED'
                inventory = update_inventory_info(update_inventory, batch_date, batch_number, inventory_status,
                                                  mrp, product_name, quantity, vendor)
                inventory.save()
                return Response({'Success': 'Records added/updated successfully!'}, status=status.HTTP_200_OK)
            else:
                inventory = update_inventory_info(update_inventory, batch_date, batch_number, inventory_status, mrp,
                                                  product_name, quantity, vendor)
                inventory.save()
                return Response({'Success': 'Sent for approval!'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Error while updating data - {}'.format(e))
            return Response({'Message': 'Error while updating data - {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


class InventoryAccessApproval(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')
        try:
            user = User.objects.get(email=email)
            user_pro = get_user_info(user)
            if user is not None and user_pro['groups'][0] != 'store_manager' and user_pro['groups'][0] != 'inventory_access_permission':
                group = Group.objects.get(name='inventory_access_permission')
                user.groups.add(group)
                user.save()
                return Response({'Success': 'Approved successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'Success': 'User records not found!'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception('Error while approving access permission - {}'.format(e))
            return Response({'Message': 'Error while approving access permission - {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
