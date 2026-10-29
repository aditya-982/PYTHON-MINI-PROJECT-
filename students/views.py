import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db.models import Avg, Count
from django.shortcuts import render
from .models import Student

def search_student(request):
    query = request.GET.get('student_id', '')
    student = None
    error_message = None

    if query:
        try:
            student = Student.objects.filter(student_id__icontains=query).first() \
                      or Student.objects.filter(first_name__icontains=query).first()
            if not student:
                error_message = "No student found with that ID or Name."
        except Exception as e:
            error_message = str(e)

    context = {
        'query': query,
        'student': student,
        'error_message': error_message,
    }
    return render(request, 'students/search.html', context)


def student_analytics(request):
    students = Student.objects.all()
    total_count = students.count()
    avg_gpa = students.aggregate(Avg('gpa'))['gpa__avg'] or 0

    plt.style.use('dark_background')

    def get_uri(fig):
        buffer = BytesIO()
        fig.savefig(buffer, format='png', transparent=True, bbox_inches='tight')
        buffer.seek(0)
        uri = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close(fig)
        return uri

    # --- Graph 1: Course Distribution (Bar Chart) ---
    courses = Student.objects.values('course').annotate(count=Count('id')).order_by('-count')
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar([c['course'] for c in courses], [c['count'] for c in courses], color=['#0d6efd', '#008080', '#20c997', '#ffc107'])
    ax.set_title('Students per Course', color='white', fontsize=10)
    plt.xticks(rotation=30, ha='right', fontsize=8)
    plt.tight_layout()
    chart1_uri = get_uri(fig)

    # --- Graph 2: GPA Histogram ---
    gpas = [s.gpa for s in students if s.gpa is not None]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    if gpas:
        ax.hist(gpas, bins=5, color='#20c997', edgecolor='#0f172a', alpha=0.85)
    ax.set_title('GPA Distribution', color='white', fontsize=10)
    ax.set_xlabel('GPA', fontsize=8, color='#94a3b8')
    plt.tight_layout()
    chart2_uri = get_uri(fig)

    # --- Graph 3: Enrollment Year Breakdown (Bar Chart) ---
    years = Student.objects.values('enrollment_year').annotate(count=Count('id')).order_by('enrollment_year')
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar([str(y['enrollment_year']) for y in years], [y['count'] for y in years], color='#ffc107')
    ax.set_title('Enrollment Year Count', color='white', fontsize=10)
    plt.tight_layout()
    chart3_uri = get_uri(fig)

    # --- Graph 4: Average GPA per Course ---
    avg_course_gpa = Student.objects.values('course').annotate(avg_gpa=Avg('gpa')).order_by('-avg_gpa')
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.barh([c['course'] for c in avg_course_gpa], [c['avg_gpa'] for c in avg_course_gpa], color='#0dcaf0')
    ax.set_title('Avg GPA by Course', color='white', fontsize=10)
    ax.set_xlim(0, 10)
    plt.tight_layout()
    chart4_uri = get_uri(fig)

    # --- Graph 5: GPA Performance Tiers ---
    tier_9_10 = Student.objects.filter(gpa__gte=9.0).count()
    tier_8_9 = Student.objects.filter(gpa__gte=8.0, gpa__lt=9.0).count()
    tier_7_8 = Student.objects.filter(gpa__gte=7.0, gpa__lt=8.0).count()
    tier_below_7 = Student.objects.filter(gpa__lt=7.0).count()
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(['9.0-10', '8.0-8.9', '7.0-7.9', '<7.0'], [tier_9_10, tier_8_9, tier_7_8, tier_below_7], color=['#198754', '#0d6efd', '#ffc107', '#dc3545'])
    ax.set_title('GPA Performance Tiers', color='white', fontsize=10)
    plt.tight_layout()
    chart5_uri = get_uri(fig)

    # --- Graph 6: Scatter Plot (ID Hash / Index vs GPA) ---
    fig, ax = plt.subplots(figsize=(5, 3.5))
    if students:
        y_vals = [s.gpa for s in students]
        x_vals = range(len(y_vals))
        ax.scatter(x_vals, y_vals, color='#d63384', alpha=0.8, edgecolors='none')
    ax.set_title('Individual Student GPA Spread', color='white', fontsize=10)
    ax.set_xlabel('Student Index', fontsize=8, color='#94a3b8')
    plt.tight_layout()
    chart6_uri = get_uri(fig)

    context = {
        'total_count': total_count,
        'avg_gpa': avg_gpa,
        'chart1_uri': chart1_uri,
        'chart2_uri': chart2_uri,
        'chart3_uri': chart3_uri,
        'chart4_uri': chart4_uri,
        'chart5_uri': chart5_uri,
        'chart6_uri': chart6_uri,
    }
    return render(request, 'students/analytics.html', context)