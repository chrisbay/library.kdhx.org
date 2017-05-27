from django.urls import resolve
from django.test import TestCase
from . import views
from django.http import HttpRequest
from django.template.loader import render_to_string


class AlbumsTest(TestCase):

    def test_albums_root_resolves_to_index(self):
        found = resolve('/albums/')
        self.assertEqual(found.func, views.index)

    
    def test_albums_index_returns_correct_html(self):
        request = HttpRequest()
        response = views.index(request)
        expected_html = render_to_string('albums/index.html', 
            {'message': 'Albums Index', 'page_title': 'Albums'})
        self.assertEqual(response.content.decode(), expected_html)


    def test_albums_new_resolves_to_new(self):
        found = resolve('/albums/new/')
        self.assertEqual(found.func, views.new)


    def test_albums_new_returns_correct_html(self):
        request = HttpRequest()
        response = views.new(request)
        expected_html = render_to_string('albums/new.html', 
            {'page_title': 'New Album'})
        self.assertEqual(response.content.decode(), expected_html)