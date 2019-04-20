import http.client
import json
import socket
import logging


class MessageEventArgs(object):
    def __init__(self, data: str, channel: str, event: str, origin: str):
        self.data = data
        self.channel = channel
        self.eventname = event
        self.origin = origin


class PushClient:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.try_connect()

    def try_connect(self):
        try:
            self.connection = http.client.HTTPConnection(self.config['server_url'], self.config['server_port'])
        except (ValueError, http.HTTPException) as e:
            logging.error('Exception Occurred: %s', e)
            exit(-1)
        else:
            logging.info('Successfully connected to SignalR Push Server in %s:%s', self.connection.host,
                         self.connection.port)

    def send_push(self, message: str):
        headers = {'Content-type': 'application/json'}
        try:
            data = MessageEventArgs(
                data=message,
                channel=self.config['message_channel'],
                event=self.config['message_event'],
                origin=self.config['service_name']
            )
            send_data = json.dumps(data.__dict__)
            self.connection.request('POST', self.config['request_url'], send_data, headers)
        except (ConnectionResetError, ConnectionRefusedError, socket.gaierror) as e:
            logging.error('Exception Occurred: %s', e)
            logging.info('Trying reconnecting to SignalR Push Server')
            self.try_connect()
        else:
            response = self.connection.getresponse()
            return response.read().decode()
