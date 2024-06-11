from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from .tasks import test_task
from django.http import HttpResponse
from .models import Job
from .serializers import JobSerializer
from rest_framework.response import Response
@api_view(["GET"])
def test_view(request) :
    job = Job.objects.create()
    coins = request.data.get('coins', [])
    price = test_task.delay(job.job_id, coins)
    return JsonResponse({"job_id" : str(job.job_id)})

@api_view(["GET"])
def scraping_status(request, job_id) :
    try :
        job = Job.objects.get(job_id = job_id)
    except Job.DoesNotExist :
        return JsonResponse({"error" : "no record found with this job id"})
    if job.status == "IN_PROGRESS" :
        return JsonResponse({"status" : job.status})

    serializer = JobSerializer(job)
    return Response(serializer.data)
