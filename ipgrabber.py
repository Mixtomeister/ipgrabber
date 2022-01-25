import os
import sys
import logging
import pyfiglet

from datetime import datetime

from flask import Flask, redirect, request

from requests import get


logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

logger = logging.getLogger(__name__)

fieldnames = [
    'host', 'ip', 'rdns', 'asn', 'isp', 'country_name',
    'country_code', 'region_name', 'region_code', 'city',
    'postal_code', 'continent_name', 'continent_code', 'latitude',
    'longitude', 'metro_code', 'timezone', 'datetime', 'user_agent'
]

app = Flask(__name__)


def print_header():
    print(f'{pyfiglet.figlet_format("IPGRABBER")}By Ivan Galvez\n')
    print(f'Link to share: http://{get_public_ip()}:8080\n')
    print(f'Connections:')

def get_public_ip():
    return get('https://api.ipify.org').content.decode('utf8')

@app.route('/')
def index():
    datenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    response = get(
        method='GET',
        headers={'User-Agent': 'keycdn-tools:https://www.example.com'},
        url=f'https://tools.keycdn.com/geo.json?host={request.remote_addr}'
    )

    response.raise_for_status()

    data = response.json()

    if data['status'] == 'success':
        ip_data = data['data']['geo']
        ip_data['user_agent'] = request.user_agent
        ip_data['datetime'] = datenow

        print(f"[{datenow}] {ip_data['ip']} - {ip_data['country_name']} - {ip_data['region_name']} - {ip_data['isp']} - {ip_data['user_agent']}")

    return redirect(sys.argv[1])


if __name__ == '__main__':

    print_header()

    app.run(host='0.0.0.0', port=8080)
