from flask import Flask, redirect, url_for, render_template,request,jsonify
import requests
from bs4 import BeautifulSoup
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml#"
response = {}
app = Flask(__name__)

@app.route('/update')
def update_data():
    s = requests.get(url)
    soup = BeautifulSoup(s.text,'lxml')
    raw = soup.find('div',id='1896310216')
    states = raw.find_all('td',class_="s19")
    for i in range(len(states)):
        p = states[i].find_parent('tr')
        cases = p.find_all('td',class_="s72")
        response[str(states[i].text).lower()]={"Confirmed":cases[0].text,"Active":cases[1].text,"Deceased":cases[2].text}
    return ''

@app.route('/')
def hello_world():
    if(not bool(response)):
        update_data()
    return render_template("template.html",response=response)

@app.route('/api/tracker')
def api_state():
    if 'state' in request.args:
        state = str(request.args['state']).lower()
    else:
        return("ERROR: No state is mentioned")

    if state in response.keys():
        return jsonify(response[state])
    else:
        return("State not found")

if __name__ == '__main__':
   app.run()