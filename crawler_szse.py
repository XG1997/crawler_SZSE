# -*- coding: UTF-8 -*-
# author xiaogu
import requests,json,os,time,re


def read_l(txt):
    line_l = [line.strip() for line in open(txt, encoding='UTF-8').readlines()]
    return line_l


def downloadpdf(pdf_url, filename):
    pdf = requests.get(pdf_url)
    with open(filename, 'wb') as f:
        f.write(pdf.content)


def find_text(text,l):
    for i in l:
        if i in text:
            r = True
            break
        else:
            r = False
    return r


def rename(file_name,firm_id):
    global pattern,s_l
    year = re.findall(pattern,file_name)[0]
    for s in s_l:
        if s in file_name:
            season = str(s_l.index(s)+1)
            break
        else:
            pass
    new_name = f'{firm_id}_{year}_{season}.pdf'
    return new_name


pattern = '[0-9]{4}'
s_l = ['第一季度','半年度','第三季度','年年度']


# 公司代码输入，一个公司一行
txt = r'C:\Users\10546\Desktop\1.txt'
firm_ids = read_l(txt)
# 需要的时间段
date = ["2013-12-31", "2020-5-29"]
#pdf保存的位置
path = 'C:/Users/10546/Desktop/reports/'
# 标题中不包含的词
l = ['摘要','取消','正文']

#url
url = 'http://www.szse.cn/api/disc/announcement/annList?random=0.8015180112682705'
headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection':'keep-alive',
            'Content-Length':'92',
            'Content-Type':'application/json',
            'DNT':'1',
            'Host':'www.szse.cn',
            'Origin':'http://www.szse.cn',
            'Referer':'http://www.szse.cn/disclosure/listed/fixed/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'X-Request-Type':'ajax',
            'X-Requested-With':'XMLHttpRequest'}

#payload，获取源代码
for firm_id in firm_ids:
    dirname = path+f'{firm_id}'
    os.mkdir(dirname)
    for page in range(1,5):
        try:
            payload = {'seDate': date,
                       'stock': ["{firm_id}".format(firm_id=firm_id)],
                       'channelCode': ["fixed_disc"],
                       'pageSize': 30,
                       'pageNum': '{page}'.format(page=page)}
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            doc = response.json()
            if response.status_code==200:
                print('获取{0}的第{1}页源代码成功'.format(firm_id,page))
                #提取pdf_url和年报信息
                #count = doc.get('announceCount')
            datas = doc.get('data')
            #print(datas)
            for i in range(len(datas)):
                data = datas[i]
                pdf_url = 'http://disc.static.szse.cn/download'+data.get('attachPath')
                title = data.get('title')
                publish_time = data.get('publishTime')[:9]
                #filename = f'{firm_id}_{title}.pdf'
                filename = rename(title,firm_id)

                if find_text(title,l):
                    continue
                else:
                    downloadpdf(pdf_url, dirname+'/'+filename)
                    print(f'开始下载{filename}')
                    time.sleep(2)
        except:
            print('{0}的第{1}页不存在'.format(firm_id,page))
            pass

