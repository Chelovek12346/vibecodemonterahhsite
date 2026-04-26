from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

from .models import StudentProfile, Donation
from .service import FundingService


@api_view(['GET'])
def funding_summary(request):
    student = request.user.studentprofile
    data = FundingService.get_summary(student)
    return Response(data)


@api_view(['POST'])
def donate(request):
    student_id = request.data.get("student_id")
    amount = float(request.data.get("amount"))

    student = StudentProfile.objects.get(id=student_id)

    Donation.objects.create(
        student=student,
        amount=amount
    )

    return Response({"status": "ok"})


def funding_summary(request):
    return render(request, 'funding/fundraising.html')

def donate(request):
    return render(request, 'funding/donation.html')