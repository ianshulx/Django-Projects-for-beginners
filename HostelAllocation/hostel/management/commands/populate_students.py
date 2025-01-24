from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hostel.models import Student

class Command(BaseCommand):
    help = "Delete existing student records and populate new students with real names and CET marks"

    def handle(self, *args, **kwargs):
        Student.objects.all().delete()

        User.objects.exclude(username='rector').delete()  

        students_data = [
            {"name": "Aarav", "student_id": "S1", "category": "open", "cet_marks": 85},
            {"name": "Vihaan", "student_id": "S2", "category": "open", "cet_marks": 78},
            {"name": "Arjun", "student_id": "S3", "category": "open", "cet_marks": 92},
            {"name": "Sai", "student_id": "S4", "category": "open", "cet_marks": 65},
            {"name": "Ishaan", "student_id": "S5", "category": "open", "cet_marks": 88},
            {"name": "Aditi", "student_id": "S6", "category": "open", "cet_marks": 90},
            {"name": "Kavya", "student_id": "S7", "category": "open", "cet_marks": 79},
            {"name": "Arnav", "student_id": "S8", "category": "open", "cet_marks": 81},
            {"name": "Riya", "student_id": "S9", "category": "open", "cet_marks": 74},
            {"name": "Vansh", "student_id": "S10", "category": "open", "cet_marks": 77},
            {"name": "Krishna", "student_id": "S11", "category": "open", "cet_marks": 82},
            {"name": "Niharika", "student_id": "S12", "category": "open", "cet_marks": 84},
            {"name": "Yash", "student_id": "S13", "category": "open", "cet_marks": 69},
            {"name": "Ananya", "student_id": "S14", "category": "open", "cet_marks": 80},
            {"name": "Aditya", "student_id": "S15", "category": "open", "cet_marks": 76},
            {"name": "Priya", "student_id": "S16", "category": "reserved", "cet_marks": 86},
            {"name": "Rahul", "student_id": "S17", "category": "reserved", "cet_marks": 75},
            {"name": "Sneha", "student_id": "S18", "category": "reserved", "cet_marks": 89},
            {"name": "Neha", "student_id": "S19", "category": "reserved", "cet_marks": 64},
            {"name": "Rohan", "student_id": "S20", "category": "reserved", "cet_marks": 72},
            {"name": "Maya", "student_id": "S21", "category": "reserved", "cet_marks": 71},
            {"name": "Isha", "student_id": "S22", "category": "reserved", "cet_marks": 82},
            {"name": "Shivam", "student_id": "S23", "category": "reserved", "cet_marks": 65},
            {"name": "Aarvi", "student_id": "S24", "category": "reserved", "cet_marks": 78},
            {"name": "Karan", "student_id": "S25", "category": "reserved", "cet_marks": 74},
            {"name": "Deepa", "student_id": "S26", "category": "reserved", "cet_marks": 70},
            {"name": "Vikram", "student_id": "S27", "category": "reserved", "cet_marks": 69},
            {"name": "Meera", "student_id": "S28", "category": "reserved", "cet_marks": 72},
            {"name": "Ravi", "student_id": "S29", "category": "reserved", "cet_marks": 68},
            {"name": "Pooja", "student_id": "S30", "category": "reserved", "cet_marks": 73},
        ]

        for data in students_data:
            user = User.objects.create(username=data["name"].lower())
            user.set_password("student@vjti")  
            user.save()

            Student.objects.create(
                user=user,
                student_id=data["student_id"],
                name=data["name"],
                category=data["category"],
                cet_marks=data["cet_marks"],
            )

        rector_user, created = User.objects.get_or_create(username="rector")
        if created:
            rector_user.set_password("rectorpass")
            rector_user.save()

        self.stdout.write(self.style.SUCCESS("Successfully deleted existing records and populated new students with CET marks, and created a rector account."))
