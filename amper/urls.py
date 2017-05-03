from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from amper.views import radiation_day
from amper.viewsets import ItemViewSet, ReportViewSet, UserConfigViewSet, DayViewSet, CapacityHourViewSet, \
    RealTimeDataViewSet

router = DefaultRouter()

router.register(r'items', ItemViewSet, 'items')
router.register(r'reports', ReportViewSet, 'reports')
router.register(r'days', DayViewSet, 'days')
router.register(r'user-config', UserConfigViewSet, 'user-config')
router.register(r'capacity-hour', CapacityHourViewSet, 'capacity-hour')
router.register(r'real-time-data', RealTimeDataViewSet, 'real-time-data')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^historical-generation/', radiation_day),
]
