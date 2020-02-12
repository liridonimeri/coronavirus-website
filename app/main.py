#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from data import DataModel
from timeloop import Timeloop
from datetime import timedelta
import json

tl = Timeloop()

app = Flask(__name__)

global dataStored


@tl.job(interval=timedelta(seconds=10))
def fetch_data():
    dataStored.pull_data()


@app.route('/')
def index():
    d = dataStored.get_latest_value()['data']
    _deaths = d['Deaths']
    _confirmed = d['Confirmed']
    _recovered = d['Recovered']

    return render_template('index.html', deaths=_deaths, confirmed=_confirmed, recovered=_recovered)


@app.route('/api/latest')
def api_latest():
    d = dataStored.get_latest_value()
    return json.dumps(d)


@app.route('/api/by_country')
def api_by_country():
    d = dataStored.get_latest_value()
    return json.dumps(d)


if __name__ == '__main__':
    dataStored = DataModel()

    tl.start()

    app.run(host='0.0.0.0', port=5000, debug=True)

    tl.stop()
