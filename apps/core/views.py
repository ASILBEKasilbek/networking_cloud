from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    """Login page with demo users."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Noto'g'ri foydalanuvchi nomi yoki parol"

    return render(request, 'login.html', {'error': error})


@login_required(login_url='/')
def dashboard_view(request):
    """Role-based dashboard."""
    user = request.user
    role = getattr(user, 'role', 'customer')
    
    role_display_map = {
        'admin': 'Administrator',
        'manager': 'Manager',
        'sales': 'Sales',
        'warehouse': 'Warehouse',
        'finance': 'Finance',
        'customer': 'Customer',
    }
    
    # Stats based on role
    stats_map = {
        'admin': [
            {'icon': 'fa-users', 'value': '156', 'label': 'Foydalanuvchilar', 'bg': '#dbeafe', 'color': '#1d4ed8'},
            {'icon': 'fa-shopping-cart', 'value': '1,247', 'label': 'Buyurtmalar', 'bg': '#d1fae5', 'color': '#059669'},
            {'icon': 'fa-boxes-stacked', 'value': '3,891', 'label': 'Mahsulotlar', 'bg': '#fef3c7', 'color': '#d97706'},
            {'icon': 'fa-dollar-sign', 'value': '$284K', 'label': 'Daromad', 'bg': '#fce7f3', 'color': '#db2777'},
        ],
        'manager': [
            {'icon': 'fa-chart-line', 'value': '$47.2K', 'label': 'Bugungi sotuv', 'bg': '#d1fae5', 'color': '#059669'},
            {'icon': 'fa-shopping-cart', 'value': '89', 'label': 'Yangi buyurtmalar', 'bg': '#dbeafe', 'color': '#1d4ed8'},
            {'icon': 'fa-users', 'value': '34', 'label': 'Faol mijozlar', 'bg': '#fef3c7', 'color': '#d97706'},
            {'icon': 'fa-truck', 'value': '12', 'label': 'Yuborilmoqda', 'bg': '#e0e7ff', 'color': '#4338ca'},
        ],
        'sales': [
            {'icon': 'fa-shopping-cart', 'value': '23', 'label': 'Mening buyurtmalarim', 'bg': '#d1fae5', 'color': '#059669'},
            {'icon': 'fa-user-plus', 'value': '8', 'label': 'Yangi mijozlar', 'bg': '#dbeafe', 'color': '#1d4ed8'},
            {'icon': 'fa-dollar-sign', 'value': '$12.4K', 'label': 'Bugungi sotuv', 'bg': '#fef3c7', 'color': '#d97706'},
            {'icon': 'fa-bullseye', 'value': '78%', 'label': 'Target', 'bg': '#fce7f3', 'color': '#db2777'},
        ],
        'warehouse': [
            {'icon': 'fa-boxes-stacked', 'value': '3,891', 'label': 'Mahsulotlar', 'bg': '#e0e7ff', 'color': '#4338ca'},
            {'icon': 'fa-clipboard-list', 'value': '15', 'label': 'Pick Lists', 'bg': '#dbeafe', 'color': '#1d4ed8'},
            {'icon': 'fa-truck', 'value': '7', 'label': 'Yuborish kutilmoqda', 'bg': '#d1fae5', 'color': '#059669'},
            {'icon': 'fa-exclamation-triangle', 'value': '23', 'label': 'Kam qolgan', 'bg': '#fef3c7', 'color': '#d97706'},
        ],
        'finance': [
            {'icon': 'fa-dollar-sign', 'value': '$284K', 'label': 'Oylik daromad', 'bg': '#d1fae5', 'color': '#059669'},
            {'icon': 'fa-file-invoice', 'value': '45', 'label': "To'lanmagan", 'bg': '#fce7f3', 'color': '#db2777'},
            {'icon': 'fa-hand-holding-usd', 'value': '$18.7K', 'label': 'Bugungi tushumlar', 'bg': '#dbeafe', 'color': '#1d4ed8'},
            {'icon': 'fa-chart-pie', 'value': '12.3%', 'label': "Foyda o'sishi", 'bg': '#fef3c7', 'color': '#d97706'},
        ],
        'customer': [
            {'icon': 'fa-shopping-bag', 'value': '12', 'label': 'Buyurtmalarim', 'bg': '#dbeafe', 'color': '#1d4ed8'},
            {'icon': 'fa-truck', 'value': '3', 'label': "Yo'lda", 'bg': '#d1fae5', 'color': '#059669'},
            {'icon': 'fa-box', 'value': '9', 'label': 'Yetkazilgan', 'bg': '#fef3c7', 'color': '#d97706'},
            {'icon': 'fa-star', 'value': '4.8', 'label': 'Reyting', 'bg': '#fce7f3', 'color': '#db2777'},
        ],
    }

    context = {
        'user': user,
        'role': role,
        'role_display': role_display_map.get(role, 'User'),
        'stats': stats_map.get(role, stats_map['customer']),
    }
    return render(request, 'dashboard.html', context)


def logout_view(request):
    """Logout and redirect to login."""
    logout(request)
    return redirect('login')
