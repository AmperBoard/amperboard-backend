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

    hours = int(params_days) * 24 if params_days is not None else 0

    if timestamp is None:
        date = timezone.now()
    else:
        date = datetime.fromtimestamp(int(timestamp))

    user_config = UserConfig.objects.all().first()

    latitude = float(user_config.latitude) if user_config.latitude is not None else 0.0
    longitude = float(user_config.longitude) if user_config.longitude is not None else 0.0
    square_meters = float(user_config.square_meters) if user_config.square_meters is not None else 0.0
    efficiency = 0.1

    radiations = []

    for x in range(1, hours):
        current_date = date - timedelta(hours=x)

        altitude_deg = get_altitude(latitude, longitude, current_date)

        altitude_deg = max(0, altitude_deg)

        azimuth_deg = get_azimuth(latitude, longitude, current_date)

        radiation_hour = get_radiation_direct(date, altitude_deg)

        final_radiation_hour = radiation_hour * efficiency * square_meters

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
