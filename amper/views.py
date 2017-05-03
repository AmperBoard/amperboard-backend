from datetime import datetime, timezone, timedelta

from django.utils import timezone
from pysolar.radiation import *
from pysolar.solar import get_altitude, get_azimuth
from rest_framework.decorators import api_view
from rest_framework.response import Response

from amper.models import UserConfig, Report
from amper.serializers import ReportSerializer


@api_view()
def historical_generation(request):
    timestamp = request.query_params.get("timestamp")
    params_days = request.query_params.get("days")

    days = int(params_days) if params_days is not None else 0

    if timestamp is None:
        date = timezone.now()
    else:
        date = datetime.fromtimestamp(int(timestamp))

    radiations = []

    for x in range(1, days + 1):
        current_date = date - timedelta(hours=x)

        user_config = UserConfig.objects.all().first()

        altitude_deg = get_altitude(float(user_config.latitude), float(user_config.longitude), current_date)

        altitude_deg = max(0, altitude_deg)

        azimuth_deg = get_azimuth(float(user_config.latitude), float(user_config.longitude), current_date)

        radiation_hour = get_radiation_direct(when=date, altitude_deg=altitude_deg)

        efficiency = 0.1

        final_radiation_hour = radiation_hour * efficiency * float(user_config.square_meters)

        radiations.append({
            "hour": current_date.hour,
            "energy": final_radiation_hour
        })

    return Response(radiations)


@api_view()
def historical_consumption(request):
    timestamp = request.query_params.get("timestamp")
    params_days = request.query_params.get("days")

    days = int(params_days) if params_days is not None else 0

    if timestamp is None:
        date = timezone.now()
    else:
        date = datetime.fromtimestamp(int(timestamp))

    reports = Report.objects.filter(start_time__lte=date - timedelta(days=days))

    serializer_class = ReportSerializer(reports, many=True)

    return Response(serializer_class.data)
