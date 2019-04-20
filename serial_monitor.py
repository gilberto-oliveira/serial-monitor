import io
import re
import serial
import threading
import logging

from push_client import PushClient


class SerialMonitor (threading.Thread):
    def __init__(self, config, push_client: PushClient):
        super().__init__()
        self.next_data = 0
        self.prev_data = 0
        self.push_client = push_client
        try:
            self.ser = serial.Serial(
                port=config['serial_port'],
                baudrate=config['serial_baudrate'],
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=config['serial_timeout']
            )
            self.sio = io.TextIOWrapper(
                buffer=io.BufferedRWPair(self.ser, self.ser),
            )
        except (serial.SerialException, AttributeError) as e:
            logging.error('Exception Occurred: %s', e)
            exit(-1)
        else:
            logging.info('Listening the Serial %s Port\n', self.ser.portstr)

    def run(self):
        while self.ser.is_open:
            data = self.sio.readline()
            try:
                if not data.isprintable():
                    self.next_data = int(re.sub("[^-0-9]", "", data.split(':')[1]))
                    if self.next_data > 0 and self.next_data != self.prev_data:
                        response = self.__send_push_notification(self.next_data)
                        if response is not None:
                            logging.info(response)
                    elif self.next_data < 0 <= self.prev_data:
                        response = self.__send_push_notification(0)
                        if response is not None:
                            logging.info(response)
                    self.prev_data = self.next_data
            except (ValueError, IndexError) as e:
                logging.error('Exception Occurred: %s', e)

    def __send_push_notification(self, message):
        return self.push_client.send_push(message=message)
