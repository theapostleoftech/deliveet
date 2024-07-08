from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from shipments.models import Delivery


@csrf_exempt
@login_required(login_url="accounts:signin")
def delivery_tasks_api(request):
    delivery_tasks = list(Delivery.objects.filter(status=Delivery.StatusChoices.PROCESSING).values())

    return JsonResponse({
        "success": True,
        "delivery_tasks": delivery_tasks
    })


@csrf_exempt
@login_required(login_url="accounts:signin")
def delivery_task_status_api(request, id):
    delivery_task = Delivery.objects.filter(
        id=id,
        courier=request.user.courier_account,
        status__in=[
            Delivery.StatusChoices.PICKUP_IN_PROGRESS,
            Delivery.StatusChoices.DELIVERY_IN_PROGRESS
        ]
    ).last()

    if Delivery.status == Delivery.StatusChoices.PICKUP_IN_PROGRESS:
        delivery_task.pickup_photo = request.FILES['pickup_photo']
        delivery_task.pickedup_at = timezone.now()
        delivery_task.status = Delivery.StatusChoices.DELIVERY_IN_PROGRESS
        delivery_task.save()

        print(delivery_task.pickup_photo.url)

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)("delivery_task_" + str(delivery_task.id), {
                'type': 'delivery_task_status_update',
                'delivery_task': {
                    'status': delivery_task.get_status_display(),
                    'pickup_photo': delivery_task.pickup_photo.url,
                }
            })
        except:
            pass

    elif delivery_task.status == Delivery.StatusChoices.DELIVERY_IN_PROGRESS:
        delivery_task.delivery_photo = request.FILES['delivery_photo']
        delivery_task.delivered_at = timezone.now()
        delivery_task.status = Delivery.StatusChoices.COMPLETED
        delivery_task.save()

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)("delivery_task_" + str(delivery_task.id), {
                'type': 'delivery_task_status_update',
                'job': {
                    'status': delivery_task.get_status_display(),
                    'delivery_photo': delivery_task.delivery_photo.url,
                }
            })
        except:
            pass

    return JsonResponse({
        "success": True
    })


@csrf_exempt
@login_required(login_url="accounts:signin")
def fcm_token_update_api(request):
    request.user.courier_account.fcm_token = request.GET.get('fcm_token')
    request.user.courier_account.save()

    return JsonResponse({
        "success": True
    })
