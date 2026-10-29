import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from students.models import Student

# Optional: Clear old entries to avoid any duplicate email conflicts
Student.objects.all().delete()

sample_students = [
    ('3', 'Aarav', 'Sharma', 'MCA', 8.5, 2024, 'aarav.sharma@example.com'),
    ('4', 'Vivaan', 'Gupta', 'BTech CSE', 7.9, 2023, 'vivaan.gupta@example.com'),
    ('5', 'Aditya', 'Verma', 'MCA', 9.2, 2024, 'aditya.verma@example.com'),
    ('6', 'Diya', 'Singh', 'BCA', 8.1, 2025, 'diya.singh@example.com'),
    ('7', 'Ananya', 'Mehra', 'MCA', 8.8, 2024, 'ananya.mehra@example.com'),
    ('8', 'Kabir', 'Malhotra', 'BTech CSE', 7.4, 2023, 'kabir.malhotra@example.com'),
    ('9', 'Rohan', 'Joshi', 'BCA', 6.9, 2025, 'rohan.joshi@example.com'),
    ('10', 'Priya', 'Nair', 'MCA', 9.1, 2024, 'priya.nair@example.com'),
    ('11', 'Neha', 'Reddy', 'BTech CSE', 8.3, 2023, 'neha.reddy@example.com'),
    ('12', 'Rahul', 'Patel', 'BCA', 7.7, 2025, 'rahul.patel@example.com'),
    ('13', 'Sneha', 'Iyer', 'MCA', 9.5, 2024, 'sneha.iyer@example.com'),
    ('14', 'Karan', 'Kulkarni', 'BTech CSE', 6.5, 2023, 'karan.kulkarni@example.com'),
    ('15', 'Simran', 'Kaur', 'BCA', 8.4, 2025, 'simran.kaur@example.com'),
    ('16', 'Arjun', 'Das', 'MCA', 7.8, 2024, 'arjun.das@example.com'),
    ('17', 'Tanvi', 'Pillai', 'BTech CSE', 8.9, 2023, 'tanvi.pillai@example.com'),
    ('18', 'Manish', 'Kumar', 'BCA', 7.2, 2025, 'manish.kumar@example.com'),
    ('19', 'Pooja', 'Chopra', 'MCA', 9.3, 2024, 'pooja.chopra@example.com'),
    ('20', 'Vikram', 'Rao', 'BTech CSE', 7.6, 2023, 'vikram.rao@example.com'),
    ('21', 'Meera', 'Menon', 'BCA', 8.0, 2025, 'meera.menon@example.com'),
    ('22', 'Amit', 'Tiwari', 'MCA', 8.7, 2024, 'amit.tiwari@example.com'),
]

for sid, fname, lname, course, gpa, year, email in sample_students:
    Student.objects.update_or_create(
        email=email,  # Lookup by unique email instead of old IDs
        defaults={
            'student_id': sid,
            'first_name': fname,
            'last_name': lname,
            'course': course,
            'gpa': gpa,
            'enrollment_year': year,
        }
    )

print("Successfully populated 20 student records with IDs starting from 3!")