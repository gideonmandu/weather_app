from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for
import requests
import pprint
from datetime import datetime


def api_current(city_name: str) -> 'responce object':
    API_key = '436def745939eb9ec905541ccadac792'
    return requests.get(
        url=f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}'
    )


def api_5days(city_name: str) -> 'responce object':
    API_key = '436def745939eb9ec905541ccadac792'
    return requests.get(
        url=f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={API_key}'
    )


bp = Blueprint(name='home', import_name=__name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    """
    Home page for application
    """
    if request.method != 'POST':
        return render_template('public/index.html')
    # call api request function
    city = request.form['search']
    api_resp = api_current(city_name=city)
    if api_resp.status_code == 200:
        location_data = api_resp.json()
        time = datetime.fromtimestamp(location_data['dt']).time()
        date = datetime.fromtimestamp(location_data['dt']).date()
        ss = datetime.fromtimestamp(location_data['sys']['sunset']).time()
        sr = datetime.fromtimestamp(location_data['sys']['sunrise']).time()
    else:
        print('NO data for current Location')
        message = 'No data for Location Provided'
        return render_template('public/index.html', message=message)

    return render_template('public/index.html', location_data=location_data, time=time, date=date, sunrise=sr, sunset=ss)


# resp = api_current(city_name='moscow')
# print(datetime.now().date())
# print(datetime.now().time() >= datetime.utcfromtimestamp(1615982400).time())
# datetime.utcoffset
# pprint.pprint(resp.json())
# print(type(resp))
