import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


def repeats(flag):
    for x in Country.query.all():
        if x.flags == flag:
            return x.countryName
    return "False"


def weather(city):
    string = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=44e59f3c7e5f1b6ae6a16b8eff82baa3&units=metric'
    r = requests.get(string)
    return r.json()['main']['temp']


def weather_icon_id(city):
    string = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=44e59f3c7e5f1b6ae6a16b8eff82baa3&units=metric'
    r = requests.get(string)
    return r.json()['weather'][-1]['icon']


def aua(string):
    return type(string)


def result_page(country_name):
    country = Country.query.filter_by(countryName=country_name).first()
    return render_template('result.html', offName=country.offName, weather=weather(country.capital),
                           region=country.region + "\t(" + country.subregion + ")",
                           currenciesName=country.currenciesName + "\t'" + country.curSymbol + "'",
                           name=country.nativeName, capital=country.capital,
                           lng=country.languages, population=country.population, area=country.area, flag=country.flags,
                           text="https://openweathermap.org/img/wn/" + weather_icon_id(country.capital) + "@2x.png")


def lng_list(dict):
    s = ''
    for x in dict:
        s = s + str(dict[x]) + ', '
    return (s[:-2])


def country_exist(name):
    for x in Country.query.all():
        if x.countryName == name:
            return "db"
    if request_num(name) == 200:
        return "api"
    return "error"


def json_text(country):
    url = "https://restcountries.com/v3.1/name/" + country
    r = requests.get(url)
    return r.json()


def request_num(country):
    url = "https://restcountries.com/v3.1/name/" + country
    r = requests.get(url)
    return r.status_code


@app.route('/result', methods=['GET', 'POST'])
def result():
    if country_exist(request.form['country']) == "db":
        return result_page(request.form['country'])
    elif country_exist(request.form['country']) == "api":
        data = json_text(request.form['country'])[0]
        name = str(data['name']['common'])
        offName = data['name']['official']
        nativeName = data['name']['nativeName'][(list(data['name']['nativeName'])[0])]['official']
        currency = data['currencies'][list(data['currencies'])[0]]
        currenciesName = currency['name']
        curSymbol = currency['symbol']
        region = data['region']
        subregion = data['subregion']
        lng = data['languages']
        language = lng_list(data['languages'])
        capital = data['capital'][0]
        area = data['area']
        population = data['population']
        flag = data['flags']['png']
        if repeats(flag) == 'False':
            add_to_db(request.form['country'], offName, nativeName, currenciesName, curSymbol, capital, region,
                      subregion,
                      language, population, area, flag)
            return result_page(request.form['country'])
        else:
            return result_page(repeats(flag))


    elif country_exist(request.form['country']) == "error":
        country = request.form['country']
        if len(request.form['country']) == 0:
            country = "'NULL'"
        return render_template('errorPage.html', country=country)


@app.route('/')
def index():
    return render_template('text.html')


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    countryName = db.Column(db.String, unique=True, nullable=False)
    offName = db.Column(db.String)
    nativeName = db.Column(db.String)
    currenciesName = db.Column(db.String)
    curSymbol = db.Column(db.String)
    capital = db.Column(db.String)
    region = db.Column(db.String)
    subregion = db.Column(db.String)
    languages = db.Column(db.String)
    population = db.Column(db.String)
    area = db.Column(db.String)
    flags = db.Column(db.String)


def add_to_db(countryName, offName, nativeName, currenciesName, curSymbol, capital, region, subregion, languages,
              population, area, flags):
    with app.app_context():
        country = Country(countryName=countryName, offName=offName, nativeName=nativeName,
                          currenciesName=currenciesName, curSymbol=curSymbol, capital=capital, region=region,
                          subregion=subregion, languages=languages, population=population, area=area, flags=flags)
        db.session.add(country)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
