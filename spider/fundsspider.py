from urllib import request
import requests
import json
import time
from fake_useragent import UserAgent
from queue import Queue
from threading import Thread,Lock
from urllib import parse
import csv
import re
from lxml import etree
import random
import csv

class FundsSpider(object):
    def __init__(self):
        self.list_url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2019-02-28&ed=2020-02-29&qdii=&tabSubtype=,,,,,&pi={}&pn=50&dx=1'
        self.per_fund_url = 'http://fund.eastmoney.com/{}.html'
        self.i = 1
        self.headers = {'User-Agent':UserAgent().random}
        self.field_name = ['fname','fnum','cumulative_nv','cnv_change_6m','unit_nv','unit_nv_change','pnv_change_1m','npv_thisy','class','risk','founded_date','scale','management','manager','fee','mmin_amount','rank_1y']

    def re_parse(self,url):
        headers = self.headers
        html = requests.get(url=url,headers=headers).text
        return html
    
    def xpath_parse(self,item):
        url = self.per_fund_url.format(item)
        req = request.Request(url=url,headers=self.headers)
        resp = request.urlopen(req)
        html = resp.read().decode()
        return html
    
    def get_funds_num(self,list_url):
        html = self.re_parse(list_url)
        regex = '"(.*?)"'
        pattern = re.compile(regex,re.S)
        funds_list = pattern.findall(html)
        funds_num_list = []
        for fund in funds_list:
            funds_num_list.append(fund.split(',')[0])
        # print(funds_num_list)
        return self.get_per_fund_detail(funds_num_list)

    def get_per_fund_detail(self,funds_num_list):
        per_page_detail_list = []
        for num in funds_num_list:
            html = self.xpath_parse(num)
            p = etree.HTML(html)
            item = {}
            try:
                item['fname'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[1]/div[1]/div/text()')[0].strip()
            except Exception:
                print('fname:',num)
                item['fname'] = ''
            try:
                item['fnum'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[1]/div[1]/div/span[2]/text()')[0].strip()
            except Exception:
                print('fnum:',num)
                item['fnum'] = ''
            try:
                item['cumulative_nv'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[1]/dl[3]/dd[3]/span[2]/text()')[0].strip()
            except Exception:
                print('cumulative_nv:',num)
                item['cumulative_nv'] = ''
            try:
                item['cnv_change_6m'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[1]/dl[3]/dd[2]/span[2]/text()')[0].strip()
            except Exception:
                print('cnv_change_6m:',num)
                item['cnv_change_6m'] = ''
            try:
                item['unit_nv'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[1]/dl[2]/dd[1]/span[1]/text()')[0].strip()
            except Exception:
                print('unit_nv:',num)
                item['unit_nv'] = ''
            try:
                item['unit_nv_change'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[1]/dl[2]/dd[1]/span[2]/text()')[0].strip()
            except Exception:
                print('unit_nv_change:',num)
                item['unit_nv_change'] = ''
            try:
                item['pnv_change_1m'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[1]/dl[1]/dd[2]/span[2]/text()')[0].strip()
            except Exception:
                print('pnv_change_1m:',num)
                item['pnv_change_1m'] = ''
            try:
                item['npv_thisy'] = p.xpath('//*[@id="increaseAmount_stage"]/table/tr[2]/td[6]/div/text()')[0].strip()
            except Exception:
                print('npv_thisy:',num)
                item['npv_thisy'] = ''
            try:
                item['class'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[2]/table/tr[1]/td[1]/a/text()')[0].strip()
            except Exception:
                print('class:',num)
                item['class'] = ''
            try:
                item['risk'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[2]/table/tr[1]/td[1]/text()[2]')[0].split('|')[-1].strip()
            except Exception:
                print('risk:',num)
                item['risk'] = ''
            try:
                item['founded_date'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[2]/table/tr[2]/td[1]/text()')[0][1:].strip()
            except Exception:
                print('founded_date:',num)
                item['founded_date'] = ''
            try:
                item['scale'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[2]/table/tr[1]/td[2]/text()')[0][1:].strip()
            except Exception:
                print('scale:',num)
                item['scale'] = ''
            try:
                item['management'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[2]/table/tr[2]/td[2]/a/text()')[0].strip()
            except Exception:
                print('management:',num)
                item['management'] = ''
            try:
                item['manager'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[2]/table/tr[1]/td[3]/a/text()')[0].strip()
            except Exception:
                print('manager:',num)
                item['manager'] = ''
            try:
                item['fee'] = p.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[2]/div[2]/div[2]/div[5]/span[2]/span[2]/text()')[0].strip()
            except Exception:
                print('fee:',num)
                item['fee'] = ''
            try:
                item['mmin_amount'] = p.xpath('//*[@id="moneyAmountTxt"]/@data-placeholder')[0].strip()
            except Exception:
                print('mmin_amount:',num)
                item['mmin_amount'] = ''
            try:
                item['rank_1y'] = p.xpath('//*[@id="increaseAmount_stage"]/table/tr[6]/td[7]/div/text()')
                if item['rank_1y'] == ['  ']:
                    item['rank_1y'] = p.xpath('//*[@id="increaseAmount_stage"]/table/tr[5]/td[6]/div/text()')
                item['rank_1y'] = item['rank_1y'][0].strip()
            except Exception:
                print('rank_1y:',num)
                item['rank_1y'] = ''
        # print(item)
            per_page_detail_list.append(item)
            time.sleep(random.uniform(0,1))
        return self.write_fcsv(per_page_detail_list)

    def write_fcsv(self,per_page_detail_list):
        with open('funds_details.csv','a',encoding='utf-8',newline='') as f:
            writer = csv.DictWriter(f,fieldnames=self.field_name)
            for item in per_page_detail_list:
                writer.writerow(item)
        print('----------------------page finished----------------------')

    def run(self):
        with open('funds_details.csv','w',encoding='utf-8',newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.field_name)
            writer.writeheader()
        print('csv header has been writen')
        for page in range(0,21):
            pi = self.i + page
            print('----------------------start page:',pi,'----------------------')
            url = self.list_url.format(pi)
            self.get_funds_num(url)
            

if __name__ == '__main__':
    spider = FundsSpider()
    spider.run()