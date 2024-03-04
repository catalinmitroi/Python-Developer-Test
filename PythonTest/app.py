import requests
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def weather():
    connect = sqlite3.connect('database.db')
    connect.execute('CREATE TABLE IF NOT EXISTS forecast (name VARCHAR(255), data DATE NOT NULL, max_temp DOUBLE NOT NULL, min_temp DOUBLE NOT NULL, total_precip DOUBLE NOT NULL, sunrise HOUR NOT NULL, sunset HOUR NOT NULL)')

    api_key = 'a2489a45e4624e6a969144138242302'
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'Bucharest'

    response = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3")


    resp = response.json()

    data = {
        "date" : resp['forecast']['forecastday'],
        "city" : resp['location']['name'],
    }
    with sqlite3.connect("database.db") as con:
        c = con.cursor()
        c.execute("DELETE FROM forecast WHERE name=?", (city,))
        con.commit()
    for i in range(3):
        date = resp['forecast']['forecastday'][i]['date']
        name = resp['location']['name']
        max_temp = resp['forecast']['forecastday'][i]['day']['maxtemp_c']
        min_temp = resp['forecast']['forecastday'][i]['day']['mintemp_c']
        total_prec = resp['forecast']['forecastday'][i]['day']['totalprecip_mm']
        sunrise = resp['forecast']['forecastday'][i]['astro']['sunrise']
        sunset =  resp['forecast']['forecastday'][i]['astro']['sunset']

        with sqlite3.connect("database.db") as con:
            c = con.cursor()
            c.execute("INSERT INTO forecast (name, data, max_temp, min_temp, total_precip, sunrise, sunset) VALUES (?,?,?,?,?,?,?)", (name, date, max_temp, min_temp, total_prec, sunrise, sunset))
            con.commit()

    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run()