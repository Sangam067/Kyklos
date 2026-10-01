import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Student, Hostel, Discussion, Resource, Warden, Complaint

logger = logging.getLogger(__name__)


def index(request):
    """Landing / home portal page."""
    return render(request, "set.html")


def login(request):
    """Student login page."""
    return render(request, "login.html")


def login_submit(request):
    """Handle student authentication with secure password verification."""
    if request.method != "POST":
        return redirect("/login/")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")

    if not username or not password:
        messages.error(request, "Username and password are required.")
        return redirect("/login/")

    try:
        student = Student.objects.get(username=username)
    except Student.DoesNotExist:
        messages.error(request, "Your account does not exist.")
        return redirect("/login/")

    # Support both modern hashed passwords and legacy plain-text
    is_valid = student.check_password(password) or (student.password == password)

    if is_valid:
        # Upgrade plain-text password to secure hash automatically
        if student.password == password:
            student.set_password(password)
            student.save(update_fields=['password'])

        request.session['student_id'] = student.id
        request.session['student_username'] = student.username
        return redirect(f"/home{student.id}/")
    else:
        messages.error(request, "Password incorrect.")
        return redirect("/login/")


def register(request):
    """Student registration page."""
    return render(request, "register.html")


def register_submit(request):
    """Handle new student registration."""
    if request.method != "POST":
        return redirect("/register/")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    email = request.POST.get("email", "").strip()
    interest = request.POST.get("interest", "").strip()
    location = request.POST.get("location", "").strip()

    if not username or not password or not email:
        messages.error(request, "Username, email, and password are required.")
        return redirect("/register/")

    if Student.objects.filter(username=username).exists():
        messages.error(request, "Username is already taken.")
        return redirect("/register/")

    if Student.objects.filter(email=email).exists():
        messages.error(request, "Email is already registered.")
        return redirect("/register/")

    student = Student(
        username=username,
        email=email,
        interest=interest,
        location=location,
        credit_score=0
    )
    student.set_password(password)
    student.save()

    messages.success(request, "Registration successful! Please log in.")
    return redirect("/login/")


def student_homepage(request, hostelid):
    """Hostel student portal homepage."""
    hostel = get_object_or_404(Hostel, id=hostelid)
    return render(request, "student.html", {"hostelid": hostelid, "hostel": hostel})


def home(request, studentid):
    """Student personal dashboard showing matching discussions and resources."""
    student = get_object_or_404(Student, id=studentid)

    # Efficient filtering based on student interest, with fallback
    if student.interest:
        discussions = Discussion.objects.filter(category__iexact=student.interest)
        if not discussions.exists():
            discussions = Discussion.objects.all()

        resources = Resource.objects.filter(category__iexact=student.interest)
        if not resources.exists():
            resources = Resource.objects.all()
    else:
        discussions = Discussion.objects.all()
        resources = Resource.objects.all()

    context = {
        'id': student.id,
        "username": student.username,
        "interest": student.interest,
        "discussions": discussions,
        "student_object": student,
        "resources": resources
    }
    return render(request, "home.html", context=context)


def view_hostel(request, hostelid):
    """Display hostel info and login form."""
    hostel = get_object_or_404(Hostel, id=hostelid)
    context = {
        "hostelname": hostel.name,
        "hostelid": hostel.id
    }
    return render(request, "hostel.html", context=context)


def hostelloginsubmit(request, hostelid):
    """Authenticate warden or student for a specific hostel."""
    if request.method != "POST":
        return redirect(f"/hostel{hostelid}/")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    usertype = request.POST.get("usertype", "").strip().lower()

    if usertype == "warden":
        try:
            warden = Warden.objects.get(username=username)
        except Warden.DoesNotExist:
            messages.error(request, "Warden account does not exist.")
            return redirect(f"/hostel{hostelid}/")

        is_valid = warden.check_password(password) or (warden.password == password)
        if is_valid and warden.hostel_id == hostelid:
            if warden.password == password:
                warden.set_password(password)
                warden.save(update_fields=['password'])
            request.session['warden_id'] = warden.id
            return redirect(f"/maintainance{hostelid}/")
        else:
            messages.error(request, "Password incorrect or not authorized for this hostel.")
            return redirect(f"/hostel{hostelid}/")

    elif usertype == "student":
        try:
            student = Student.objects.get(username=username)
        except Student.DoesNotExist:
            messages.error(request, "Student account does not exist.")
            return redirect(f"/hostel{hostelid}/")

        is_valid = student.check_password(password) or (student.password == password)
        if is_valid:
            if student.password == password:
                student.set_password(password)
                student.save(update_fields=['password'])
            request.session['student_id'] = student.id
            return redirect(f"/student{hostelid}/")
        else:
            messages.error(request, "Password incorrect.")
            return redirect(f"/hostel{hostelid}/")

    messages.error(request, "Please choose a valid user type.")
    return redirect(f"/hostel{hostelid}/")


def view_studyspace(request, studentid):
    """View study space and resources for a student."""
    student = get_object_or_404(Student, id=studentid)
    if student.interest:
        resources = Resource.objects.filter(category__iexact=student.interest)
        if not resources.exists():
            resources = Resource.objects.all()
    else:
        resources = Resource.objects.all()

    context = {
        'id': student.id,
        "username": student.username,
        "interest": student.interest,
        "resources": resources
    }
    return render(request, "studyspace.html", context=context)


def addresource(request, userid):
    """Upload a study resource and award credit points."""
    if request.method == "POST":
        student = get_object_or_404(Student, id=userid)
        title = request.POST.get("title", "").strip()
        category = request.POST.get("category", "").strip()
        url = request.POST.get("url", "").strip()
        image = request.FILES.get("thumbnail")

        if not title or not category or not url or not image:
            messages.error(request, "All resource fields including thumbnail are required.")
            return redirect(f'/studyspace{userid}/')

        Resource.objects.create(
            title=title,
            category=category,
            resourceurl=url,
            thumbnail=image,
            username=student.username
        )

        # Single query update for credit score
        student.credit_score = (student.credit_score or 0) + 150
        student.save(update_fields=['credit_score'])

    return redirect(f'/studyspace{userid}/')


def discussion(request, userid):
    """List all community discussions."""
    context = {
        "userid": userid,
        "discussions": Discussion.objects.all()
    }
    return render(request, "discussion.html", context=context)


def create_discussion(request, userid):
    """Render new discussion form."""
    return render(request, "creatediscussion.html", {"userid": userid})


def post_discussion(request, userid):
    """Handle new discussion submission."""
    if request.method == "POST":
        student = get_object_or_404(Student, id=userid)
        topic = request.POST.get("topic", "").strip()
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        category = request.POST.get("category", "").strip() or topic

        if not title or not content:
            messages.error(request, "Title and content cannot be empty.")
            return redirect(f"/creatediscussion{userid}/")

        Discussion.objects.create(
            topic=topic,
            title=title,
            content=content,
            category=category,
            username=student.username
        )
    return redirect(f"/discussion{userid}/")


def maintainance(request, hostelid):
    """Warden maintenance portal."""
    hostel = get_object_or_404(Hostel, id=hostelid)
    return render(request, "maintainance.html", {"hostel": hostel})


def dashboard(request, hostelid):
    """Hostel overview dashboard."""
    hostel = get_object_or_404(Hostel, id=hostelid)
    return render(request, "dashboard.html", {"hostel": hostel})


def complaint(request, hostelid):
    """Hostel complaints list."""
    hostel = get_object_or_404(Hostel, id=hostelid)
    complaints = Complaint.objects.filter(hostelid=hostelid)
    return render(request, "complaint.html", {"hostel": hostel, "complaints": complaints})


def submit_complaint(request, hostelid):
    """Submit a student maintenance complaint and notify warden."""
    if request.method == 'POST':
        roomno = request.POST.get('roomno', '').strip()
        studentname = request.POST.get('studentname', '').strip()
        priority = request.POST.get('priority', '').strip()
        complaint_type = request.POST.get('type', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')

        if not all([roomno, studentname, priority, complaint_type, description]):
            return JsonResponse({'error': 'All fields are required!'}, status=400)

        complaint = Complaint.objects.create(
            roomno=roomno,
            studentname=studentname,
            priority=priority,
            complaint_type=complaint_type,
            description=description,
            image=image,
            hostelid=hostelid
        )

        # Notify warden by email if configured
        email_sent = False
        try:
            warden = Warden.objects.filter(hostel_id=hostelid).first()
            if warden and warden.gmail and getattr(settings, 'EMAIL_HOST_USER', None):
                subject = f"New Complaint from {studentname} (Room {roomno})"
                body = (
                    f"A new complaint has been submitted:\n\n"
                    f"Room No: {roomno}\n"
                    f"Name: {studentname}\n"
                    f"Priority: {priority}\n"
                    f"Type: {complaint_type}\n"
                    f"Description: {description}\n"
                )
                email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [warden.gmail])
                if image:
                    image.seek(0)
                    email.attach(image.name, image.read(), getattr(image, 'content_type', 'image/jpeg'))
                email.send(fail_silently=True)
                email_sent = True
        except Exception as e:
            logger.warning("Could not send complaint email: %s", e)

        return JsonResponse({
            'message': 'Complaint submitted successfully!' + (' Email sent to warden.' if email_sent else ''),
            'complaint_id': complaint.id,
            'email_sent': email_sent
        }, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def reedem(request, studentid):
    """Rewards redemption page."""
    student = get_object_or_404(Student, id=studentid)
    context = {
        "creditscore": student.credit_score,
        "id": studentid
    }
    return render(request, "redeem.html", context=context)


def redeem_submit(request, studentid):
    """Handle item redemption using credit points."""
    student = get_object_or_404(Student, id=studentid)
    if (student.credit_score or 0) >= 150:
        student.credit_score -= 150
        student.save(update_fields=['credit_score'])
        messages.success(request, "Item redeemed successfully!")
    else:
        messages.error(request, "Credit score not sufficient (150 required).")

    return redirect(f"/reedem{studentid}/")


def correctoptionclicked(request, studentid):
    """Reward user for answering quiz question correctly."""
    student = get_object_or_404(Student, id=studentid)
    student.credit_score = (student.credit_score or 0) + 20
    student.save(update_fields=['credit_score'])
    return redirect(f'/home{studentid}/')


# Subject quiz and study group views
def math(request):
    return render(request, "math.html")


def computer(request):
    return render(request, "computer.html")


def biology(request):
    return render(request, "biology.html")


def physics(request):
    return render(request, "physics.html")


def mathgroup(request):
    return render(request, "mathgroup.html")


def physicsgroup(request):
    return render(request, "physicsgroup.html")


def computergroup(request):
    return render(request, "computergroup.html")


def biologygroup(request):
    return render(request, "biologygroup.html")
