
"""
    Url paterns for search app

"""


from django.urls import path, include
from rest_framework import routers

from search_app.api.drf.views import SearchViewSet

# Create a router to generate automatically all paths on de viewset
router = routers.SimpleRouter()

router.register(r'', SearchViewSet)


urlpatterns = [
    # Using include to maintain flexibility to change anytime the path
    path('', include(router.urls)),
]
