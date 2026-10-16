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


class PortfolioTemplateTests(TestCase):

    def setUp(self):
        self.url = reverse('portfolio')

    def _render(self):
        return self.client.get(self.url)

    def test_template_used(self):
        response = self._render()
        self.assertTemplateUsed(response, 'portfolio.html')

    def test_static_css_is_loaded(self):
        response = self._render()
        self.assertContains(response, 'css/portfolio.css')

    def test_static_js_is_loaded(self):
        response = self._render()
        self.assertContains(response, 'js/portfolio.js')

    def test_bootstrap_cdn_present(self):
        response = self._render()
        self.assertContains(response, 'bootstrap@5.3.3')

    def test_page_title_uses_system_name(self):
        SystemInfo.objects.create(
            system_name="My Portfolio",
            system_short_name="MP",
            welcome_message="Welcome!",
            system_logo=fake_image('logo.jpg'),
        )
        response = self._render()
        self.assertContains(response, '<title>My Portfolio</title>', html=False)

    def test_system_name_rendered_in_navbar_and_footer(self):
        SystemInfo.objects.create(
            system_name="ReneTech",
            system_short_name="RT",
            welcome_message="Hello",
            system_logo=fake_image('logo.jpg'),
        )
        response = self._render()
        self.assertContains(response, 'ReneTech')

    def test_welcome_message_rendered(self):
        SystemInfo.objects.create(
            system_name="X",
            system_short_name="X",
            welcome_message="Welcome to my site",
            system_logo=fake_image('logo.jpg'),
        )
        response = self._render()
        self.assertContains(response, 'Welcome to my site')

    def test_about_content_rendered(self):
        About.objects.create(content_message="This is about me.")
        response = self._render()
        self.assertContains(response, 'This is about me.')

    def test_about_profile_picture_rendered_when_present(self):
        About.objects.create(
            content_message="Hi",
            profile_picture=fake_image('pic.jpg'),
        )
        response = self._render()
        self.assertContains(response, 'profile_pics/')

    def test_about_profile_picture_absent_when_missing(self):
        About.objects.create(content_message="Hi")
        response = self._render()
        self.assertNotContains(response, 'profile_pics/')

    def test_contact_details_rendered(self):
        Contact.objects.create(
            contact="1234567890",
            email="me@example.com",
            facebook_link="https://facebook.com/me",
            X_link="https://x.com/me",
            linked_in="https://linkedin.com/in/me",
            address="123 Main St",
        )
        response = self._render()
        self.assertContains(response, "1234567890")
        self.assertContains(response, "me@example.com")
        self.assertContains(response, "123 Main St")
        self.assertContains(response, "https://facebook.com/me")
        self.assertContains(response, "https://x.com/me")
        self.assertContains(response, "https://linkedin.com/in/me")

    def test_hire_me_mailto_link(self):
        Contact.objects.create(
            contact="1",
            email="hire@example.com",
            facebook_link="https://f.com",
            X_link="https://x.com",
            linked_in="https://l.com",
            address="A",
        )
        response = self._render()
        self.assertContains(response, 'mailto:hire@example.com')

    def test_education_first_entry_rendered(self):
        Education.objects.create(
            school_name="MIT",
            qualification="BSc Computer Science",
            year_month=date(2020, 6, 1),
            description="Studied CS deeply.",
        )
        response = self._render()
        self.assertContains(response, "MIT")
        self.assertContains(response, "BSc Computer Science")
        self.assertContains(response, "Studied CS deeply.")

    def test_work_first_entry_rendered(self):
        Work.objects.create(
            company_name="Acme Corp",
            position="Engineer",
            start_date=date(2021, 1, 1),
            end_date=date(2023, 1, 1),
            description="Built APIs.",
        )
        response = self._render()
        self.assertContains(response, "Acme Corp")
        self.assertContains(response, "Engineer")
        self.assertContains(response, "Built APIs.")

    def test_project_rendered(self):
        Project.objects.create(
            project_name="Portfolio Site",
            client="Self",
            summery="A site",
            description="Built with Django",
            project_banner_image=fake_image('b.jpg'),
        )
        response = self._render()
        self.assertContains(response, "Portfolio Site")
        self.assertContains(response, "Built with Django")


    def test_project_url_button_rendered_when_provided(self):
        Project.objects.create(
            project_name="P",
            client="C",
            summery="S",
            project_url="https://example.com",
            description="D",
            project_banner_image=fake_image('b.jpg'),
        )
        response = self._render()
        self.assertContains(response, "https://example.com")
        self.assertContains(response, "Visit The Project")

    def test_project_url_button_absent_when_missing(self):
        Project.objects.create(
            project_name="P",
            client="C",
            summery="S",
            description="D",
            project_banner_image=fake_image('b.jpg'),
        )
        response = self._render()
        self.assertNotContains(response, "Visit The Project")

    def test_empty_projects_shows_empty_state(self):
        response = self._render()
        self.assertContains(response, "No projects to display yet.")

    def test_testimonial_rendered(self):
        Testimonials.objects.create(
            client_name="Jane Doe",
            testimony="Amazing work!",
        )
        response = self._render()
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "Amazing work!")

    def test_testimonial_background_image_rendered(self):
        Testimonials.objects.create(
            client_name="Jane",
            testimony="Great",
            background_image=fake_image('bg.jpg'),
        )
        response = self._render()
        self.assertContains(response, 'background_images/')

    def test_all_section_ids_present(self):
        response = self._render()
        for section_id in [
            'scrollspyHome', 'scrollspyAbout', 'scrollspyResume',
            'scrollspyProjects', 'scrollspyTestimonials',
        ]:
            self.assertContains(response, f'id="{section_id}"', html=False)

    def test_footer_copyright_present(self):
        response = self._render()
        self.assertContains(response, "Copyright 2026")
        self.assertContains(response, "All rights reserved")