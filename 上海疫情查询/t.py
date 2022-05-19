import requests
from lxml import etree
from prettytable import PrettyTable

url = "https://www.vigeotec.com/sh/query"

headers = {
    "Host": "www.vigeotec.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
    "Content-Length": "48",
    "Content-Type": "application/x-www-form-urlencoded"
}
while True:
    address = input("\n请输入小区名称，或者关键字，例如(浦城路366弄)：")
    print('\n查询中，请稍等片刻······')
    data = {
        "position": address
    }
    try:
        res = requests.post(url, headers=headers, data=data)
    except Exception as e:
        print("请检查您的网络是否正常！")
    else:

        html = etree.HTML(res.text)
        try:
            tr_list = html.xpath('//tbody/tr')[:-1]
            print()
        except Exception as e:
            print("暂无结果，该小区可能无新冠病例，或使用街道(小区)名称搜索")
        tb = PrettyTable()
        tb.field_names = ["序号", "区", "街道(小区)", "确诊时间", "推算类型", "推算解封时间"]
        tb.align["确诊时间"] = "l"
        tb.align["街道(小区)"] = "l"
        tb.title = "上海疫情查询"
        try:
            for i in tr_list:
                id = i.xpath('th/text()')[0].strip()
                area = i.xpath('td[1]/text()')[0].strip()
                community = i.xpath('td[2]/text()')[0].strip()
                diagnosis_time = i.xpath('td[3]/text()')[0].strip()
                risk_type = i.xpath('td[4]/text()')[0].strip()
                unblocking_time = i.xpath('td[5]/text()')[0].strip()
                tb.add_row([id, area, community, diagnosis_time, risk_type, unblocking_time])
        except Exception as e:
            # print("数据发生了变化，请联系开发者！")
            print("暂无结果，该小区可能无新冠病例，或使用街道(小区)名称搜索")
            # print(id, area, community, diagnosis_time, risk_type, unblocking_time)
        else:
            print(tb)
            print("预计解封日期根据+14天政策推算。(具体以当地居委或政府通知为准，本数据仅供参考)\n")
