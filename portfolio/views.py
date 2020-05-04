from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from datetime import date
import time,random
import yfinance as yf  
import matplotlib.pyplot as plt
from datetime import datetime
from .forms import nameofstock
import io
from django.db.models import Sum
import investpy
import urllib, base64
import quandl
import json
from forex_python.converter import CurrencyRates
from datetime import  timedelta
from nsepy import get_history
from nsepy.derivatives import get_expiry_date

#------work on this (As everything is on landing page)------------------------------------
def dash(request):
	ass1=[]
	cdate= str(date.today())
	rst1= yf.download('NFLX','2020-03-01',cdate)
	close11=rst1['Close'].tolist()
	rst2= yf.download('MSFT','2020-03-01',cdate)
	close22=rst2['Close'].tolist()
	import datetime
	s1='NFLX'
	s2='MSFT'
	v123=""
	no11=[]
	no22=[]
	sdate11=datetime.datetime.strptime('2020-03-01', "%Y-%m-%d").date()
	edate11=datetime.datetime.strptime(cdate, "%Y-%m-%d").date()
	sdate22=datetime.datetime.strptime('2020-03-01', "%Y-%m-%d").date()
	edate22=datetime.datetime.strptime(cdate, "%Y-%m-%d").date()
	delta = edate11 - sdate11
	for i in range(delta.days + 1):
		day = sdate11+ timedelta(days=i)
		no11.append(str(day))
	diff=len(no11)-len(close11)
	for i in range(1,diff+1):
		no11.remove(no11[i])
	delta = edate22 - sdate22
	for i in range(delta.days + 1):
		day = sdate22+ timedelta(days=i)
		no22.append(str(day))
	diff=len(no22)-len(close22)
	for i in range(1,diff+1):
		no22.remove(no22[i])

	a21=investments.objects.aggregate(t=Sum('price'))['t']
	a22=investmentsincommodities.objects.aggregate(t=Sum('price'))['t']
	a23=investmentsinfunds.objects.aggregate(t=Sum('price'))['t']
	a24=investmentsinbonds.objects.aggregate(t=Sum('price'))['t']
	a25=investmentsinfutures.objects.aggregate(t=Sum('price'))['t']
	a26=investmentsinindices.objects.aggregate(t=Sum('price'))['t']
	datapinall=[a21,a22,a23,a24,a25,a26]
	labelsinall=['Stock','Commodities','Funds','Bonds','Futures','Indices']
	indianbonds=['India 10Y','India 30Y','India 24Y','India 15Y']
	indianfunds=['Icici Prudential Life - Balancer Fund','Hdfc Standard Life - Balanced Managed Investment Pension']
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
	n1=""
	n2=""
	n3=""
	n4=""
	n5=""
	n6=""
	st=""
	price1=0.0
	price2=0.0
	price3=0.0
	price4=0.0
	price5=0.0
	price6=0.0
	n=""
	s=""
	labels = []
	datap = []
	DataFrame3="Table"
	#fetch recent 10 investments
	query_results1= investments.objects.all().order_by('-id')[:10]
	query_results2= investmentsincommodities.objects.all().order_by('-id')[:10]
	query_results3= investmentsinbonds.objects.all().order_by('-id')[:10]
	query_results4= investmentsinfunds.objects.all().order_by('-id')[:10]
	query_results5= investmentsinfutures.objects.all().order_by('-id')[:10]
	query_results6= investmentsinindices.objects.all().order_by('-id')[:10]
	indianindices=['BSE Healthcare','BSE Teck','BNY Mellon India ADR TR','BSE IT']
	last_stock=0
	v1=0
	assname=[]
	if request.method == 'POST' :
		if('assname1') in request.POST:
			stocks=['NFLX','FB','AAPL','MSFT']
			bonds=['India 10Y',"India 30Y","India 24Y","India 15Y","U.S. 10Y","U.S. 7Y","U.S. 5Y","U.S. 3Y","U.S. 2Y"]
			commodities=['Gold','Silver','Copper','Palladium','Platinum','Xetra-Gold','US Cocoa','London Wheat','Lead']
			funds=['Icici Prudential Life - Balancer Fund','Hdfc Standard Life - Balanced Managed Investment Pension','The Hartford Midcap Fund Class C','Goldman Sachs Growth Opportunities Fund Institutional Class','Neuberger Berman Mid Cap Growth Fund Investor Class']
			futures=['BAJAJ-AUTO','ASIANPAINT','EICHERMOT']
			indices=['BSE Healthcare','BSE Teck','BSE IT','BNY Mellon India ADR TR','NQ US Mid Cap Value','DJ Internet','DJ Insurance Brokers']
			assname=request.POST['assname1']
			if(assname in stocks):
				v123="stocks"
				n=assname
				DataFrame3=yf.download(n,request.POST['sdate'],request.POST['edate'])
				DataFrame3=DataFrame3.to_html()
			elif(assname in funds):
				v123="funds"
				n=assname
				a11=request.POST['sdate']
				import datetime
				darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				a11=request.POST['edate']
				edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)

				if(n in indianfunds):
					DataFrame3=investpy.get_fund_historical_data(fund=n, country='india',from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
					
				else:
					DataFrame3=investpy.get_fund_historical_data(fund=n, country='united states',from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
				DataFrame3=DataFrame3.to_html()
			elif(assname in bonds):
				v123="bonds"
				n=assname
				a11=request.POST['sdate']
				import datetime
				darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				a11=request.POST['edate']
				edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)

				if(n in indianbonds):
					DataFrame3=investpy.get_bond_historical_data(bond=n,from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
					
				else:
					DataFrame3=investpy.get_bond_historical_data(bond=n,from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
				DataFrame3=DataFrame3.to_html()
			elif(assname in indices):
				v123="indices"
				n=assname
				a11=request.POST['sdate']
				import datetime
				darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				a11=request.POST['edate']
				edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)

				if(n in indianindices):
					DataFrame3=investpy.indices.get_index_historical_data(index=n, country='india', from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, as_json=False, order='descending', interval='Daily')
					
				else:
					DataFrame3=investpy.indices.get_index_historical_data(index=n, country='united states', from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, as_json=False, order='descending', interval='Daily')
				DataFrame3=DataFrame3.to_html()
			elif(assname in commodities):
				v123="commodities"
				n=assname
				a11=request.POST['sdate']
				import datetime
				darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				a11=request.POST['edate']
				edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				DataFrame3=investpy.commodities.get_commodity_historical_data(commodity=n, from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, country='united states', as_json=False, order='descending', interval='Daily')
				DataFrame3=DataFrame3.to_html()

			elif(assname in futures):
				v123="futures(INR)"
				from datetime import datetime
				n=assname
				a1=request.POST['sdate']
				usethis1 = datetime.strptime(a1, '%Y-%m-%d')
				a2=request.POST['edate']
				usethis2 = datetime.strptime(a2, '%Y-%m-%d')
				expire=get_expiry_date(usethis2.year,usethis2.month)
				exp=list(expire)
				maxi=0
				in1=-1
				ct=0
				for i in exp:
				    if(i.day>maxi):
				        maxi=i.day
				        in1=ct
				    ct=ct+1
				expire_date=exp[in1]
				DataFrame3=get_history(symbol=n,start=usethis1,end=usethis2,futures=True,expiry_date=expire_date)
				DataFrame3=DataFrame3.to_html()

		elif('assname') in request.POST:
			stocks=['NFLX','FB','AAPL','MSFT']
			bonds=['India 10Y',"India 30Y","India 24Y","India 15Y","U.S. 10Y","U.S. 7Y","U.S. 5Y","U.S. 3Y","U.S. 2Y"]
			commodities=['Gold','Silver','Copper','Palladium','Platinum','Xetra-Gold','US Cocoa','London Wheat','Lead']
			funds=['Icici Prudential Life - Balancer Fund','Hdfc Standard Life - Balanced Managed Investment Pension','The Hartford Midcap Fund Class C','Goldman Sachs Growth Opportunities Fund Institutional Class','Neuberger Berman Mid Cap Growth Fund Investor Class']
			futures=['BAJAJ-AUTO','ASIANPAINT','EICHERMOT']
			indices=['BSE Healthcare','BSE Teck','BSE IT','BNY Mellon India ADR TR','NQ US Mid Cap Value','DJ Internet','DJ Insurance Brokers']
			assname=request.POST['assname']
			if(assname in stocks):
				v123="stocks"
				n=assname
				DataFrame = yf.download(n,request.POST['sdate'],request.POST['edate'])
				close=DataFrame['Close'].tolist()
				import datetime
				s=n
				sdate=datetime.datetime.strptime(request.POST['sdate'], "%Y-%m-%d").date()
				edate=datetime.datetime.strptime(request.POST['edate'], "%Y-%m-%d").date()
				delta = edate - sdate
				for i in range(delta.days + 1):
					day = sdate + timedelta(days=i)
					no.append(str(day))
				diff=len(no)-len(close)
				for i in range(1,diff+1):
					no.remove(no[i])
			elif(assname in funds):
				v123="funds"
				s=assname
				a11=request.POST['sdate']
				import datetime
				darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				a11=request.POST['edate']
				edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				if(s in indianfunds):
					DataFrame=investpy.get_fund_historical_data(fund=s, country='india',from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
					
				else:
					DataFrame=investpy.get_fund_historical_data(fund=s, country='united states',from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
				#DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
				close=DataFrame['Close'].tolist()
				s=str(s)
				sdate2=date(int(darevy), int(darevm), int(darevd))
				edate2=date(int(edarevy), int(edarevm), int(edarevd)) 
				delta2 = edate2 - sdate2 
				for i in range(delta2.days + 1):
					day = sdate2 + timedelta(days=i)
					no.append(str(day))
				diff=len(no)-len(close)
				for i in range(1,diff+1):
					no.remove(no[i])
			elif(assname in bonds):
				v123="bonds"
				s=assname
				a11=request.POST['sdate']
				import datetime
				darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				a11=request.POST['edate']
				edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				DataFrame=investpy.get_bond_historical_data(bond=s,from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy)
				#DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
				close=DataFrame['Close'].tolist()
				s=str(s)
				sdate2=date(int(darevy), int(darevm), int(darevd))
				edate2=date(int(edarevy), int(edarevm), int(edarevd)) 
				delta2 = edate2 - sdate2 
				for i in range(delta2.days + 1):
					day = sdate2 + timedelta(days=i)
					no.append(str(day))
				diff=len(no)-len(close)
				for i in range(1,diff+1):
					no.remove(no[i])
			elif(assname in indices):
				v123="indices"
				s=assname
				a11=request.POST['sdate']
				import datetime
				darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				a11=request.POST['edate']
				edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				if(s in indianindices):
					DataFrame=investpy.indices.get_index_historical_data(index=s, country='india', from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, as_json=False, order='descending', interval='Daily')
					
				else:
					DataFrame=investpy.indices.get_index_historical_data(index=s, country='united states', from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, as_json=False, order='descending', interval='Daily')
					
				#DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
				close=DataFrame['Close'].tolist()
				s=str(s)
				sdate2=date(int(darevy), int(darevm), int(darevd))
				edate2=date(int(edarevy), int(edarevm), int(edarevd)) 
				delta2 = edate2 - sdate2 
				for i in range(delta2.days + 1):
					day = sdate2 + timedelta(days=i)
					no.append(str(day))
				diff=len(no)-len(close)
				for i in range(1,diff+1):
					no.remove(no[i])
			elif(assname in commodities):
				v123="commodities"
				s=assname
				a11=request.POST['sdate']
				import datetime
				darevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				darevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				darevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				a11=request.POST['edate']
				edarevy=str(datetime.datetime.strptime(a11, "%Y-%m-%d").year)
				edarevd=str(datetime.datetime.strptime(a11, "%Y-%m-%d").day)
				edarevm=str(datetime.datetime.strptime(a11, "%Y-%m-%d").month)
				DataFrame=investpy.commodities.get_commodity_historical_data(commodity=s, from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, country='united states', as_json=False, order='descending', interval='Daily')
				#DataFrame = yf.download(request.POST['s'],request.POST['sdate'],request.POST['edate'])
				close=DataFrame['Close'].tolist()
				s=str(s)
				sdate2=date(int(darevy), int(darevm), int(darevd))
				edate2=date(int(edarevy), int(edarevm), int(edarevd)) 
				delta2 = edate2 - sdate2 
				for i in range(delta2.days + 1):
					day = sdate2 + timedelta(days=i)
					no.append(str(day))
				diff=len(no)-len(close)
				for i in range(1,diff+1):
					no.remove(no[i])

			elif(assname in futures):
				v123="futures"
				from datetime import datetime
				s=assname
				a1=request.POST['sdate']
				usethis1 = datetime.strptime(a1, '%Y-%m-%d').date()
				a2=request.POST['edate']
				usethis2 = datetime.strptime(a2, '%Y-%m-%d').date()
				expire=get_expiry_date(usethis2.year,usethis2.month)
				exp=list(expire)
				maxi=0
				in1=-1
				ct=0
				for i in exp:
				    if(i.day>maxi):
				        maxi=i.day
				        in1=ct
				    ct=ct+1
				expire_date=exp[in1]
				DataFrame=get_history(symbol=s,start=usethis1,end=usethis2,futures=True,expiry_date=expire_date)
				close=DataFrame['Close'].tolist()
				s=str(s)
				sdate2=usethis1
				edate2=usethis2
				delta2 = edate2 - sdate2 
				for i in range(delta2.days + 1):
					day = sdate2 + timedelta(days=i)
					no.append(str(day))
				diff=len(no)-len(close)
				for i in range(1,diff+1):
					no.remove(no[i])


		elif('futurename' in request.POST):
			from datetime import datetime
			n1=request.POST['futurename']
			tday = date.today()
			yesterday = tday - timedelta(days=1)
			st=get_history(symbol=request.POST['futurename'],start=yesterday,end=tday)
			cl=len(list(st['Close']))
			i=1;
			if(cl==0):
				while(cl==0):
					tday=date.today()-timedelta(days=i)
					yesterday=tday-timedelta(days=1)
					st=get_history(symbol=request.POST['futurename'],start=yesterday,end=tday)
					tp=list(st['Close'])
					i=i+1
					# price=tp[0]
					cl=len(list(st['Close']))
					if(cl!=0):
						break
			else:
				tp=list(st['Close'])

			price1=tp[0]
			c = CurrencyRates()
			inrtousd=c.get_rate('INR','USD')
			price1=price1*inrtousd
			price1=round(price1,2)
			n=request.POST['futurename']
			# Table Entry
			last_stock=investmentsinfutures.objects.filter(name = n1).values('id', 'price').last()

			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:#assigned price because profit or loss=0 if we are adding it to table first time(assumption)
				last_stock=price1

			if(price1!=0.0):
				if(amount>price1):
					amount=amount-price1
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price1-last_stock
					last_stock=round(last_stock,2)
					usethis2 = datetime.strptime(str(date.today()), '%Y-%m-%d')
					expire=get_expiry_date(usethis2.year,usethis2.month)
					exp=list(expire)
					in1=random.randrange(1,len(exp), 1)
					expire_date=exp[in1]
					a = investmentsinfutures(name=n.upper(),price=price1,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock,expiry_date=expire_date)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			a21=investments.objects.aggregate(t=Sum('price'))['t']
			a22=investmentsincommodities.objects.aggregate(t=Sum('price'))['t']
			a23=investmentsinfunds.objects.aggregate(t=Sum('price'))['t']
			a24=investmentsinbonds.objects.aggregate(t=Sum('price'))['t']
			a25=investmentsinfutures.objects.aggregate(t=Sum('price'))['t']
			a26=investmentsinindices.objects.aggregate(t=Sum('price'))['t']
			datapinall=[a21,a22,a23,a24,a25,a26]
			labelsinall=['Stock','Commodities','Funds','Bonds','Futures','Indices']

		elif('stockname' in request.POST):
			n2=request.POST['stockname']
			api_key = 'BJQZ9I2H012Q7FDD'
			#code for profit loss returns none if no query found so used if condition
			last_stock=investments.objects.filter(name = n2).values('id', 'price').last()
			ts = TimeSeries(key=api_key, output_format='json')
			data, meta_data = ts.get_quote_endpoint(n2)
			#get price  real-time
			price2=float(data['05. price'])
			price2=round(price2, 2)
			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:#assigned price because profit or loss=0 if we are adding it to table first time(assumption)
				last_stock=price2

			if(price2!=0.0):
				if(amount>price2):
					amount=amount-price2
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price2-last_stock
					last_stock=round(last_stock,2)
					a = investments(name=n2.upper(),price=price2,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			a21=investments.objects.aggregate(t=Sum('price'))['t']
			a22=investmentsincommodities.objects.aggregate(t=Sum('price'))['t']
			a23=investmentsinfunds.objects.aggregate(t=Sum('price'))['t']
			a24=investmentsinbonds.objects.aggregate(t=Sum('price'))['t']
			a25=investmentsinfutures.objects.aggregate(t=Sum('price'))['t']
			a26=investmentsinindices.objects.aggregate(t=Sum('price'))['t']
			datapinall=[a21,a22,a23,a24,a25,a26]
			labelsinall=['Stock','Commodities','Funds','Bonds','Futures','Indices']
		elif('fundname' in request.POST) :
			n3=request.POST['fundname']
			indianfunds=['Icici Prudential Life - Balancer Fund','Hdfc Standard Life - Balanced Managed Investment Pension']
			#api_key = 'BJQZ9I2H012Q7FDD'
			#code for profit loss returns none if no query found so used if condition
			last_stock=investmentsinfunds.objects.filter(name = n3).values('id', 'price').last()
			#ts = TimeSeries(key=api_key, output_format='json')
			#data, meta_data = ts.get_quote_endpoint(n)
			#get price  real-time
			if(n3 in indianfunds):
				v1=investpy.funds.get_fund_recent_data(fund=n3, country='india', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close']
				v1=float(v1)
				c = CurrencyRates()
				inrtousd=c.get_rate('INR','USD')
				v1=v1*inrtousd
				price3=round(v1,2)
			else:
				v1=float(investpy.funds.get_fund_recent_data(fund=n3, country='united states', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close'])
				price3=round(v1,2)
			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:#assigned price because profit or loss=0 if we are adding it to table first time(assumption)
				last_stock=price3

			if(price3!=0.0):
				if(amount>price3):
					amount=amount-price3
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price3-last_stock
					last_stock=round(last_stock,2)
					a = investmentsinfunds(name=n3.upper(),price=price3,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			a21=investments.objects.aggregate(t=Sum('price'))['t']
			a22=investmentsincommodities.objects.aggregate(t=Sum('price'))['t']
			a23=investmentsinfunds.objects.aggregate(t=Sum('price'))['t']
			a24=investmentsinbonds.objects.aggregate(t=Sum('price'))['t']
			a25=investmentsinfutures.objects.aggregate(t=Sum('price'))['t']
			a26=investmentsinindices.objects.aggregate(t=Sum('price'))['t']
			datapinall=[a21,a22,a23,a24,a25,a26]
			labelsinall=['Stock','Commodities','Funds','Bonds','Futures','Indices']

		elif('indicesname' in request.POST):
			n4=request.POST['indicesname']
			indianfunds=['BSE Healthcare','BSE Teck','BNY Mellon India ADR TR','BSE IT']

				#api_key = 'BJQZ9I2H012Q7FDD'
				#code for profit loss returns none if no query found so used if condition
			last_stock=investmentsinindices.objects.filter(name = n4).values('id', 'price').last()
				#ts = TimeSeries(key=api_key, output_format='json')
				#data, meta_data = ts.get_quote_endpoint(n)
				#get price  real-time
			if(n4 in indianfunds):
					#v1=investpy.funds.get_fund_recent_data(fund=n, country='india', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close']
				v1=float(investpy.indices.get_index_information(index=n4, country='india', as_json=False)['Prev. Close'])
				c = CurrencyRates()
				inrtousd=c.get_rate('INR','USD')
				v1=v1*inrtousd
				price4=round(v1,2)
			else:
					#v1=float(investpy.funds.get_fund_recent_data(fund=n, country='united states', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close'])
				v1=float(investpy.indices.get_index_information(index=n4, country='united states', as_json=False)['Prev. Close'])
				price4=round(v1,2)
			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:#assigned price because profit or loss=0 if we are adding it to table first time(assumption)
				last_stock=price4

			if(price4!=0.0):
				if(amount>price4):
					amount=amount-price4
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price4-last_stock
					last_stock=round(last_stock,2)
					a = investmentsinindices(name=n4.upper(),price=price4,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			a21=investments.objects.aggregate(t=Sum('price'))['t']
			a22=investmentsincommodities.objects.aggregate(t=Sum('price'))['t']
			a23=investmentsinfunds.objects.aggregate(t=Sum('price'))['t']
			a24=investmentsinbonds.objects.aggregate(t=Sum('price'))['t']
			a25=investmentsinfutures.objects.aggregate(t=Sum('price'))['t']
			a26=investmentsinindices.objects.aggregate(t=Sum('price'))['t']
			datapinall=[a21,a22,a23,a24,a25,a26]
			labelsinall=['Stock','Commodities','Funds','Bonds','Futures','Indices']

		elif('bondsname' in request.POST):
			n5=request.POST['bondsname']
			indianfunds=['India 10Y','India 30Y','India 24Y','India 15Y']

			#api_key = 'BJQZ9I2H012Q7FDD'
			#code for profit loss returns none if no query found so used if condition
			last_stock=investmentsinbonds.objects.filter(name = n5).values('id', 'price').last()
			#ts = TimeSeries(key=api_key, output_format='json')
			#data, meta_data = ts.get_quote_endpoint(n)
			#get price  real-time
			if(n5 in indianfunds):
				v1=investpy.bonds.get_bond_recent_data(bond=n5, as_json=False, order='descending', interval='Daily').iloc[0,:]['Close']
				v1=float(v1)
				c = CurrencyRates()
				inrtousd=c.get_rate('INR','USD')
				v1=v1*inrtousd
				price5=round(v1,2)
			else:
				v1=float(investpy.bonds.get_bond_recent_data(bond=n5, as_json=False, order='descending', interval='Daily').iloc[0,:]['Close'])
				price5=round(v1,2)
			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:#assigned price because profit or loss=0 if we are adding it to table first time(assumption)
				last_stock=price5

			if(price5!=0.0):
				if(amount>price5):
					amount=amount-price5
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price5-last_stock
					last_stock=round(last_stock,2)
					a = investmentsinbonds(name=n5.upper(),price=price5,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			a21=investments.objects.aggregate(t=Sum('price'))['t']
			a22=investmentsincommodities.objects.aggregate(t=Sum('price'))['t']
			a23=investmentsinfunds.objects.aggregate(t=Sum('price'))['t']
			a24=investmentsinbonds.objects.aggregate(t=Sum('price'))['t']
			a25=investmentsinfutures.objects.aggregate(t=Sum('price'))['t']
			a26=investmentsinindices.objects.aggregate(t=Sum('price'))['t']
			datapinall=[a21,a22,a23,a24,a25,a26]
			labelsinall=['Stock','Commodities','Funds','Bonds','Futures','Indices']
		elif('commodityname' in request.POST):
			n6=request.POST['commodityname']
			last_stock=investmentsincommodities.objects.filter(name = n6).values('id', 'price').last()
			v1=float(investpy.get_commodity_recent_data(commodity=n6)['Close'][0])
			price6=round(v1,2)
			if(last_stock!=None):
				last_stock=float(last_stock['price'])
				last_stock=round(last_stock,2)
			else:
				last_stock=price6

			if(price6!=0.0):
				if(amount>price6):
					amount=amount-price6
					amount=round(amount, 2)
					m.mymoney=amount
					m.save()
					t = time.localtime()
					current_time = str(time.strftime("%H:%M:%S", t))
					last_stock=price6-last_stock
					last_stock=round(last_stock,2)
					a = investmentsincommodities(name=n6.upper(),price=price6,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)
			a21=investments.objects.aggregate(t=Sum('price'))['t']
			a22=investmentsincommodities.objects.aggregate(t=Sum('price'))['t']
			a23=investmentsinfunds.objects.aggregate(t=Sum('price'))['t']
			a24=investmentsinbonds.objects.aggregate(t=Sum('price'))['t']
			a25=investmentsinfutures.objects.aggregate(t=Sum('price'))['t']
			a26=investmentsinindices.objects.aggregate(t=Sum('price'))['t']
			datapinall=[a21,a22,a23,a24,a25,a26]
			labelsinall=['Stock','Commodities','Funds','Bonds','Futures','Indices']
    #1st
	d=dict()
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset = investmentsincommodities.objects.order_by('name')
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
	#2nd
	d1=dict()
	labels1=[]
	datap1=[]
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset1 = investments.objects.order_by('name')
	for stock in queryset1:
		labels1.append(stock.name)
		datap1.append(stock.price)
	for i in range(len(labels1)):
		if(labels1[i] in d1.keys()):
			d1[labels1[i]]+=datap1[i]
		else:
			d1[labels1[i]]=datap1[i]
	labels1=list(d1.keys())
	datap1=list(d1.values())
	#3rd
	d2=dict()
	labels2=[]
	datap2=[]
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset2 = investmentsinbonds.objects.order_by('name')
	for stock in queryset2:
		labels2.append(stock.name)
		datap2.append(stock.price)
	for i in range(len(labels2)):
		if(labels2[i] in d2.keys()):
			d2[labels2[i]]+=datap2[i]
		else:
			d2[labels2[i]]=datap2[i]
	labels2=list(d2.keys())
	datap2=list(d2.values())
	#4th
	d3=dict()
	labels3=[]
	datap3=[]
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset3 = investmentsinfunds.objects.order_by('name')
	for stock in queryset3:
		labels3.append(stock.name)
		datap3.append(stock.price)
	for i in range(len(labels3)):
		if(labels3[i] in d3.keys()):
			d3[labels3[i]]+=datap3[i]
		else:
			d3[labels3[i]]=datap3[i]
	labels3=list(d3.keys())
	datap3=list(d3.values())
	#5th
	d4=dict()
	labels4=[]
	datap4=[]
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset4 = investmentsinindices.objects.order_by('name')
	for stock in queryset4:
		labels4.append(stock.name)
		datap4.append(stock.price)
	for i in range(len(labels4)):
		if(labels4[i] in d4.keys()):
			d4[labels4[i]]+=datap4[i]
		else:
			d4[labels4[i]]=datap4[i]
	labels4=list(d4.keys())
	datap4=list(d4.values())
	#6th
	d5=dict()
	labels5=[]
	datap5=[]
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset5 = investmentsinfutures.objects.order_by('name')
	for stock in queryset5:
		labels5.append(stock.name)
		datap5.append(stock.price)
	for i in range(len(labels5)):
		if(labels5[i] in d5.keys()):
			d5[labels5[i]]+=datap5[i]
		else:
			d5[labels5[i]]=datap5[i]
	labels5=list(d5.keys())
	datap5=list(d5.values())
	#returning all the calculates values to html
	return render(request, 'portfolio/dash.html',{'price1':price1,'price2':price2,'price3':price3,'price4':price4,'price5':price5,'price6':price6,'n1':n1,'n3':n3,'n2':n2,'n4':n4,'n5':n5,'n6':n6,'v123':v123,'ass1':ass1,'no11':no11,'no22':no22,'close11':close11,'close22':close22,'labelsinall':labelsinall,'datapinall':datapinall,'n':n,'labels':labels,'datap':datap,'labels1':labels1,'datap1':datap1,'labels2':labels2,'datap2':datap2,'labels3':labels3,'datap3':datap3,'labels4':labels4,'datap4':datap4,'labels5':labels5,'datap5':datap5,'price':price,'amount':amount,'query_results1':query_results1,'query_results2':query_results2,'query_results3':query_results3,'query_results4':query_results4,'query_results5':query_results5,'query_results6':query_results6,'rem':rem,'close':close,'no':no,'s':s,'close1':close1,'close2':close2,'no1':no1,'no2':no2,'DataFrame3':DataFrame3})
def sales(request):
	return render(request,'portfolio/sales.html')
def index(request):
	#intialize variables that we are going to pass
	price=0.0
	m=money.objects.get(pk=1)
	amount=m.mymoney
	amount=round(amount, 2)
	rem=1000000-amount
	rem=round(rem, 2)
	close=[]
	no=[]
	s=""
	labels = []
	datap = []
	n="Stock"
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
			close=DataFrame['Close'].tolist()
			import datetime
			s=request.POST['s']
			sdate=datetime.datetime.strptime(request.POST['sdate'], "%Y-%m-%d").date()
			edate=datetime.datetime.strptime(request.POST['edate'], "%Y-%m-%d").date()
			delta = edate - sdate
			for i in range(delta.days + 1):
				day = sdate + timedelta(days=i)
				no.append(str(day))
			diff=len(no)-len(close)
			for i in range(1,diff+1):
				no.remove(no[i])
						
		 
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
	return render(request, 'portfolio/index.html',{'n':n,'labels':labels,'datap':datap,'price':price,'amount':amount,'query_results':query_results,'rem':rem,'close':close,'no':no,'s':s,'DataFrame3':DataFrame3})

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

def indices(request):
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
	n="Indices name"
	for i in range(len(close)):
				no.append(i+1)
	for i in range(len(close1)):
		no1.append(i+1)
	for i in range(len(close2)):
		no2.append(i+1)

	s=""
	labels = []
	datap = []
	DataFrame3="Table for Particular Indices"
	indianfunds=['BSE Healthcare','BSE Teck','BNY Mellon India ADR TR','BSE IT']
	#fetch recent 10 investments
	query_results= investmentsinindices.objects.all().order_by('-id')[:10]
	last_stock=0
	v1=0
	if request.method == 'POST' :
		#for buy stock,available assets,investments and pushing purcahses into investment table
		if('stockname' in request.POST) :
			n=request.POST['stockname']
			#api_key = 'BJQZ9I2H012Q7FDD'
			#code for profit loss returns none if no query found so used if condition
			last_stock=investmentsinindices.objects.filter(name = n).values('id', 'price').last()
			#ts = TimeSeries(key=api_key, output_format='json')
			#data, meta_data = ts.get_quote_endpoint(n)
			#get price  real-time 
			if(n in indianfunds):
				#v1=investpy.funds.get_fund_recent_data(fund=n, country='india', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close']
				v1=float(investpy.indices.get_index_information(index=n, country='india', as_json=False)['Prev. Close'])
				c = CurrencyRates()
				inrtousd=c.get_rate('INR','USD') 
				v1=v1*inrtousd
				price=round(v1,2)
			else:
				#v1=float(investpy.funds.get_fund_recent_data(fund=n, country='united states', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close'])
				v1=float(investpy.indices.get_index_information(index=n, country='united states', as_json=False)['Prev. Close'])
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
					a = investmentsinindices(name=n.upper(),price=price,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
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
				DataFrame3=investpy.indices.get_index_historical_data(index=request.POST['sn'], country='india', from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, as_json=False, order='descending', interval='Daily')
				
			else:
				DataFrame3=investpy.indices.get_index_historical_data(index=request.POST['sn'], country='united states', from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, as_json=False, order='descending', interval='Daily')
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
				DataFrame=investpy.indices.get_index_historical_data(index=request.POST['s'], country='india', from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, as_json=False, order='descending', interval='Daily')
				
			else:
				DataFrame=investpy.indices.get_index_historical_data(index=request.POST['s'], country='united states', from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, as_json=False, order='descending', interval='Daily')
				
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
	queryset = investmentsinindices.objects.order_by('name')
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
	return render(request, 'portfolio/indices.html',{'n':n,'labels':labels,'datap':datap,'price':price,'amount':amount,'query_results':query_results,'rem':rem,'close':close,'no':no,'s':s,'close1':close1,'close2':close2,'no1':no1,'no2':no2,'DataFrame3':DataFrame3})

def commodities(request):
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
	n="commodities name"
	for i in range(len(close)):
				no.append(i+1)
	for i in range(len(close1)):
		no1.append(i+1)
	for i in range(len(close2)):
		no2.append(i+1)

	s=""
	labels = []
	datap = []
	DataFrame3="Table for Particular commodities"
	#fetch recent 10 investments
	query_results= investmentsincommodities.objects.all().order_by('-id')[:10]
	last_stock=0
	v1=0
	if request.method == 'POST' :
		#for buy stock,available assets,investments and pushing purcahses into investment table
		if('stockname' in request.POST) :
			n=request.POST['stockname']
			#api_key = 'BJQZ9I2H012Q7FDD'
			#code for profit loss returns none if no query found so used if condition
			last_stock=investmentsincommodities.objects.filter(name = n).values('id', 'price').last()
			#ts = TimeSeries(key=api_key, output_format='json')
			#data, meta_data = ts.get_quote_endpoint(n)
			#get price  real-time 
			
				#v1=float(investpy.funds.get_fund_recent_data(fund=n, country='united states', as_json=False, order='descending', interval='Daily').iloc[0,:]['Close'])
			v1=float(investpy.get_commodity_recent_data(commodity=n)['Close'][0])
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
					a = investmentsincommodities(name=n.upper(),price=price,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock)
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
			DataFrame3=investpy.commodities.get_commodity_historical_data(commodity=request.POST['sn'], from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, country='united states', as_json=False, order='descending', interval='Daily')
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
			DataFrame=investpy.commodities.get_commodity_historical_data(commodity=request.POST['s'], from_date=darevd+'/'+darevm+'/'+darevy, to_date=edarevd+'/'+edarevm+'/'+edarevy, country='united states', as_json=False, order='descending', interval='Daily')
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
	queryset = investmentsincommodities.objects.order_by('name')
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
	return render(request, 'portfolio/commodities.html',{'n':n,'labels':labels,'datap':datap,'price':price,'amount':amount,'query_results':query_results,'rem':rem,'close':close,'no':no,'s':s,'close1':close1,'close2':close2,'no1':no1,'no2':no2,'DataFrame3':DataFrame3})


def futures(request):
	stock_fut="Table for Futures"
	stock_fut2="Table for Grap"
	enter_name=""
	gname=""
	labels=[]
	datap=[]
	no=[]
	fprice=[]
	price=0.0
	m=money.objects.get(pk=1)
	amount=m.mymoney
	amount=round(amount, 2)
	rem=1000000-amount
	rem=round(rem, 2)
	last_stock=0;
	query_results= investmentsinfutures.objects.all().order_by('-id')[:10]
	if request.method == 'POST':
		if('stockname' in request.POST):
			tday = date.today()
			yesterday = tday - timedelta(days=1)
			st=get_history(symbol=request.POST['stockname'],start=yesterday,end=tday)
			cl=len(list(st['Close']))
			if(cl==0):
				while(cl==0):
					tday=date.today()-timedelta(days=1)
					yesterday=tday-timedelta(days=1)
					st=get_history(symbol=request.POST['stockname'],start=yesterday,end=tday)
					tp=list(st['Close'])
					# price=tp[0]
					cl=len(list(st['Close']))
					if(cl!=0):
						break
			else:
				tp=list(st['Close'])

			price=tp[0]
			# tday = date.today()
			# yesterday = tday - timedelta(days=1)
			# d1=yesterday.date()
			# d2=tday.date()
			# st=get_history(symbol=request.POST['stockname'],start=d1,end=d2)
			# tp=list(st['Close'])
			# price=tp[0]
			c = CurrencyRates()
			inrtousd=c.get_rate('INR','USD')
			price=price*inrtousd
			price=round(price,2)
			enter_name=request.POST['stockname']
			# Table Entry
			last_stock=investmentsinfutures.objects.filter(name = enter_name).values('id', 'price').last()

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
					usethis2 = datetime.strptime(str(date.today()), '%Y-%m-%d')
					expire=get_expiry_date(usethis2.year,usethis2.month)
					exp=list(expire)
					in1=random.randrange(1,len(exp), 1)
					expire_date=exp[in1]
					a = investmentsinfutures(name=enter_name.upper(),price=price,date_created=str(date.today()),current_time=current_time,gain_loss=last_stock,expiry_date=expire_date)
					a.save()
					rem=1000000-amount
					rem=round(rem, 2)

		elif('na' in request.POST):
			a1=request.POST['sd']
			usethis1 = datetime.strptime(a1, '%Y-%m-%d')
			a2=request.POST['ed']
			usethis2 = datetime.strptime(a2, '%Y-%m-%d')
			expire=get_expiry_date(usethis2.year,usethis2.month)
			exp=list(expire)
			in1=random.randrange(1,len(exp), 1)
			expire_date=exp[in1]
			stock_fut=get_history(symbol=request.POST['na'],start=usethis1,end=usethis2,futures=True,expiry_date=expire_date)
			stock_fut=stock_fut.to_html()


	#for pie chart getting all investemnts summing up the stock by their labels
	queryset=investmentsinfutures.objects.order_by('name')
	d=dict()
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
	return render(request,'portfolio/futures.html',{'stock_fut':stock_fut,'price':price,'enter_name':enter_name,'labels':labels,'datap':datap,'query_results':query_results,'amount':amount,'rem':rem,'no':no,'fprice':fprice,'gname':gname})

def calendar(request):
	labels=[]
	datap=[]
	d=dict()
	#for pie chart getting all investemnts summing up the stock by their labels
	queryset = investmentsinfutures.objects.order_by('name')
	for stock in queryset:
		labels.append(stock.name)
		datap.append(stock.expiry_date)
	con=([{'date':datap[0],'calendar':'work','eventName':labels[0],'color':'orange'},{'date':datap[1],'calendar':'work','eventName':labels[1],'color':'orange'}]);
	# expiry = get_expiry_date(year=2015, month=1)
	# stock_opt = get_history(symbol="SBIN", start=date(2015,1,1), end=date(2015,1,10), futures=True, expiry_date=get_expiry_date(2015,1))
	return render(request, 'portfolio/calendar.html', {'labels':labels,'datap':datap,'con':con})

