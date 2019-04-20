from push_client import PushClient
from serial_monitor import SerialMonitor
import logging
import datetime

# monitor configs
config = {
    'serial_baudrate': 115200,
    'serial_port': 'COM4',
    'serial_timeout': .2,
    'service_name': 'SerialMonitorTRF01',
    'message_channel': 'BalancaTrefila1',
    'message_event': 'MessageProcessed',
    'server_url': 'localhost',
    'server_port': 4478,
    'request_url': '/api/push/notify',
}

if __name__ == '__main__':
    now = datetime.datetime.now()
    # logging config
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        handlers=[
            logging.FileHandler(
                filename="C:\\SerialMonitor\\logs\\log_{0}-{1}-{2}_trf01.log".format(now.day, now.month, now.year),
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]
    )

    logging.info('Starting Serial Monitor Log from %s', config['service_name'])

    # starting monitor service
    push_client = PushClient(config=config)
    serial_monitor = SerialMonitor(config=config, push_client=push_client)
    serial_monitor.start()
