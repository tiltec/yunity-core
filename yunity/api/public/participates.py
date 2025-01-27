from django.conf.urls import url
from django.http import HttpRequest
from django.views.generic import View

from yunity.api.ids import participate_id_uri_pattern
from yunity.utils.api.abc import ApiBase


class Participates(ApiBase, View):
    def get(self, request):
        """list all participates of this user

        :type request: HttpRequest
        """
        raise NotImplementedError

    def post(self, request):
        """create a new participate

        :type request: HttpRequest
        """
        raise NotImplementedError


class Participate(ApiBase, View):
    def get(self, request, participateid):
        """return details about this participate

        :type request: HttpRequest
        :type participateid: int
        """
        raise NotImplementedError

    def put(self, request, participateid):
        """modify the participate, e.g. approve it

        :type request: HttpRequest
        :type participateid: int
        """
        raise NotImplementedError

    def delete(self, request, participateid):
        """unrequest the participate

        :type request: HttpRequest
        :type participateid: int
        """
        raise NotImplementedError


urlpatterns = [
    url(r'^$', Participates.as_view()),
    url(r'^{participateid}/?$'.format(participateid=participate_id_uri_pattern), Participate.as_view()),
]
