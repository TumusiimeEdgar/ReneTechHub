from django.test import TestCase
from django.urls import reverse, resolve
from django.urls.exceptions import Resolver404

from myWeb import views


class PortfolioUrlTests(TestCase):

    def test_url_resolves_to_portfolio_view(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func, views.portfolio_view)

    def test_url_name_is_portfolio(self):
        resolver = resolve('/')
        self.assertEqual(resolver.url_name, 'portfolio')

    def test_url_has_no_namespace(self):
        resolver = resolve('/')
        self.assertEqual(resolver.namespace, '')

    def test_reverse_returns_root_path(self):
        self.assertEqual(reverse('portfolio'), '/')

    def test_reverse_and_resolve_are_consistent(self):
        url = reverse('portfolio')
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.portfolio_view)

    def test_unknown_path_raises_resolver404(self):
        with self.assertRaises(Resolver404):
            resolve('/does-not-exist/')

    def test_trailing_slash_route(self):
        resolver = resolve('/')
        self.assertEqual(resolver.route, '')

    def test_url_kwargs_and_args_are_empty(self):
        resolver = resolve('/')
        self.assertEqual(resolver.args, ())
        self.assertEqual(resolver.kwargs, {})