from django.test import TestCase, Client
from django.urls import reverse
from main.models import Student, Hostel, Discussion, Resource, Warden, Complaint


class KyklosAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.hostel = Hostel.objects.create(name="Central Hostel", location="Kathmandu")
        self.student = Student.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="secretpassword",
            interest="Physics",
            credit_score=200
        )
        self.warden = Warden.objects.create(
            username="warden1",
            hostel=self.hostel,
            gmail="warden@example.com"
        )
        self.warden.set_password("wardenpass")
        self.warden.save()

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "set.html")

    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_submit_success(self):
        response = self.client.post('/login_submit/', {
            'username': 'testuser',
            'password': 'secretpassword'
        })
        self.assertRedirects(response, f'/home{self.student.id}/')
        self.assertEqual(self.client.session.get('student_id'), self.student.id)

    def test_login_submit_invalid_password(self):
        response = self.client.post('/login_submit/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertRedirects(response, '/login/')

    def test_registration_success(self):
        response = self.client.post('/register_submit/', {
            'username': 'newstudent',
            'email': 'new@example.com',
            'password': 'newpassword123',
            'interest': 'Mathematics',
            'location': 'Pokhara'
        })
        self.assertRedirects(response, '/login/')
        self.assertTrue(Student.objects.filter(username='newstudent').exists())

    def test_registration_duplicate_username(self):
        response = self.client.post('/register_submit/', {
            'username': 'testuser',
            'email': 'different@example.com',
            'password': 'pwd',
        })
        self.assertRedirects(response, '/register/')

    def test_home_view(self):
        Discussion.objects.create(
            topic="Physics",
            title="Quantum Mechanics",
            content="Discussion about wave particle duality",
            category="Physics",
            username=self.student.username
        )
        response = self.client.get(f'/home{self.student.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quantum Mechanics")

    def test_post_discussion(self):
        response = self.client.post(f'/postdiscussion{self.student.id}/', {
            'topic': 'Computer Science',
            'title': 'Python Tips',
            'content': 'Write clean and efficient code',
            'category': 'Computer Science'
        })
        self.assertRedirects(response, f'/discussion{self.student.id}/')
        self.assertTrue(Discussion.objects.filter(title='Python Tips').exists())

    def test_redeem_credit_success(self):
        self.assertEqual(self.student.credit_score, 200)
        response = self.client.post(f'/redeemsubmit{self.student.id}/')
        self.assertRedirects(response, f'/reedem{self.student.id}/')
        self.student.refresh_from_db()
        self.assertEqual(self.student.credit_score, 50)

    def test_redeem_credit_insufficient(self):
        self.student.credit_score = 50
        self.student.save()
        response = self.client.post(f'/redeemsubmit{self.student.id}/')
        self.student.refresh_from_db()
        self.assertEqual(self.student.credit_score, 50)

    def test_correct_option_clicked(self):
        initial_score = self.student.credit_score
        response = self.client.get(f'/correctoptionclicked{self.student.id}/')
        self.assertRedirects(response, f'/home{self.student.id}/')
        self.student.refresh_from_db()
        self.assertEqual(self.student.credit_score, initial_score + 20)

    def test_submit_complaint(self):
        response = self.client.post(f'/complaintsubmit{self.hostel.id}/', {
            'roomno': '101',
            'studentname': 'Alice',
            'priority': 'High',
            'type': 'Plumbing',
            'description': 'Water leak in bathroom'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('complaint_id', data)
        self.assertTrue(Complaint.objects.filter(roomno='101').exists())

    def test_login_submit_empty_fields(self):
        """Login with missing credentials should redirect back with error."""
        response = self.client.post('/login_submit/', {
            'username': '',
            'password': ''
        })
        self.assertRedirects(response, '/login/')

    def test_login_submit_nonexistent_user(self):
        """Login with a username that doesn't exist should redirect back."""
        response = self.client.post('/login_submit/', {
            'username': 'ghost_user',
            'password': 'somepassword'
        })
        self.assertRedirects(response, '/login/')

    def test_registration_duplicate_email(self):
        """Registration with an already-used email should be rejected."""
        response = self.client.post('/register_submit/', {
            'username': 'uniqueuser',
            'email': 'test@example.com',  # already used by self.student
            'password': 'password123',
        })
        self.assertRedirects(response, '/register/')
        self.assertFalse(Student.objects.filter(username='uniqueuser').exists())

    def test_submit_complaint_get_not_allowed(self):
        """GET request to complaint submit should return 405 Method Not Allowed."""
        response = self.client.get(f'/complaintsubmit{self.hostel.id}/')
        self.assertEqual(response.status_code, 405)

    def test_post_discussion_empty_fields(self):
        """Posting a discussion with empty title/content should redirect back."""
        response = self.client.post(f'/postdiscussion{self.student.id}/', {
            'topic': 'Physics',
            'title': '',
            'content': '',
            'category': 'Physics'
        })
        self.assertRedirects(response, f'/creatediscussion{self.student.id}/')
        self.assertEqual(Discussion.objects.count(), 0)

    def test_view_nonexistent_hostel_returns_404(self):
        """Requesting a hostel that doesn't exist should return 404."""
        response = self.client.get('/hostel9999/')
        self.assertEqual(response.status_code, 404)

