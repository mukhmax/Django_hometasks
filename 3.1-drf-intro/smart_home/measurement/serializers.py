from rest_framework import serializers
from measurement.models import Sensor, Measurement


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        ordering = '-id'


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class SensorMeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            'temperature',
            'time',
            'picture',
        )


class SensorDataSerializer(serializers.ModelSerializer):
    measurements = SensorMeasurementsSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = (
            'id',
            'name',
            'description',
            'measurements',
        )
