from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100)
    enrollment_year = models.IntegerField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"