from datetime import datetime, timedelta

from pysolar.solar import get_altitude, get_azimuth
from pysolar.radiation import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

from amper.models import UserConfig


@api_view()
def radiation_day(request):
    timestamp = request.query_params.get("timestamp")

    if timestamp is None:
        date = datetime.now()
    else:
        date = datetime.fromtimestamp(int(timestamp))

    date = datetime(year=date.year, month=date.month, day=date.day, hour=date.hour, minute=0, second=0, microsecond=0)

    radiations = []

    for x in range(1, 25):
        current_date = date - timedelta(hours=x)

        user_config = UserConfig.objects.all().first()

        altitude_deg = get_altitude(float(user_config.latitude), float(user_config.longitude), current_date)
        azimuth_deg = get_azimuth(float(user_config.latitude), float(user_config.longitude), current_date)
        radiation_hour = get_radiation_direct(when=date, altitude_deg=altitude_deg)

        final_radiation_hour = radiation_hour * 0.15 * float(user_config.square_meters)

        radiations.append({
            "hour": current_date.hour,
            "radiation": final_radiation_hour
        })

    return Response(radiations)