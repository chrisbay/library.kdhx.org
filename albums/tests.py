from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.db.utils import IntegrityError
from albums import views
from albums.models import MediaType
import re


class AlbumsTest(TestCase):

    @classmethod
    def remove_csrf_input(cls, html):
        return re.sub((r'<input\stype=["\']hidden["\']\sname=["\']'
                       r'csrfmiddlewaretoken["\']\svalue=["\']\w+["\']\s/>'),
                      '', html)

    def test_albums_root_resolves_to_index(self):
        found = resolve('/albums/')
        self.assertEqual(found.func, views.index)

    def test_albums_index_returns_correct_html(self):
        request = HttpRequest()
        response = views.index(request)
        view_args = {'message': 'Albums Index',
                     'page_title': 'Albums'}
        expected_html = render_to_string('albums/index.jinja', view_args)
        self.assertEqual(response.content.decode(), expected_html)

    def test_albums_new_resolves_to_new(self):
        found = resolve('/albums/new/')
        self.assertEqual(found.func.view_class, views.AlbumCreate)

    # TODO - Fix this. View isn't rendering properly
    """
    def test_albums_new_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'GET'
        response = views.AlbumCreate.as_view()(request)
        expected_html = render_to_string('albums/album_form.jinja',
                                         {'page_title': 'New Album'})
        self.assertEqual(response.content.decode(), expected_html)
    """