from django.test import TestCase
from django.urls import reverse
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


class PortfolioViewTests(TestCase):

    def setUp(self):
        self.url = reverse('portfolio')

    def test_view_uses_portfolio_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'portfolio.html')

    def test_view_returns_200_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_with_empty_database(self):
        response = self.client.get(self.url)
        self.assertIsNone(response.context['about'])
        self.assertIsNone(response.context['contact'])
        self.assertIsNone(response.context['system_info'])
        self.assertEqual(list(response.context['education']), [])
        self.assertEqual(list(response.context['work']), [])
        self.assertEqual(list(response.context['project']), [])
        self.assertEqual(list(response.context['testimonials']), [])

    def test_context_contains_all_keys(self):
        response = self.client.get(self.url)
        for key in ['about', 'education', 'work', 'project',
                    'contact', 'system_info', 'testimonials']:
            self.assertIn(key, response.context)

    def test_about_context_returns_first_instance(self):
        About.objects.create(content_message="About me")
        response = self.client.get(self.url)
        self.assertEqual(response.context['about'].content_message, "About me")

    def test_contact_context_returns_first_instance(self):
        Contact.objects.create(
            contact="1234567890",
            email="me@example.com",
            facebook_link="https://facebook.com/me",
            X_link="https://x.com/me",
            linked_in="https://linkedin.com/in/me",
            address="123 Main St",
        )
        response = self.client.get(self.url)
        self.assertEqual(response.context['contact'].email, "me@example.com")

    def test_system_info_context_returns_first_instance(self):
        SystemInfo.objects.create(
            system_name="My Portfolio",
            system_short_name="MP",
            welcome_message="Welcome!",
            system_logo=fake_image('logo.jpg'),
        )
        response = self.client.get(self.url)
        self.assertEqual(response.context['system_info'].system_name, "My Portfolio")

    def test_education_context_returns_all_instances(self):
        Education.objects.create(
            school_name="MIT",
            qualification="BSc",
            year_month=date(2020, 6, 1),
            description="CS",
        )
        Education.objects.create(
            school_name="Harvard",
            qualification="MSc",
            year_month=date(2022, 9, 1),
            description="Advanced",
        )
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['education']), 2)

    def test_work_context_returns_all_instances(self):
        Work.objects.create(
            company_name="Acme",
            position="Dev",
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
            description="Work",
        )
        Work.objects.create(
            company_name="Beta",
            position="Lead",
            start_date=date(2021, 1, 1),
            end_date=date(2022, 1, 1),
            description="More work",
        )
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['work']), 2)

    def test_project_context_returns_all_instances(self):
        Project.objects.create(
            project_name="P1",
            client="C1",
            summery="S1",
            description="D1",
            project_banner_image=fake_image('b1.jpg'),
        )
        Project.objects.create(
            project_name="P2",
            client="C2",
            summery="S2",
            description="D2",
            project_banner_image=fake_image('b2.jpg'),
        )
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['project']), 2)

    def test_testimonials_context_returns_all_instances(self):
        Testimonials.objects.create(client_name="Jane", testimony="Great")
        Testimonials.objects.create(client_name="John", testimony="Nice")
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['testimonials']), 2)

    def test_view_with_full_data(self):
        About.objects.create(content_message="About me")
        Education.objects.create(
            school_name="MIT", qualification="BSc",
            year_month=date(2020, 6, 1), description="CS",
        )
        Work.objects.create(
            company_name="Acme", position="Dev",
            start_date=date(2020, 1, 1), end_date=date(2021, 1, 1),
            description="Work",
        )
        Project.objects.create(
            project_name="P1", client="C1", summery="S1",
            description="D1", project_banner_image=fake_image('b.jpg'),
        )
        Contact.objects.create(
            contact="1234567890", email="me@example.com",
            facebook_link="https://facebook.com/me",
            X_link="https://x.com/me",
            linked_in="https://linkedin.com/in/me",
            address="123 Main St",
        )
        SystemInfo.objects.create(
            system_name="My Portfolio", system_short_name="MP",
            welcome_message="Welcome!", system_logo=fake_image('logo.jpg'),
        )
        Testimonials.objects.create(client_name="Jane", testimony="Great")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['about'].content_message, "About me")
        self.assertEqual(len(response.context['education']), 1)
        self.assertEqual(len(response.context['work']), 1)
        self.assertEqual(len(response.context['project']), 1)
        self.assertEqual(response.context['contact'].email, "me@example.com")
        self.assertEqual(response.context['system_info'].system_name, "My Portfolio")
        self.assertEqual(len(response.context['testimonials']), 1)