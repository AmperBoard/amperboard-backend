from rest_framework import serializers

from amper import utils
from amper.models import Item, Report, CapacityHour, Day, UserConfig, RealTimeData


class ItemSerializer(utils.RelationModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "consumption")


class ReportSerializer(utils.RelationModelSerializer):
    item = ItemSerializer(is_relation=True)

    def create(self, validated_data):
        return super(ReportSerializer, self).create(validated_data=validated_data)

    class Meta:
        model = Report
        fields = ("id", "item", "start_time", "duration", "consumption")


class CapacityHourSerializer(utils.RelationModelSerializer):
    class Meta:
        model = CapacityHour
        fields = ("id", "hour", "capacity")


class DaySerializer(utils.RelationModelSerializer):
    date = serializers.DateTimeField(required=False)
    reports = ReportSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        report_data = self.context["request"].data.get("report")
        item_data = report_data["item"]

        report_data["item"] = Item.objects.get(pk=int(item_data.get("id")))

        report = Report.objects.create(**report_data)

        instance.reports.add(report)
        return instance

    class Meta:
        model = Day
        fields = ("id", "reports", "capacity", "date")


class RealTimeDataSerializer(utils.RelationModelSerializer):
    consumption = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=True, required=False)
    produced = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=True, required=False)

    class Meta:
        model = RealTimeData
        fields = ("id", "consumption", "produced")


class UserConfigSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        config = UserConfig.objects.all()
        if config.exists():
            config.update(**validated_data)
            return config.first()
        else:
            return super(UserConfigSerializer, self).create(validated_data=validated_data)

    class Meta:
        model = UserConfig
        fields = ("latitude", "longitude", "place_id", "address", "solar_panel_angle", "square_meters")
