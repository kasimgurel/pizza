from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Pizza menüsü
pizzas = [
    {"name": "Margarita", "price": 10},
    {"name": "Karışık", "price": 12},
    {"name": "Ton Balıklı", "price": 14},
    {"name": "Sucuklu", "price": 13},
]

@app.route('/')
def index():
    return render_template('menu.html', pizzas=pizzas)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pizza_name = request.form['pizza_name']
    size = request.form['size']
    price = next(pizza['price'] for pizza in pizzas if pizza['name'] == pizza_name)
    if size == 'large':
        price += 2

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({"name": pizza_name, "size": size, "price": price})
    session.modified = True

    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/checkout', methods=['POST'])
def checkout():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    # Burada siparişi işletmeye gönderme işlemini gerçekleştirebilirsiniz
    session.pop('cart', None)
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)