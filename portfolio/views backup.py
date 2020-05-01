from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from datetime import date
import time
import yfinance as yf  
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from .forms import nameofstock
from django.db.models import Sum
import io
import urllib, base64
import quandl
# Create your views here.

def sales(request):
	return render(request,'portfolio/sales.html')

def tables(request):
	DataFrame="Table for Particular Stock"
	if request.method == 'POST':
		#sd=str(request.POST['sdate'])
		#print(request.POST['edate'])
		#print(sd)
		#print(request.POST['s'])
		#DataFrame = yf.download('GOOG',sd,ed)
		DataFrame=yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
		DataFrame=DataFrame.to_html()
	return render(request,'portfolio/tables.html',{'DataFrame':DataFrame})

def pie_chart(request):
	labels = []
	datap = []
	d=dict()
	queryset = investments.objects.order_by('name')
	for stock in queryset:
		labels.append(stock.name)
		datap.append(stock.price)
	for i in range(len(labels)):
		if(labels[i] in d.keys()):
			d[labels[i]]+=datap[i]
		else:
			d[labels[i]]=datap[i]
	labels=list(d.keys())
	datap=list(d.values())
	
	return render(request, 'portfolio/pie_chart.html',{
			'labels': labels,
			'datap': datap,
		})
		
def index(request):
	form = nameofstock()
	price=0.0
	m=money.objects.get(pk=1)
	amount=m.mymoney
	amount=round(amount, 2)
	rem=1000000-amount
	rem=round(rem, 2)
	close=[]
	close1=[]
	close2=[]
	no=[]
	no1=[]
	no2=[]
	s=""
	labels = []
	datap = []
	DataFrame3="Table for Particular Stock"
	#rem=investments.objects.filter(field_name__isnull=True).aggregate(Sum('price'))
	query_results= investments.objects.all().order_by('-id')[:10]
	if request.method == 'POST':
		if('stockname' in request.POST):
			form = nameofstock(request.POST)
			n=form.data['stockname']
			api_key = 'BJQZ9I2H012Q7FDD'
			ts = TimeSeries(key=api_key, output_format='json')
			data, meta_data = ts.get_quote_endpoint(n)
			price=float(data['05. price'])
			price=round(price, 2)
			if(price!=0.0):
				if(amount>price):
					amount=amount-price
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					a = investments(name=n.upper(),price=price,date_created=str(date.today()),current_time=current_time)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			#rem=investments.objects.filter(price__isnull=True).aggregate(Sum('price'))
			
			#if form.is_valid():
			#	pass
		elif('sn'in  request.POST):
			DataFrame3=yf.download(request.POST['sn'],request.POST['sdate1'],request.POST['edate1'])
			DataFrame3=DataFrame3.to_html()
		else:
			DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
			DataFrame1 = yf.download("AAPL",request.POST['sdate'],request.POST['edate'])
			DataFrame2 = yf.download("TSLA",request.POST['sdate'],request.POST['edate'])
			close=DataFrame['Close'].tolist()
			close1=DataFrame1['Close'].tolist()
			close2=DataFrame2['Close'].tolist()
			s=str(request.POST['s'])
			for i in range(len(close)):
				no.append(i+1)
			for i in range(len(close1)):
				no1.append(i+1)
			for i in range(len(close2)):
				no2.append(i+1)
		
	d=dict()
	queryset = investments.objects.order_by('name')
	for stock in queryset:
		labels.append(stock.name)
		datap.append(stock.price)
	for i in range(len(labels)):
		if(labels[i] in d.keys()):
			d[labels[i]]+=datap[i]
		else:
			d[labels[i]]=datap[i]
	labels=list(d.keys())
	datap=list(d.values())
	
	return render(request, 'portfolio/index.html',{'labels':labels,'datap':datap,'form':form,'price':price,'amount':amount,'query_results':query_results,'rem':rem,'close':close,'no':no,'s':s,'close1':close1,'close2':close2,'no1':no1,'no2':no2,'DataFrame3':DataFrame3})


def analytics(request):
	#DataFrame=pd.DataFrame(index=[], columns=[])
	close=[]
	close1=[]
	close2=[]
	no=[]
	no1=[]
	no2=[]
	s=""
	if request.method == 'POST':
		DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
		DataFrame1 = yf.download("AAPL",request.POST['sdate'],request.POST['edate'])
		DataFrame2 = yf.download("TSLA",request.POST['sdate'],request.POST['edate'])
		close=DataFrame['Close'].tolist()
		close1=DataFrame1['Close'].tolist()
		close2=DataFrame2['Close'].tolist()
		s=str(request.POST['s'])
		for i in range(len(close)):
			no.append(i+1)
		for i in range(len(close1)):
			no1.append(i+1)
		for i in range(len(close2)):
			no2.append(i+1)
	return render(request,'portfolio/analytics.html',{'close':close,'no':no,'s':s,'close1':close1,'close2':close2,'no1':no1,'no2':no2})