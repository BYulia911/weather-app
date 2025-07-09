from flask import Flask, render_template, request, url_for
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "7b38bb005411c5ce0fb9610d02fdd90f"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru"
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.json()
                # Обработка даты и времени
                for item in weather_data['list']:
                    dt_str = item['dt_txt']
                    dt_object = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                    item['formatted_date'] = dt_object.strftime('%d.%m')
                    item['formatted_time'] = dt_object.strftime('%H:%M')

                    description = item['weather'][0]['description'].capitalize()
                    hour = dt_object.hour
                    match description:
                        case "Ясно":
                            if hour >= 22 or hour < 4:
                                item['image'] = url_for('static', filename='images/moon.png')
                            else:
                                item['image'] = url_for('static', filename='images/clear.png')
                        case "Облачно":
                            item['image'] = url_for('static', filename="images/clouds.png")
                        case "Дождь":
                            item['image'] = url_for('static', filename='images/rain.png')
                        case "Снег":
                            item['image'] = url_for('static', filename="images/snow.png")
                        case "Туман":
                            item['image'] = url_for('static', filename="images/fog.png")
                        case "Небольшой дождь":
                            item['image'] = url_for('static', filename="images/light_rain.png")
                        case _:
                            item['image'] = url_for('static', filename="images/default.png")
            else:
                error_message = "Ошибка при получении данных о погоде. Проверьте название города."

    return render_template("index.html", weather_data=weather_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True, port=5001)