from datetime import date
from io import BytesIO

import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from student_management_app.models import Courses, CustomUser, SessionYearModel, Students


class BulkUploadTests(TestCase):
    def test_student_bulk_upload_creates_user_and_profile(self):
        Courses.objects.create(course_name='Computer Science')
        SessionYearModel.objects.create(
            session_start_year=date(2025, 1, 1),
            session_end_year=date(2026, 12, 31),
        )
        admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Test@1234',
            user_type='1',
            first_name='Admin',
            last_name='User',
        )
        self.client.force_login(admin)

        df = pd.DataFrame([
            {
                'first_name': 'Alice',
                'last_name': 'Ngugi',
                'username': 'STD999',
                'email': 'alice@example.com',
                'password': 'Password@123',
                'gender': 'Female',
                'address': 'Nairobi',
                'course': 'Computer Science',
                'session': '2025-2026',
            }
        ])
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Students')
        output.seek(0)
        uploaded = SimpleUploadedFile(
            'students.xlsx',
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

        response = self.client.post(reverse('bulk_upload_students_save'), {'file': uploaded}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['imported_count'], 1)
        self.assertTrue(CustomUser.objects.filter(username='STD999').exists())
        self.assertTrue(Students.objects.filter(admin__username='STD999').exists())
