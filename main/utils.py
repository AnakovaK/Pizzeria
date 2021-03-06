import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'get_bonus_points': 0}
    notifications = order['get_cart_items']

    for i in cart:
        try:
            notifications += cart[i]["quantity"]

            pizza = Pizza.objects.get(id=i)
            total = (pizza.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'pizza': {
                    'id': pizza.id,
                    'name': pizza.name,
                    'price': pizza.price,
                    'imageURL': pizza.imageURL,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)
        except:
            pass
    return {'notifications': notifications, 'order': order, 'items': items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        notifications = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        notifications = cookieData['notifications']
        order = cookieData['order']
        items = cookieData['items']
    return {'notifications': notifications, 'order': order, 'items': items}
