from django.shortcuts import render,redirect
from .models import snacks,store
from django.http import Http404

def snack_list(request):
    snack=snacks.objects.all()
    return render(request,'app/snacks_list.html',{'snack':snack})
def store_list(request):
    storelist=store.objects.all()
    return render(request,'app/store_list.html',{'storelist':storelist})
def add_snacks(request):
    if request.method == "POST":
        name=request.POST.get("name")
        if name:
            if snacks.objects.filter(name__iexact=name).exists():
                return render(request,'app/add_snacks.html', {
                                  'error_message':'The snacks already added.',
                                  'name':name
                              })
            snacks.objects.create(name=name)
            return redirect('snacks_list')
    return render(request,'app/add_snacks.html')
# def add_store(request):
#     if request.method == "POST":
#         storename=request.POST.get("storename")
#         snacks_id=request.POST.getlist("snacks")
#         qty=request.POST.get("qty")
#         rate=request.POST.get("rate")
        
#         # snack= snacks.objects.get(id=snacks_id) if snacks_id else None
#         # print(snack)
        
#         if not storename and not qty and not rate:
#             return render(request,'app/add_store.html',{"error_message": "Please enter all values"
#             })
        
#         # if storename and qty and rate:
#         #     store.objects.create(storename=storename,snacks=snack,qty=qty,rate=rate)
#         #     return redirect('store_list')
#         stores = store(storename=storename,qty=qty,rate=rate)
#         stores.save()
        
#         for snack_id in snacks_id:
#             snack = snacks.object.get(id=snack_id)
#             stores.snacks.add(snack)
    
#     snack = snacks.objects.all()
#     return render(request,'app/add_store.html',{'snack':snack})

# def delete_snack(request,snack_id):
#     try:
#         snack = snacks.objects.get(id=snack_id)
#     except snacks.DoesNotExist:
#         return Http404("Snack does not exists")
    
#     if request.method == "POST":
#         snack.delete()
#         return redirect("snack_list")
#     return render(request,'app/delete.html',{'snack':snack})

# from django.shortcuts import render, redirect
# from .models import Store, Snacks

def add_store(request):
    if request.method == "POST":
        storename = request.POST.get("storename")
        snacks_ids = request.POST.getlist("snacks")
        qty = request.POST.get("qty")
        rate = request.POST.get("rate")
        
        if not storename or not qty or not rate:
            return render(request, 'app/add_store.html', {"error_message": "Please enter all values"})
        
        # Create the Store instance
        store_instance = store(storename=storename, qty=qty, rate=rate)
        store_instance.save()
        
        # Add snacks to the store
        for snack_id in snacks_ids:
            print(snack_id)
            snack = snacks.objects.get(id=snack_id)
            store_instance.snacks.add(snack)
        
        return redirect('store_list')
    
    snack = snacks.objects.all()
    return render(request, 'app/add_store.html', {'snack': snack})

    # if request.method == "POST":
    #     storename = request.POST.get("storename")
    #     snacks_ids = request.POST.getlist("snacks")
    #     qty = request.POST.get("qty")
    #     rate = request.POST.get("rate")
        
    #     snack=snacks(storename=storename,qty=qty,rate=rate)
    #     snack.save()
        
    #     if not storename or not qty or not rate:
    #         error_message = "Please enter all details"
    #         return render(request,'app/add_store.html',{'error_message':error_message})
        
    #     for snack_id in snacks_ids:
    #         snack1 = snacks.objects.get(id=snack_id)
    #         snack.snacks.add(snack1)
    #     return redirect('store_list')
    # stores=store.obejcts.all()
    # return render(request,'app/add_store.html',{'stores':stores})
    
def delete_store(request,store_id):
    try:
        stores = store.objects.get(id=store_id)
    except store.DoesNotExist:
        raise Http404('Store does not exists')
    if request.method == "POST":
        stores.delete()
        return redirect('store_list')
    return render(request,'app/delete.html',{'store': stores})

def update_store(request,store_id):
    try:
        stores = store.objects.get(id=store_id)
    except store.DoesNotExist:
        return Http404("Store does not exists")
    
    if request.method == "POST":
        stores.storename=request.POST.get('storename')
        stores.qty=request.POST.get('qty')
        stores.rate=request.POST.get('rate')
        stores_snacks=request.POST.getlist('snacks')
        # a=snacks.objects.filter(id__in=stores_snacks)
        # stores.snacks.set(a)
        selected_snacks = snacks.objects.filter(id__in=stores_snacks)
        stores.snacks.set(selected_snacks)
        stores.save()
        return redirect('store_list')
    snack=snacks.objects.all()
    return render(request,'app/update.html',{'store': stores,'snack':snack})
        
        


        
