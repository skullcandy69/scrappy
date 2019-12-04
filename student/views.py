from builtins import int

from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Input
from .forms import InputForm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import time
import csv
# Create your views here.

def home(request):
    return render(request,'student/front.html',)
def add(request):
    form = InputForm(request.POST)
    if form.is_valid():
        input_item = form.save(commit=False)
        input_item.save()
        return redirect('/student/function')
        #return redirect('/student/func/')
    else:
        form = InputForm()
    return render(request,'student/student_form.html', {'form': form})

def func(request):
    return render(request, 'student/disp.html', )


def function(request):
    import sqlite3

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    source = "select source from student_input order by id desc limit 0,1;"
    cursor.execute(source)
    s = cursor.fetchall()
    src1="".join(s[0])
    src=[src1]
    dest = "select destination from student_input order by id desc limit 0,1;"
    cursor.execute(dest)
    d = cursor.fetchall()
    des1 = "".join(d[0])
    des = [des1]

    dat = "select date from student_input order by id desc limit 0,1;"
    cursor.execute(dat)
    dt = cursor.fetchall()
    dt1 = "".join(dt[0])
    dt2=[dt1]


    f = open('data.csv', 'w')


    # browser = webdriver.Chrome(executable_path='C:\\Users\\Meet\\Desktop\\chromedriver.exe')
    # browser.implicitly_wait(10)
    df = pd.DataFrame()

    def dep_country_chooser(dep_country):
        fly_from = browser.find_element_by_xpath("//input[@id='departure-airport-1']")
        time.sleep(1)
        fly_from.clear()
        time.sleep(1.5)
        fly_from.send_keys('  ' + dep_country)
        time.sleep(1.5)
        first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
        time.sleep(1.5)
        first_item.click()

    def arrival_country_chooser(arrival_country):
        fly_to = browser.find_element_by_xpath("//input[@id='arrival-airport-1']")
        time.sleep(1)
        fly_to.clear()
        time.sleep(1.5)
        fly_to.send_keys('  ' + arrival_country)
        time.sleep(1.5)
        first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
        time.sleep(1.5)
        first_item.click()

    def dep_date_chooser(date):

        dep_date_button = browser.find_element_by_xpath("//input[@id='departure-date-1']")
        dep_date_button.clear()
        dep_date_button.send_keys(date)

    def search():
        search = browser.find_element_by_xpath("//button[@class='btn-secondary btn-sub-action']")
        search.click()
        time.sleep(15)
        print('Results ready!')

    def compile_data():
        global df
        global dep_times_list
        global arr_times_list
        global airlines_list
        global price_list
        global durations_list
        global stops_list
        global layovers_list

        # departure times
        dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
        dep_times_list = [value.text for value in dep_times]

        # arrival times
        arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
        arr_times_list = [value.text for value in arr_times]

        # airline name
        airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
        airlines_list = [value.text for value in airlines]

        # prices
        prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
        price_list = [value.text.split('Rs')[1] for value in prices]
        # a=pd.DataFrame(price_list)
        # print(a)

        # durations
        durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
        durations_list = [durations[i].text for i in range(0,14)]

        # stops
        stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
        stops_list = [value.text for value in stops]

        # layovers
        # layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
        # layovers_list = [value.text for value in layovers]

        # now = datetime.datetime.now()
        # current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
        # current_time = (str(now.hour) + ':' + str(now.minute))
        # current_price = 'price' + '(' + current_date + '---' + current_time + ')'
        current_price = 'price'
        for i in range(len(dep_times_list)):
            # try:
            #     df.loc[i, 'departure_time'] = dep_times_list[i]
            # except Exception as e:
            #     pass
            # try:
            #     df.loc[i, 'arrival_time'] = arr_times_list[i]
            # except Exception as e:
            #     pass
            try:
                df.loc[i, 'airline'] = airlines_list[i]
            except Exception as e:
                pass
            try:
                df.loc[i, 'duration'] = durations_list[i]
            except Exception as e:
                pass
            try:
                df.loc[i, 'stops'] = stops_list[i]
            except Exception as e:
                pass
            # try:
            #     df.loc[i, 'layovers'] = layovers_list[i]
            # except Exception as e:
            #     pass
            try:
                df.loc[i, str(current_price)] = price_list[i]
            except Exception as e:
                pass

        print('Excel Sheet Created!')

    url = 'https://www.expedia.co.in/Flights-Search?flight-type=on&starDate=05%2F12%2F2019&mode=search&trip=oneway&leg1=from%3ADelhi%2C+India+%28DEL-Indira+Gandhi+Intl.%29%2Cto%3AMumbai%2C+India+%28BOM-Chhatrapati+Shivaji+Intl.%29%2Cdeparture%3A05%2F12%2F2019TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY'
    browser = webdriver.Chrome(executable_path='C:\\Users\\Meet\\Desktop\\chromedriver.exe')
    browser.implicitly_wait(10)
    browser.get(url)

    dep_country_chooser(src1)

    arrival_country_chooser(des1)

    dep_date_chooser(dt1)

    search()
    compile_data()
    cheapest_flight = price_list
    a=[]
    for i in range (0,15):
        a.append(src1)
    b=[]
    for i in range (0,15):
       b.append(des1)

    zipplist = zip(a,b,dep_times_list,arr_times_list,durations_list,stops_list,price_list,airlines_list)
    # m = []
    # m = results_agg['origin']
    # n = []
    # n = results_agg['destination']
    # o = []
    # o = results_agg['startdate']
    # p = []
    # p = results_agg['price(in ?)']
    zl = zip(src,des,dt2,price_list[0])

    return render(request, 'student/disp.html', {'zipplist': zipplist,'zl':zl})