from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
