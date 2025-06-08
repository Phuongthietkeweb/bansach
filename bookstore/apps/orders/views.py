from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from decimal import Decimal
from .models import Order, OrderItem
from .forms import CheckoutForm
from books.models import Book
from cart.views import get_cart

def order_list_view(request):
    """Lịch sử đơn hàng"""
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders/order_list.html', {'orders': orders})
    else:
        return HttpResponse('''
        <h1>📋 Lịch sử đơn hàng</h1>
        <p>Bạn cần đăng nhập để xem lịch sử đơn hàng.</p>
        <a href="/accounts/login/">Đăng nhập</a> | 
        <a href="/books/">Mua sắm ngay</a> | 
        <a href="/">← Về trang chủ</a>
        ''')

def order_create_view(request):
    """Tạo đơn hàng"""
    return HttpResponse('''
    <h1>📝 Tạo đơn hàng mới</h1>
    <p>Chức năng tạo đơn hàng đang được phát triển.</p>
    <a href="/cart/">← Về giỏ hàng</a>
    ''')

def checkout_view(request):
    """Thanh toán"""
    # Lấy giỏ hàng từ session
    cart = get_cart(request)
    
    if not cart:
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart:detail')
    
    # Tính toán thông tin giỏ hàng
    cart_items = []
    total_price = Decimal('0.000')
    total_quantity = 0
    
    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=int(book_id))
            # Kiểm tra tồn kho
            if book.stock < quantity:
                messages.error(request, f'Sách "{book.title}" chỉ còn {book.stock} cuốn trong kho!')
                return redirect('cart:detail')
            
            # Sử dụng giá đã giảm thay vì giá gốc
            discounted_price = book.get_discounted_price()
            item_total = discounted_price * quantity
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'item_total': item_total,
                'discounted_price': discounted_price
            })
            total_price += item_total
            total_quantity += quantity
        except Book.DoesNotExist:
            messages.error(request, 'Có sản phẩm trong giỏ hàng không tồn tại!')
            return redirect('cart:detail')
    
    # Tính phí ship (ví dụ: miễn phí ship từ 200k, dưới 200k tính 30k)
    shipping_fee = Decimal('0.000') if total_price >= Decimal('200.000') else Decimal('30.000')
    final_total = total_price + shipping_fee
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Tạo đơn hàng
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    order.total_amount = total_price
                    order.shipping_fee = shipping_fee
                    order.save()
                    
                    # Tạo chi tiết đơn hàng và cập nhật tồn kho
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            book=item['book'],
                            quantity=item['quantity'],
                            price=item['discounted_price']
                        )
                        # Giảm tồn kho
                        item['book'].stock -= item['quantity']
                        item['book'].save()
                    
                    # Xóa giỏ hàng
                    request.session['cart'] = {}
                    request.session.modified = True
                    
                    messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: #{order.id}')
                    return redirect('orders:detail', order_id=order.id)
                    
            except Exception as e:
                messages.error(request, 'Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại.')
    else:
        form = CheckoutForm(user=request.user)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_fee': shipping_fee,
        'final_total': final_total,
        'total_quantity': total_quantity,
        'page_title': 'Thanh toán'
    }
    
    return render(request, 'orders/checkout.html', context)

def order_detail_view(request, order_id):
    """Chi tiết đơn hàng"""
    try:
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=order_id, user=request.user)
        else:
            order = get_object_or_404(Order, id=order_id)
        
        return render(request, 'orders/order_detail.html', {'order': order})
    except:
        return HttpResponse(f'''
        <h1>📄 Chi tiết đơn hàng #{order_id}</h1>
        <p>Không tìm thấy đơn hàng hoặc bạn không có quyền xem đơn hàng này.</p>
        <a href="/orders/">← Về lịch sử đơn hàng</a>
        ''')
