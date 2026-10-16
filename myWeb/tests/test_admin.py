from django.test import TestCase
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.test import Client

from myWeb.models import (
    About, Education, Work, Project,
    Contact, SystemInfo, Testimonials,
)
from myWeb.admin import (
    AboutAdmin, EducationAdmin, WorkAdmin, ProjectAdmin,
    ContactAdmin, SystemInfoAdmin, TestimonialsAdmin,
    SingletonAdmin,
)


class AdminRegistrationTests(TestCase):

    def test_all_models_registered(self):
        for model in [About, Education, Work, Project, Contact, SystemInfo, Testimonials]:
            self.assertIn(model, site._registry)

    def test_about_admin_class(self):
        self.assertIsInstance(site._registry[About], AboutAdmin)

    def test_education_admin_class(self):
        self.assertIsInstance(site._registry[Education], EducationAdmin)

    def test_work_admin_class(self):
        self.assertIsInstance(site._registry[Work], WorkAdmin)

    def test_project_admin_class(self):
        self.assertIsInstance(site._registry[Project], ProjectAdmin)

    def test_contact_admin_class(self):
        self.assertIsInstance(site._registry[Contact], ContactAdmin)

    def test_system_info_admin_class(self):
        self.assertIsInstance(site._registry[SystemInfo], SystemInfoAdmin)

    def test_testimonials_admin_class(self):
        self.assertIsInstance(site._registry[Testimonials], TestimonialsAdmin)


class AdminListDisplayTests(TestCase):

    def test_about_list_display(self):
        self.assertEqual(
            site._registry[About].list_display,
            ['content_message', 'profile_picture'],
        )

    def test_education_list_display(self):
        self.assertEqual(
            site._registry[Education].list_display,
            ('school_name', 'qualification', 'year_month', 'description'),
        )

    def test_work_list_display(self):
        self.assertEqual(
            site._registry[Work].list_display,
            ('company_name', 'position', 'start_date', 'end_date', 'description'),
        )

    def test_project_list_display(self):
        self.assertEqual(
            site._registry[Project].list_display,
            ('project_name', 'client', 'summery', 'description',
             'project_banner_image', 'project_url'),
        )

    def test_contact_list_display(self):
        self.assertEqual(
            site._registry[Contact].list_display,
            ('contact', 'email', 'facebook_link', 'X_link', 'linked_in', 'address'),
        )

    def test_system_info_list_display(self):
        self.assertEqual(
            site._registry[SystemInfo].list_display,
            ('system_name', 'system_short_name', 'owner_name', 'welcome_message',
             'system_logo', 'background_image'),
        )

    def test_testimonials_list_display(self):
        self.assertEqual(
            site._registry[Testimonials].list_display,
            ('client_name', 'testimony', 'background_image'),
        )


class AdminSearchFieldsTests(TestCase):

    def test_education_search_fields(self):
        self.assertEqual(
            site._registry[Education].search_fields,
            ('school_name', 'qualification'),
        )

    def test_work_search_fields(self):
        self.assertEqual(
            site._registry[Work].search_fields,
            ('company_name', 'position'),
        )

    def test_project_search_fields(self):
        self.assertEqual(
            site._registry[Project].search_fields,
            ('project_name', 'client'),
        )

    def test_contact_search_fields(self):
        self.assertEqual(
            site._registry[Contact].search_fields,
            ('contact', 'email'),
        )

    def test_system_info_search_fields(self):
        self.assertEqual(
            site._registry[SystemInfo].search_fields,
            ('system_name', 'system_short_name'),
        )

    def test_testimonials_search_fields(self):
        self.assertEqual(site._registry[Testimonials].search_fields, ['client_name'])


class AdminListFilterTests(TestCase):

    def test_education_list_filter(self):
        self.assertEqual(
            site._registry[Education].list_filter,
            ('school_name', 'qualification', 'year_month'),
        )

    def test_work_list_filter(self):
        self.assertEqual(
            site._registry[Work].list_filter,
            ('company_name', 'position', 'start_date', 'end_date'),
        )

    def test_project_list_filter(self):
        self.assertEqual(
            site._registry[Project].list_filter,
            ('project_name', 'client'),
        )

    def test_contact_list_filter(self):
        self.assertEqual(
            site._registry[Contact].list_filter,
            ('contact', 'email'),
        )

    def test_system_info_list_filter(self):
        self.assertEqual(
            site._registry[SystemInfo].list_filter,
            ('system_name', 'system_short_name'),
        )

    def test_testimonials_list_filter(self):
        self.assertEqual(
            site._registry[Testimonials].list_filter,
            ('client_name', 'testimony'),
        )


class SingletonAdminPermissionTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='a@a.com', password='pass',
        )
        self.request = self.client.request().wsgi_request
        self.request.user = self.admin

    def test_has_add_permission_true_when_empty(self):
        admin_instance = AboutAdmin(About, site)
        self.assertTrue(admin_instance.has_add_permission(self.request))

    def test_has_add_permission_false_when_exists(self):
        About.objects.create(content_message="Exists")
        admin_instance = AboutAdmin(About, site)
        self.assertFalse(admin_instance.has_add_permission(self.request))

    def test_has_delete_permission_always_true(self):
        admin_instance = AboutAdmin(About, site)
        self.assertTrue(admin_instance.has_delete_permission(self.request))

    def test_singleton_admin_contact_empty(self):
        admin_instance = ContactAdmin(Contact, site)
        self.assertTrue(admin_instance.has_add_permission(self.request))

    def test_singleton_admin_contact_exists(self):
        Contact.objects.create(
            contact="1234567890",
            email="me@example.com",
            facebook_link="https://facebook.com/me",
            X_link="https://x.com/me",
            linked_in="https://linkedin.com/in/me",
            address="123 Main St",
        )
        admin_instance = ContactAdmin(Contact, site)
        self.assertFalse(admin_instance.has_add_permission(self.request))

    def test_singleton_admin_system_info_empty(self):
        admin_instance = SystemInfoAdmin(SystemInfo, site)
        self.assertTrue(admin_instance.has_add_permission(self.request))

    def test_singleton_admin_system_info_exists(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        SystemInfo.objects.create(
            system_name="X", system_short_name="X",
            welcome_message="Hi",
            system_logo=SimpleUploadedFile(
                'l.gif', b'\x47\x49\x46\x38\x39\x61', content_type='image/gif',
            ),
        )
        admin_instance = SystemInfoAdmin(SystemInfo, site)
        self.assertFalse(admin_instance.has_add_permission(self.request))


class AdminSmokeTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='a@a.com', password='pass',
        )
        self.client = Client()
        self.client.force_login(self.admin)

    def test_admin_index_loads(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_about_changelist_loads(self):
        response = self.client.get('/admin/myWeb/about/')
        self.assertEqual(response.status_code, 200)

    def test_education_changelist_loads(self):
        response = self.client.get('/admin/myWeb/education/')
        self.assertEqual(response.status_code, 200)

    def test_work_changelist_loads(self):
        response = self.client.get('/admin/myWeb/work/')
        self.assertEqual(response.status_code, 200)

    def test_project_changelist_loads(self):
        response = self.client.get('/admin/myWeb/project/')
        self.assertEqual(response.status_code, 200)

    def test_contact_changelist_loads(self):
        response = self.client.get('/admin/myWeb/contact/')
        self.assertEqual(response.status_code, 200)

    def test_system_info_changelist_loads(self):
        response = self.client.get('/admin/myWeb/systeminfo/')
        self.assertEqual(response.status_code, 200)

    def test_testimonials_changelist_loads(self):
        response = self.client.get('/admin/myWeb/testimonials/')
        self.assertEqual(response.status_code, 200)