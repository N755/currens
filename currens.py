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
currens_name = []
with open('currens.csv', newline='', encoding='utf-8') as csvfile:
    reader=csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        currency = row['currency']
        code = row['code']
        bid = float(row['bid'])
        ask = float(row['ask'])
        rates[currency] = [code, bid, ask]

def calculate_result(amount, ask):
    return (amount*ask)


@app.route('/', methods=['GET','POST'])
def calculate():
    items = rates.keys()
    result = " "
    if request.method == 'POST':
        data = request.form
        amount = float(data.get('amount'))
        code = data.get('code')
        for currency in rates:
            if rates[currency][0] == code:
                name_currency = currency
                ask = float(rates[currency][2])
                costs = calculate_result(amount, ask)
                result = f"{amount} {name_currency} costs {costs:.2f} PLN"
                print(result)
        return render_template('currens.html', items=items, result=result)
    



if __name__ == '__main__':
    app.run(debug=True)
