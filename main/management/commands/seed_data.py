from django.core.management.base import BaseCommand
from main.models import Hostel, Warden, Student, Discussion, Resource


class Command(BaseCommand):
    help = "Seed database with initial hostels, wardens, demo student, and discussions"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Kyklos database...")

        # 1. Hostels
        hostel1, _ = Hostel.objects.get_or_create(
            id=1,
            defaults={"name": "Bagbazzar fancy hostel", "location": "Bagbazzar, Kathmandu"}
        )
        hostel2, _ = Hostel.objects.get_or_create(
            id=2,
            defaults={"name": "Maitighar hostel", "location": "Maitighar, Kathmandu"}
        )
        hostel3, _ = Hostel.objects.get_or_create(
            id=3,
            defaults={"name": "Boys Dream Hostel", "location": "Baneshwor, Kathmandu"}
        )
        self.stdout.write(self.style.SUCCESS("[OK] Hostels created"))

        # 2. Wardens
        warden_data = [
            ("warden_bagbazzar", "warden123", hostel1, "warden1@kyklos.edu"),
            ("warden_maitighar", "warden123", hostel2, "warden2@kyklos.edu"),
            ("warden_boysdream", "warden123", hostel3, "warden3@kyklos.edu"),
        ]
        for username, password, hostel, email in warden_data:
            warden, created = Warden.objects.get_or_create(
                username=username,
                defaults={"hostel": hostel, "gmail": email}
            )
            if created or warden.password != password:
                warden.set_password(password)
                warden.save()
        self.stdout.write(self.style.SUCCESS("[OK] Wardens created"))

        # 3. Demo Student
        demo_student, created = Student.objects.get_or_create(
            username="demo_student",
            defaults={
                "email": "student@kyklos.edu",
                "interest": "Computer Science",
                "location": "Kathmandu",
                "credit_score": 350,
                "hostel": hostel1
            }
        )
        if created:
            demo_student.set_password("student123")
            demo_student.save()
        self.stdout.write(self.style.SUCCESS("[OK] Demo student created (demo_student / student123)"))

        # 4. Sample Discussions
        discussions = [
            ("Computer Science", "Algorithms and Data Structures", "Tips on mastering graph algorithms and dynamic programming.", "Computer Science"),
            ("Physics", "Quantum Mechanics Foundations", "How does wave-particle duality impact quantum computing architectures?", "Physics"),
            ("Mathematics", "Calculus & Linear Algebra", "Intuitive ways to understand eigenvectors and eigenvalues.", "Mathematics"),
        ]
        for topic, title, content, category in discussions:
            Discussion.objects.get_or_create(
                title=title,
                defaults={
                    "topic": topic,
                    "content": content,
                    "category": category,
                    "username": "demo_student"
                }
            )
        self.stdout.write(self.style.SUCCESS("[OK] Sample discussions seeded"))

        self.stdout.write(self.style.SUCCESS("Kyklos database successfully initialized and ready to run!"))
