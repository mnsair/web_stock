from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages



def home(request):
	return render(request, 'home.html',{})

def USStock(request):

	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_f9c004537c87492c833385d1e2c9c2d7")

		try:
			api = json.loads(api_request.content)

		except Exception as e:
			api = "Error"
		return render(request, 'USStock.html', {'api': api})

	else:
		return render(request, 'USStock.html', {'ticker': "Enter Ticker Symbol Above"})


def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added!"))
			return redirect('add_stock')

	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_f9c004537c87492c833385d1e2c9c2d7")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error"

		return render(request, 'add_stock.html',{'ticker': ticker, 'output': output})




def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been Deleted!"))
	return redirect(Delete_Stock)

def Delete_Stock(request):
	ticker = Stock.objects.all()
	return render(request, 'Delete_Stock.html', {'ticker': ticker})