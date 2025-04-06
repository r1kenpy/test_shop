from cart.cart import Cart
from django.shortcuts import render

from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()  # Проверка на пустую корзину
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            order_created.delay(order.id)

            cart.clear()
            return render(
                request, 'orders/order/created.html', {'order': order}
            )
    else:
        form = OrderCreateForm()
    return render(
        request, 'orders/order/create.html', {'cart': cart, 'form': form}
    )
