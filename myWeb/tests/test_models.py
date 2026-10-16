from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

from myWeb.models import (
    About, Education, Work, Project,
    Contact, SystemInfo, Testimonials,
)


def fake_image(name='test.jpg'):
    return SimpleUploadedFile(
        name,
        b'\x47\x49\x46\x38\x39\x61',
        content_type='image/gif',
    )


class AboutModelTests(TestCase):

    def test_str_returns_content(self):
        about = About.objects.create(content_message="Hello world")
        self.assertEqual(str(about), "Content")

    def test_can_create_first_instance(self):
        About.objects.create(content_message="First")
        self.assertEqual(About.objects.count(), 1)

    def test_second_instance_raises_validation_error(self):
        About.objects.create(content_message="First")
        with self.assertRaises(ValidationError):
            About.objects.create(content_message="Second")

    def test_second_instance_via_full_clean_raises(self):
        About.objects.create(content_message="First")
        second = About(content_message="Second")
        with self.assertRaises(ValidationError):
            second.full_clean()

    def test_update_existing_instance_is_allowed(self):
        about = About.objects.create(content_message="First")
        about.content_message = "Updated"
        about.save()
        about.refresh_from_db()
        self.assertEqual(about.content_message, "Updated")

    def test_profile_picture_is_optional(self):
        about = About.objects.create(content_message="No image")
        self.assertFalse(about.profile_picture)


class EducationModelTests(TestCase):

    def test_str_returns_school_name(self):
        edu = Education.objects.create(
            school_name="MIT",
            qualification="BSc Computer Science",
            year_month=date(2020, 6, 1),
            description="Studied CS",
        )
        self.assertEqual(str(edu), "MIT")

    def test_fields_saved_correctly(self):
        edu = Education.objects.create(
            school_name="Harvard",
            qualification="MSc",
            year_month=date(2022, 9, 1),
            description="Advanced studies",
        )
        edu.refresh_from_db()
        self.assertEqual(edu.qualification, "MSc")
        self.assertEqual(edu.year_month, date(2022, 9, 1))


class WorkModelTests(TestCase):

    def test_str_returns_company_name(self):
        work = Work.objects.create(
            company_name="Acme Corp",
            position="Engineer",
            start_date=date(2021, 1, 1),
            end_date=date(2023, 1, 1),
            description="Built things",
        )
        self.assertEqual(str(work), "Acme Corp")

    def test_dates_saved_correctly(self):
        work = Work.objects.create(
            company_name="Acme",
            position="Dev",
            start_date=date(2020, 5, 1),
            end_date=date(2021, 5, 1),
            description="Work",
        )
        work.refresh_from_db()
        self.assertEqual(work.start_date, date(2020, 5, 1))
        self.assertEqual(work.end_date, date(2021, 5, 1))


class ProjectModelTests(TestCase):

    def test_str_returns_project_name(self):
        project = Project.objects.create(
            project_name="Portfolio",
            client="Self",
            summery="A portfolio site",
            description="Built with Django",
            project_banner_image=fake_image('banner.jpg'),
        )
        self.assertEqual(str(project), "Portfolio")

    def test_project_url_optional(self):
        project = Project.objects.create(
            project_name="No URL",
            client="Client",
            summery="Summary",
            description="Desc",
            project_banner_image=fake_image('banner.jpg'),
        )
        self.assertIsNone(project.project_url)

    def test_project_url_saved_when_provided(self):
        project = Project.objects.create(
            project_name="With URL",
            client="Client",
            summery="Summary",
            project_url="https://example.com",
            description="Desc",
            project_banner_image=fake_image('banner.jpg'),
        )
        project.refresh_from_db()
        self.assertEqual(project.project_url, "https://example.com")


class ContactModelTests(TestCase):

    def _create_contact(self, **overrides):
        data = {
            "contact": "1234567890",
            "email": "me@example.com",
            "facebook_link": "https://facebook.com/me",
            "X_link": "https://x.com/me",
            "linked_in": "https://linkedin.com/in/me",
            "address": "123 Main St",
        }
        data.update(overrides)
        return Contact.objects.create(**data)

    def test_str_returns_email(self):
        contact = self._create_contact()
        self.assertEqual(str(contact), "me@example.com")

    def test_second_instance_raises_validation_error(self):
        self._create_contact()
        with self.assertRaises(ValidationError):
            self._create_contact(email="other@example.com")

    def test_update_existing_instance_allowed(self):
        contact = self._create_contact()
        contact.address = "New Address"
        contact.save()
        contact.refresh_from_db()
        self.assertEqual(contact.address, "New Address")


class SystemInfoModelTests(TestCase):

    def _create_system_info(self, **overrides):
        data = {
            "system_name": "My Portfolio",
            "system_short_name": "MP",
            "welcome_message": "Welcome!",
            "system_logo": fake_image('logo.jpg'),
        }
        data.update(overrides)
        return SystemInfo.objects.create(**data)

    def test_str_returns_system_name(self):
        info = self._create_system_info()
        self.assertEqual(str(info), "My Portfolio")

    def test_second_instance_raises_validation_error(self):
        self._create_system_info()
        with self.assertRaises(ValidationError):
            self._create_system_info(system_name="Other")

    def test_background_image_optional(self):
        info = self._create_system_info()
        self.assertFalse(info.background_image)

    def test_update_existing_instance_allowed(self):
        info = self._create_system_info()
        info.welcome_message = "Updated"
        info.save()
        info.refresh_from_db()
        self.assertEqual(info.welcome_message, "Updated")


class TestimonialsModelTests(TestCase):

    def test_str_returns_client_name(self):
        t = Testimonials.objects.create(
            client_name="Jane Doe",
            testimony="Great work!",
        )
        self.assertEqual(str(t), "Jane Doe")

    def test_background_image_optional(self):
        t = Testimonials.objects.create(
            client_name="John",
            testimony="Nice",
        )
        self.assertFalse(t.background_image)

    def test_multiple_testimonials_allowed(self):
        Testimonials.objects.create(client_name="A", testimony="X")
        Testimonials.objects.create(client_name="B", testimony="Y")
        self.assertEqual(Testimonials.objects.count(), 2)