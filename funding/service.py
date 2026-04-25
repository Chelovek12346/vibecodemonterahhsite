from .models import *

class FundingService:
    @staticmethod
    def get_summary(student):
        sources = FundingSource.objects.filter(student=student, status="confirmed")
        donations = Donation.objects.filter(student=student)

        covered = sum(s.amount for s in sources) + sum(d.amount for d in donations)
        gap = student.total_cost - covered
        progress = covered / student.total_cost if student.total_cost else 0

        return {
            "covered": covered,
            "gap": gap,
            "progress": progress
        }