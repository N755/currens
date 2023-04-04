import csv
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

with open('currens.csv', 'w', newline='', encoding='utf-8') as file:
    fields = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(file, delimiter=';', fieldnames=fields)
    writer.writeheader()
    for rate in data[0]['rates']:
        writer.writerow({'currency': rate["currency"], 'code': rate["code"], 'bid': rate["bid"], 'ask': rate["ask"]})

rates = {}
with open('currens.csv', newline='', encoding='utf-8') as csvfile:
    reader=csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        currency = row['currency']
        code = row['code']
        bid = float(row['bid'])
        ask = float(row['ask'])
        rates[currency] = [code, bid, ask]

def calculate_result(amount, ask):
    return float(amount)*float(ask)


@app.route('/', methods=['GET','POST'])
def calculate():
    items = rates.keys()
    result=calculate_result    # як зробити щоб на початковій сторінці був пустий результат а не Result: <function calculate_result at 0x000001D17B56B1C0>
    if request.method == 'GET':
        return render_template('currens.html', items=items, result=result)
    if request.method == 'POST':
        data = request.form
        amount = data.get('amount')
        code = data.get('code')
        ask = float(rates[currency][2])
        costs = calculate_result(float(amount), float(ask))
        result = f"{amount} {code} costs {costs:.2f} PLN"
        return render_template('currens.html', items=items, result=result)

if __name__ == '__main__':
    app.run(debug=True)
