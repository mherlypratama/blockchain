from flask import Flask, render_template

app = Flask(__name__, template_folder='template')

my_dict = {
    'id': [1, 2, 3, 4, 5],
    'product_name': ['product1', 'product2', 'product3', 'product4', 'product5'],
    'value': [200, 400, 600, 800, 1000],
    'available_qty': [1, 2, 3, 2, 4]
}

all_headers = list(my_dict.keys())

all_rows = list(zip(*my_dict.values()))


@app.route('/')
def table():
    return render_template('table.html', all_headers=all_headers, all_rows=all_rows)


if __name__ == "__main__":
    app.run(debug=True)
