import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = ''
INFLUXDB_USER = ''
INFLUXDB_PASSWORD = ''
INFLUXDB_DATABASE = ''

MQTT_ADDRESS = 'test.mosquitto.org'
MQTT_USER = 'mqtt'
MQTT_PASSWORD = 'coba'
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'local'

influxdb_client = InfluxDBClient(host=INFLUXDB_ADDRESS, port=8086, username=INFLUXDB_USER, password=INFLUXDB_PASSWORD, database=INFLUXDB_DATABASE)

BUCKET_NAME='Powermonitoring'
INFLUX_URL=''
ORG=''
QUERY_URI='http://{}:8086/api/v2/write?org={}&bucket={}&precision=ms'.format(INFLUX_URL,ORG,BUCKET_NAME)
INFLUX_TOKEN='h2pO0IzV8OiP8aCtRzAgudY9W0DIiX-m5OQhSAf-7USCEjH8OBDZdoue5upJjW5Lw8EBUZWUnrMtN0eORZFTfA==' #Put your INFLUX KEY here
headers = {}
headers['Authorization'] = 'Token {}'.format(INFLUX_TOKEN)

class SensorData(NamedTuple):
    location: str
    measurement: str
    #value: float
    value: str

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        location = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        #return SensorData(location, measurement, float(payload))
        return SensorData(location, measurement, payload)
    else:
        return None

def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    #influxdb_client.write_points(json_body)
    import requests
    r = requests.post(QUERY_URI, data=json_body, headers=headers)
    print( r.status_code )

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)

def _init_influxdb_database():
    databases = QUERY_URI.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        QUERY_URI.create_database(INFLUXDB_DATABASE)
    QUERY_URI.switch_database(INFLUXDB_DATABASE)

def main():
    #_init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    main()
    print('MQTT to InfluxDB bridge')