from django.shortcuts import render, redirect,get_list_or_404,get_object_or_404
from .models import Store, Snack, StoreSnack,Product,Supremarket
from django.http import Http404,HttpResponseNotFound,HttpResponse
from openpyxl import Workbook
from django.http import HttpResponseBadRequest
# from openpyxl.writer.excel import save_virtual_workbook
from io import BytesIO

def add_store(request):
    if request.method == 'POST':
        storename = request.POST['storename']
        store = Store.objects.create(storename=storename)

        snack_names = request.POST.getlist('snack_name')
        quantities = request.POST.getlist('qty')
        rates = request.POST.getlist('rate')

        for name, qty, rate in zip(snack_names, quantities, rates):
            if name and qty and rate:
                snack, created = Snack.objects.get_or_create(name=name)
                StoreSnack.objects.create(store=store, snack=snack, qty=qty, rate=rate)

        return redirect('store_list')

    return render(request, 'app2/add_store.html')

def store_list(request):
    stores = Store.objects.all()
    return render(request, 'app2/store_list.html', {'stores': stores})
def delete_list(request,id):
    try:
        store = get_object_or_404(Store,id=id)
        # print(store.storename)
    except Store.DoesNotExist:
        return HttpResponseNotFound("Models not found")
    if request.method == "POST":
        print('test')
        store.delete()
        return redirect('store_list')
    return render(request,'app2/delete_list.html',{'store':store})

def productadd(request):
    if request.method == "POST":
        productname = request.POST.get('productname').strip()       
        productcode = request.POST.get('productcode').strip()
        cost = request.POST.get('price').strip()
        product = Product.objects.all()
        
        if not productname or not productcode or not cost:
            return render(request,'app2/productadd.html',{'error_message':'Please Enter All fields','products': product,'productname':productname,
                'productcode':productcode,
                'cost':cost})
        
        if productname and cost and productcode:
            Product.objects.create(productname=productname,productcode=productcode,cost=cost)
            return redirect('productadd')
        else:
            context={
                'productname':productname,
                'productcode':productcode,
                'cost':cost
            }
            return render(request,'app2/productadd.html',context)
            
    product = Product.objects.all().order_by('-id')
    count = Product.objects.count()
    return render(request,'app2/productadd.html',{'products': product,'count':count})
    
def deleteproduct(request,id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        return redirect('productadd')
    return render(request,'app2/productadd.html',{'product':product})
def updateproduct(request,id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        productname = request.POST.get('productname','').strip()
        productcode = request.POST.get('productcode','').strip()
        cost = request.POST.get('price','').strip()
        if not productname or not productcode or not cost:
            return render(request,'app2/productupdate.html',{'error_message':'Please enter all fields','productname':productname,'productcode':productcode,'cost':cost})

        product.productname=request.POST.get('productname') 
        product.productcode=request.POST.get('productcode') 
        product.cost=request.POST.get('price') 
        product.save()
        return redirect('productadd')
    return render(request,'app2/productupdate.html',{'product':product})

def addstore(request):
    if request.method == "POST":
        storename = request.POST.get('storename').strip()
        invoiceno = request.POST.get('invoiceno').strip()
        date = request.POST.get('date')

        # Validate store details
        if not storename or not invoiceno or not date:
            return render(request, 'app2/addstore.html', {
                'error_message': 'Please enter all store details',
                'products': Product.objects.all()
            })

        # Process each product entry
        product_index = 0
        while True:
            product_id = request.POST.get(f'products[{product_index}][product]')
            pieces = request.POST.get(f'products[{product_index}][pieces]')
            units = request.POST.get(f'products[{product_index}][units]')
            amount = request.POST.get(f'products[{product_index}][amount]')

            if not product_id:
                break  # Exit loop if no more products are found

            # Validate product data
            if not pieces or not units or not amount:
                return render(request, 'app2/addstore.html', {
                    'error_message': f'Product data missing for index {product_index}',
                    'products': Product.objects.all()
                })

            try:
                product = Product.objects.get(id=product_id)
                # Create a Supremarket entry for each product
                Supremarket.objects.create(
                    storename=storename,
                    invoiceno=invoiceno,
                    date=date,
                    product=product,
                    pieces=pieces,
                    units=units,
                    amount=amount
                )
            except Product.DoesNotExist:
                return render(request, 'app2/addstore.html', {
                    'error_message': f'Product with ID {product_id} does not exist',
                    'products': Product.objects.all()
                })

            product_index += 1

        return redirect('addstore')
    products = Product.objects.all()
    
    demo={}
    try:
        # supre = Supremarket.objects.values('storename')
        storing = Supremarket.objects.all().values()
        print(storing)
        for i in storing:
            a=i.get('storename')
            if a not in demo:
                demo[a]=[]
            demo[a].append(i)
        print(demo)
    except Exception as e:
        print(str(e))

    return render(request, 'app2/addstore.html', {
        'demo': demo,'products':products
    })

def deletestore(request,storename):
    a=Supremarket.objects.filter(storename=storename)
    if request.method=="POST":
        a.delete()
        return redirect('addstore')
    return render(request,'app2/addstrore.html')

def updatestore(request, storename):
    stores = Supremarket.objects.filter(storename=storename)
    if not stores:
        return HttpResponse('not store')

    if request.method == "POST":
        storename = request.POST.get('storename')
        invoiceno = request.POST.get('invoiceno')
        date = request.POST.get('date')

        # Validate store details
        if not storename or not invoiceno or not date:
            return render(request, 'app2/addstore.html', {
                'error_message': 'Please enter all store details',
                'products': Product.objects.all(),
                'store': stores.first() if stores.exists() else None
            })

        # Update or create store details
        for store in stores:
            store.storename = storename
            store.invoiceno = invoiceno
            store.date = date
            store.save()

        # Handle product data
        product_index = 0
        while True:
            product_id = request.POST.get(f'products[{product_index}][product]')
            pieces = request.POST.get(f'products[{product_index}][pieces]')
            units = request.POST.get(f'products[{product_index}][units]')
            amount = request.POST.get(f'products[{product_index}][amount]')

            if not product_id:
                break

            # Validate product data
            if not pieces or not units or not amount:
                return render(request, 'app2/addstore.html', {
                    'error_message': f'Product data missing for index {product_index}',
                    'products': Product.objects.all(),
                    'store': stores.first() if stores.exists() else None
                })

            try:
                product = Product.objects.get(id=product_id)
                Supremarket.objects.update_or_create(
                    storename=storename,
                    invoiceno=invoiceno,
                    date=date,
                    product=product,
                    defaults={
                        'pieces': pieces,
                        'units': units,
                        'amount': amount
                    }
                )
            except Product.DoesNotExist:
                return render(request, 'app2/addstore.html', {
                    'error_message': f'Product with ID {product_id} does not exist',
                    'products': Product.objects.all(),
                    'store': stores.first() if stores.exists() else None
                })

            product_index += 1

        # return redirect('liststores')

    products = Product.objects.all()

    return render(request, 'app2/addstoreupdate.html', {
        'products': products
    })



def export_products_to_excel(request):
    # Create a workbook and a worksheet
 if request.method == "GET":
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Products'

    # Add column headers
    headers = ['Product Name', 'Product Code', 'Cost']
    worksheet.append(headers)

    # Fetch data from the database
    products = Product.objects.all()

    # Add data rows to the worksheet
    for product in products:
        worksheet.append([
            product.productname,
            product.productcode,
            product.cost,
        ])

    # Save workbook to BytesIO
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Create HTTP response
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'
    return response


def storing(request):
    demo={}
    try:
        # supre = Supremarket.objects.values('storename')
        storing = Supremarket.objects.all().values()
        print(storing)
        for i in storing:
            a=i.get('storename')
            if a not in demo:
                demo[a]=[]
            demo[a].append(i)
        print(demo)
    except Exception as e:
        print(str(e))
    return render(request,'app2/list.html',{'demo':demo})

def deletestoring(request,storename):
    a=Supremarket.objects.filter(storename=storename)
    if request.method=="POST":
        a.delete()
        return redirect('storing')
    return render(request,'app2/list.html')
from app2.models import demo
import json
from django.http import JsonResponse
    
def demoving(request):
    if request.method == 'POST':
        c=request.body
        print(c)
        data = json.loads(c)
        print(data)
        name = data.get('name')
        price = data.get('price')
        a=demo.objects.create(name=name,price=price)
        a.save()
        return JsonResponse({'id': a.id, 'name': a.name, 'price': str(a.price)})
    return render(request,'app2/list3.html')

    
        
