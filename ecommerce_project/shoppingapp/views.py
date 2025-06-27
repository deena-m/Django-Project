from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.db.models import Avg, Sum
from django.http import HttpResponse
from collections import Counter
import openpyxl
from datetime import datetime


def dashboard(request):
    year = request.GET.get('year')
    current_year = datetime.now().year
    selected_year = int(year) if year else current_year

    products = Product.objects.filter(date_added__year=selected_year)

    total_sales = products.aggregate(total=Sum('sales'))['total'] or 0
    avg_price = products.aggregate(avg=Avg('price'))['avg'] or 0
    sold_out_count = products.filter(sales=0).count()
    sold_count = products.exclude(sales=0).count()

    labels = [product.name for product in products]
    sales = [product.sales for product in products]
    prices = [float(product.price) for product in products]

    categories = [product.category for product in products]
    category_counts_dict = Counter(categories)
    category_labels = list(category_counts_dict.keys())
    category_counts = list(category_counts_dict.values())

    context = {
        'products': products,
        'total_sales': total_sales,
        'avg_price': f"{avg_price:.2f}",
        'sold_out_count': sold_out_count,
        'sold_count': sold_count,
        'labels': labels,
        'sales': sales,
        'prices': prices,
        'category_labels': category_labels,
        'category_counts': category_counts,
        'selected_year': selected_year,
        'year_range': [2024, 2025]
    }
    return render(request, 'shoppingapp/dashboard.html', context)


def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        sales = request.POST['sales']
        category = request.POST['category']
        Product.objects.create(name=name, price=price, sales=sales, category=category)
    return redirect('dashboard')


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('dashboard')


def export_to_excel(request):
    year = request.GET.get('year')
    selected_year = int(year) if year else datetime.now().year
    products = Product.objects.filter(date_added__year=selected_year)

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = f"Products_{selected_year}"

    worksheet.append(['Name', 'Price', 'Sales', 'Category', 'Date Added'])

    for p in products:
        worksheet.append([p.name, float(p.price), p.sales, p.category, p.date_added.strftime('%Y-%m-%d')])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"Products_{selected_year}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    workbook.save(response)

    return response
