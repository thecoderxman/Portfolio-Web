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
import investpy
import urllib, base64
import quandl
from forex_python.converter import CurrencyRates
from datetime import  timedelta


#------work on this (As everything is on landing page)------------------------------------

def index(request):
	#intialize variables that we are going to pass
	price=0.0
	m=money.objects.get(pk=1)
	amount=m.mymoney
	amount=round(amount, 2)
	rem=1000000-amount
	rem=round(rem, 2)
	close=[]
	import yfinance as yf
	close1=yf.download("AAPL",'2020-01-01',date.today())
	close1=close1['Close'].tolist()
	close2=yf.download("TSLA",'2020-01-01',date.today())
	close2=close2['Close'].tolist()
	no=[]
	no1=['a','b','c','d','e']
	no2=[]
	sdate1 = date(2020,1, 1) 
	edate1 = date.today()
	delta1 = edate1 - sdate1  
	for i in range(delta1.days + 1):
	    day = sdate1 + timedelta(days=i)
	    no1.append((day))
	diff=len(no1)-len(close1)
	for i in range(diff):
		no1.remove(no1[i])
	for i in range(len(close2)):
		no2.append(i+1)
	s=""
	labels = []
	datap = []
	DataFrame3="Table for Particular Stock"
	#fetch recent 10 investments
	query_results= investments.objects.all().order_by('-id')[:10]
	last_stock=0
	if request.method == 'POST' :
		#for buy stock,available assets,investments and pushing purcahses into investment table
		if('stockname' in request.POST) :
			n=request.POST['stockname']
			api_key = 'BJQZ9I2H012Q7FDD'
			#code for profit loss returns none if no query found so used if condition
			last_stock=investments.objects.filter(name = n).values('id', 'price').last()
			ts = TimeSeries(key=api_key, output_format='json')
			data, meta_data = ts.get_quote_endpoint(n)
			#get price  real-time 
			price=float(data['05. price'])
			price=round(price, 2)
			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:#assigned price because profit or loss=0 if we are adding it to table first time(assumption)
				last_stock=price
			
			if(price!=0.0):
				if(amount>price):
					amount=amount-price
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price-last_stock
					last_stock=round(last_stock,2)
					a = investments(name=n.upper(),price=price,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			#for table start to end
		elif('sn'in  request.POST):
			DataFrame3=yf.download(request.POST['sn'],request.POST['sdate1'],request.POST['edate1'])
			DataFrame3=DataFrame3.to_html()
			#for graphs start to end
		else:
			DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
			DataFrame1 = yf.download("AAPL",request.POST['sdate'],request.POST['edate'])
			DataFrame2 = yf.download("TSLA",request.POST['sdate'],request.POST['edate'])
			close=DataFrame['Close'].tolist()
			close1=DataFrame1['Close'].tolist()
			close2=DataFrame2['Close'].tolist()
			s=str(request.POST['s'])
			no=[]
			no1=[]
			no2=[]
			for i in range(len(close)):
				no.append(i+1)
			for i in range(len(close1)):
				no1.append(i+1)
			for i in range(len(close2)):
				no2.append(i+1)
		 
	d=dict()
	#for pie chart getting all investemnts summing up the stock by their labels
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
	#returning all the calculates values to html
	return render(request, 'portfolio/index.html',{'labels':labels,'datap':datap,'price':price,'amount':amount,'query_results':query_results,'rem':rem,'close':close,'no':no,'s':s,'close1':close1,'close2':close2,'no1':no1,'no2':no2,'DataFrame3':DataFrame3})

#work end
# not needed now--------------------------------------------------------------------------
def funds(request):
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
	n="Funds name"
	for i in range(len(close)):
				no.append(i+1)
	for i in range(len(close1)):
		no1.append(i+1)
	for i in range(len(close2)):
		no2.append(i+1)

	s=""
	labels = []
	datap = []
	DataFrame3="Table for Particular Stock"
	indianfunds=['Icici Prudential Life - Balancer Fund','Hdfc Standard Life - Balanced Managed Investment Pension']
	#fetch recent 10 investments
	query_results= investmentsinfunds.objects.all().order_by('-id')[:10]
	last_stock=0
	v1=0
	if request.method == 'POST' :
		#for buy stock,available assets,investments and pushing purcahses into investment table
		if('stockname' in request.POST) :
			n=request.POST['stockname']
			#api_key = 'BJQZ9I2H012Q7FDD'
			#code for profit loss returns none if no query found so used if condition
			last_stock=investmentsinfunds.objects.filter(name = n).values('id', 'price').last()
			#ts = TimeSeries(key=api_key, output_format='json')
			#data, meta_data = ts.get_quote_endpoint(n)
			#get price  real-time 
			if(n in indianfunds):
				v1=investpy.funds.get_fund_recent_data(fund=n, country='india', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close']
				v1=float(v1)
				c = CurrencyRates()
				inrtousd=c.get_rate('INR','USD') 
				v1=v1*inrtousd
				price=round(v1,2)
			else:
				v1=float(investpy.funds.get_fund_recent_data(fund=n, country='united states', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close'])
				price=round(v1,2)
			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:#assigned price because profit or loss=0 if we are adding it to table first time(assumption)
				last_stock=price
			
			if(price!=0.0):
				if(amount>price):
					amount=amount-price
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price-last_stock
					last_stock=round(last_stock,2)
					a = investmentsinfunds(name=n.upper(),price=price,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			#for table start to end
		elif('sn'in  request.POST):
			a11=request.POST['sdate1']
			import datetime
			darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
			darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
			darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
			a11=request.POST['edate1']
			edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
			edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
			edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)

			if(request.POST['sn'] in indianfunds):
				DataFrame3=investpy.get_fund_historical_data(fund=request.POST['sn'], country='india',from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
				
			else:
				DataFrame3=investpy.get_fund_historical_data(fund=request.POST['sn'], country='united states',from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
			DataFrame3=DataFrame3.to_html()
			#for graphs start to end
		
		else:
			a11=request.POST['sdate']
			import datetime
			darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
			darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
			darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
			a11=request.POST['edate']
			edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
			edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
			edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
			if(request.POST['s'] in indianfunds):
				DataFrame=investpy.get_fund_historical_data(fund=request.POST['s'], country='india',from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
				
			else:
				DataFrame=investpy.get_fund_historical_data(fund=request.POST['s'], country='united states',from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
			#DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
			close=DataFrame['Close'].tolist()
			s=str(request.POST['s'])
			sdate2=date(int(darevy), int(darevm), int(darevd))
			edate2=date(int(edarevy), int(edarevm), int(edarevd)) 
			delta2 = edate2 - sdate2 
			for i in range(delta2.days + 1):
			    day = sdate2 + timedelta(days=i)
			    no.append(str(day))
			diff=len(no)-len(close)
			for i in range(1,diff+1):
				no.remove(no[i])

		 
	d=dict()
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset = investmentsinfunds.objects.order_by('name')
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
	#returning all the calculates values to html
	return render(request, 'portfolio/funds.html',{'n':n,'labels':labels,'datap':datap,'price':price,'amount':amount,'query_results':query_results,'rem':rem,'close':close,'no':no,'s':s,'close1':close1,'close2':close2,'no1':no1,'no2':no2,'DataFrame3':DataFrame3})
def bonds(request):
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
	n="Funds name"
	s=""
	labels = []
	datap = []
	DataFrame3="Table for Particular Stock"
	indianfunds=['India 10Y','India 30Y','India 24Y','India 15Y']
	#fetch recent 10 investments
	query_results= investmentsinbonds.objects.all().order_by('-id')[:10]
	last_stock=0
	v1=0
	if request.method == 'POST' :
		#for buy stock,available assets,investments and pushing purcahses into investment table
		if('stockname' in request.POST) :
			n=request.POST['stockname']
			#api_key = 'BJQZ9I2H012Q7FDD'
			#code for profit loss returns none if no query found so used if condition
			last_stock=investmentsinbonds.objects.filter(name = n).values('id', 'price').last()
			#ts = TimeSeries(key=api_key, output_format='json')
			#data, meta_data = ts.get_quote_endpoint(n)
			#get price  real-time 
			if(n in indianfunds):
				v1=investpy.bonds.get_bond_recent_data(bond=n, as_json=False, order='descending', interval='Daily').iloc[0,:]['Close']
				v1=float(v1)
				c = CurrencyRates()
				inrtousd=c.get_rate('INR','USD') 
				v1=v1*inrtousd
				price=round(v1,2)
			else:
				v1=float(investpy.bonds.get_bond_recent_data(bond=n, as_json=False, order='descending', interval='Daily').iloc[0,:]['Close'])
				price=round(v1,2)
			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:#assigned price because profit or loss=0 if we are adding it to table first time(assumption)
				last_stock=price
			
			if(price!=0.0):
				if(amount>price):
					amount=amount-price
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price-last_stock
					last_stock=round(last_stock,2)
					a = investmentsinbonds(name=n.upper(),price=price,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			#for table start to end
		elif('sn'in  request.POST):
			a11=request.POST['sdate1']
			import datetime
			darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
			darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
			darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
			a11=request.POST['edate1']
			edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
			edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
			edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)

			if(request.POST['sn'] in indianfunds):
				DataFrame3=investpy.get_bond_historical_data(bond=request.POST['sn'],from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
				
			else:
				DataFrame3=investpy.get_bond_historical_data(bond=request.POST['sn'],from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
			DataFrame3=DataFrame3.to_html()
			#for graphs start to end
		
		else:
			a11=request.POST['sdate']
			import datetime
			darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
			darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
			darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
			a11=request.POST['edate']
			edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
			edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
			edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
			if(request.POST['s'] in indianfunds):
				DataFrame=investpy.get_bond_historical_data(bond=request.POST['s'],from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
				
			else:
				DataFrame=investpy.get_bond_historical_data(bond=request.POST['s'],from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
			#DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
			close=DataFrame['Close'].tolist()
			s=str(request.POST['s'])
			sdate2=date(int(darevy), int(darevm), int(darevd))
			edate2=date(int(edarevy), int(edarevm), int(edarevd)) 
			delta2 = edate2 - sdate2 
			for i in range(delta2.days + 1):
			    day = sdate2 + timedelta(days=i)
			    no.append(str(day))
			diff=len(no)-len(close)
			for i in range(1,diff+1):
				no.remove(no[i])

		 
	d=dict()
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset = investmentsinbonds.objects.order_by('name')
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
	#returning all the calculates values to html
	return render(request, 'portfolio/bonds.html',{'n':n,'labels':labels,'datap':datap,'price':price,'amount':amount,'query_results':query_results,'rem':rem,'close':close,'no':no,'s':s,'close1':close1,'close2':close2,'no1':no1,'no2':no2,'DataFrame3':DataFrame3})	
