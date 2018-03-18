#!/usr/bin/env python3.6
import sys
from bs4 import BeautifulSoup
import requests
import lxml
import json
import click
import math
# use --->>> pip install -r requirements.txt
stock_name=''
sector_name=''
stock_data = {}
financial_data = {}
project_url = "https://data.carouse41.hasura-app.io/"
headers = {"Content-Type":"Application/json", "Authorization": "Bearer b2c0b172a554ab92c3fc437e9aa3de1974218c2d95146844"}

def fetch_urls():
	urls = []
	url = "http://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html"
	page = requests.get(url).text
	soup = BeautifulSoup(page,"lxml")
	table = soup.find('table', class_="tbldata14")
	
	for tr in table.findAll('tr')[1:]:
		companyUrl = tr.find('a', class_='bl_12', href=True)['href']
		urls.append(companyUrl)
	
	for url in urls:
		extract_b1_p1_data(url)

def extract_b1_p1_data(companyUrl):
	global stock_name
	global sector_name
	url = "http://www.moneycontrol.com" + companyUrl
	page = requests.get(url).text
	soup = BeautifulSoup(page,"lxml")

	blsUrl = soup.find('a', text='Balance Sheet', href=True)['href']
	plUrl = soup.find('a', text='Profit & Loss', href=True)['href']

	stock_data = {}
	financial_data = {}

	base_div = soup.find('div',{"id":"nChrtPrc"})
	stock_name = base_div.find('h1').text
	print("============================================")
	print("Company: "+stock_name)
	sector_name = soup.findAll('a', class_='gD_10')[2].text
	print("Sector: "+sector_name)
	stock_data['stock_name'] = stock_name
	stock_data['sector_name'] = sector_name

	extract_b1_data(blsUrl)
	extract_p1_data(plUrl)
	insert_data()

def extract_b1_data(blsUrl):
	url = "http://www.moneycontrol.com" + blsUrl
	print("Extracting Balance Sheet from "+url)
	page = requests.get(url).text
	soup = BeautifulSoup(page,"lxml")

	base_div = soup.find('div', class_='boxBg1')
	table = base_div.findAll('table')[2]
	years = []
	trs = table.findAll('tr')[0]

	for td in trs.findAll('td')[1:]:
		years.append(int(td.text[-2:]) + 2000)
	get_td_value('Total Current Assets','total_net_current_assets', years, table)
	get_td_value('Total Non-Current Assets', 'net_block', years, table)
	print(" -------- Finished Extracting Balance Sheet data")

def get_td_value(name, column, years, table):
	try:
		all_data = table.find('td', text=name).find_next_siblings()
		index=0
		for year in years:
			current_data = all_data[index]
			if year in financial_data:
				financial_data[year][column] = float(current_data.text.replace(',',''))
			else:
				financial_data[year] = {"year": year}
				financial_data[year][column] = float(current_data.text.replace(',',''))
			index = index + 1
	except Exception as e:
		print("Error: %s" %str(e))

def extract_p1_data(plUrl):
	url = "http://www.moneycontrol.com" + plUrl
	print("Extracting Profit & Loss data from "+url)
	page = requests.get(url).text
	soup = BeautifulSoup(page,"lxml")

	base_div = soup.find('div', class_='boxBg1')
	table = base_div.findAll('table')[2]
	years = []
	trs = table.findAll('tr')[0]

	for td in trs.findAll('td')[1:]:
		years.append(int(td.text[-2:]) + 2000)
	get_td_value('Total Revenue','total_revenue', years, table)
	get_td_value('Profit/Loss Before Tax', 'profit_before_tax', years, table)
	get_td_value('Other Income','other_income', years, table)
	get_td_value('Total Tax Expenses','total_tax', years, table)
	print(" -------- Finished Extracting Profit & Loss data")

def insert_data():
	print("Calculating economic data")
	for year in financial_data:
		yearly_data = financial_data[year]
		pbt = yearly_data["profit_before_tax"]
		other_income = yearly_data["other_income"]
		adj_ebit = pbt - other_income

		total_tax = yearly_data["total_tax"]
		tax_rate = total_tax/pbt
		tax_on_other_income = tax_rate*other_income
		tax_on_adj_ebit = total_tax - tax_on_other_income

		noplat = adj_ebit - tax_on_adj_ebit

		coe = 0.12

		net_block = yearly_data["net_block"]
		total_net_current_assets = yearly_data["total_net_current_assets"]
		invested_capital = net_block + total_net_current_assets

		economic_profit = noplat - (coe*invested_capital)
		economic_profit = math.ceil((economic_profit*100)/100)
		total_revenue = yearly_data["total_revenue"]
		ep_ratio = economic_profit/total_revenue
		economic_profit = math.ceil((ep_ratio*10000)/10000)

		financial_data[year]["economic_profit"] = economic_profit
		financial_data[year]["ep_ratio"] = ep_ratio

	data_url = project_url + "/v1/query"

	stock_query = {"type":"insert",
		"args":{
			"table": "stocks",
			"objects": [{
				"stock_name" : stock_name, 
				"sector_name" : sector_name
			}]
			}
		}
	try:
		print("Inserting stock info")
		resp = requests.post(data_url, headers = headers, data = json.dumps(stock_query))
		# print("Response: " + str(resp.content))
	except Exception as e:
		print('Error %s' % str(e))

	for obj in financial_data:
		current_data = financial_data[obj]
		# print("Current data: "+str(current_data))
		financials_query = {"type":"insert",
			"args":{
				"table": "stock_financial_data",
				"objects": [current_data]
				}
			}
		try:
			resp = requests.post(data_url, headers = headers, data = json.dumps(financials_query))
			print("Response: " + str(resp.content))
		except Exception as e:
			print("Error: %s" % str(e))
	print(" +++++ Successfully inserted data +++++ ")

def delete_all():
	data_url = project_url + "/v1/query"
	query = {"args": {
			"table": "stocks",
			"where": {}
		},
		"type": "delete"
	}
	try:
		resp = requests.post(data_url, headers = headers, data = json.dumps(query))
		print("Response: " + str(resp.content))
	except Exception as e:
		print("Error: %s" %str(e))

	data_url = project_url + "/v1/query"
	query = {"args": {
			"table": "stock_financial_data",
			"where": {}
		},
		"type": "delete"
	}
	try:
		resp = requests.post(data_url, headers = headers, data = json.dumps(query))
		print("Response: " + str(resp.content))
	except Exception as e:
		print("Error: %s" %str(e))

delete_all()
fetch_urls()