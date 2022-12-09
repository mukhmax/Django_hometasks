from django.urls import path
from measurement.views import SensorCreateView, SensorModifyView, SensorsListView, MeasurementAddView, SensorDataView

urlpatterns = [
    path('create_sensor/', SensorCreateView.as_view()),
    path('modify/<pk>/', SensorModifyView.as_view()),
    path('add-measurement/', MeasurementAddView.as_view()),
    path('sensors-list/', SensorsListView.as_view()),
    path('sensor-data/<pk>/', SensorDataView.as_view()),
    path('pictures/<pk>', SensorDataView.as_view()),
]
