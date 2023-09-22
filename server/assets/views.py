from django.shortcuts import render, redirect
from assets.models import Asset
# Create your views here.
# Create Employee

def insert_asset(request):
    if request.method == "POST":
        ticker = request.POST['ticker'] 
        category = request.POST['category']
        name = request.POST['name']
        description = request.POST['description'] 
        data = Asset(ticker=ticker, category=category, name=name,  description= description)
        data.save()
  
        return redirect('show/')
    else:
        return render(request, 'insert.html')
    

# Retrive assets 
        
def show_asset(request):
    assets = Asset.objects.all()
    return render(request,'show.html',{'Assets':assets} )

def edit_asset(request,pk):
    assets = Asset.objects.get(id=pk)
    if request.method == 'POST':
        return redirect('/show')

    context = {
        'assets': assets,
    }

    return render(request,'edit.html',context)

def remove_asset(request, pk):
    assets = Asset.objects.get(id=pk)

    if request.method == 'POST':
        assets.delete()
        return redirect('/show')

    context = {
        'assets': assets,
    }

    return render(request, 'delete.html', context)