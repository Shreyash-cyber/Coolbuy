from django import template

register = template.Library()

@register.filter(name='total_price')
def total_cart_price(item, cart):
    sum = 0
    for p in item:
        sum += p.price
    return sum 


@register.filter(name='total_actual_price')
def total_actual_cart_price(item, cart):
    sum = 0
    for a in item:
        sum += a.actual_price
    return sum

@register.filter(name='discount_price')
def discount_cart_price(item, cart):
    return (total_cart_price(item, cart) - total_actual_cart_price(item, cart))

@register.filter(name='cart_size')
def cart_size(item, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == item.id:
            return cart.get(id)
    return 'Regular';
