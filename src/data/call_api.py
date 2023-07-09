import requests
import xml.etree.ElementTree as ET
import pandas as pd
from util.tools import make_one_step

class GetData:
    def __init__(self, service_key):
        self.trade_url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'
        self.rent_url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent'
        self.service_key = service_key

    def load_trade_rent_data(self, trade_dir, rent_dir):
        trade = pd.read_csv(trade_dir)
        rent = pd.read_csv(rent_dir)
        return trade, rent

    def get_estate_price(self, LAWD_CD, DEAL_YMD, serviceKey, tp):
        if tp == 'trade':
            url = self.trade_url
        else:
            url = self.rent_url
        params = {
                'LAWD_CD':LAWD_CD,
                'DEAL_YMD':DEAL_YMD,
                'serviceKey':serviceKey
            }
        res = requests.get(url, params=params)
        return res

    def get_items(self, response):
        root = ET.fromstring(response.content)
        item_list = []
        for child in root.find('body').find('items'):
            elements = child.findall('*')
            data = {}
            for element in elements:
                tag = element.tag.strip()
                text = element.text.strip()
                data[tag] = text
            item_list.append(data)
        return item_list

    def get_all_data(self, end_yrm, region_code, tp):
        result = pd.DataFrame()
        yrm = 200601 # start date
        while yrm != end_yrm:
            print(f'Done {yrm} for {tp} data')
            res = self.get_estate_price(str(region_code), str(yrm), self.service_key, tp)
            items = pd.DataFrame(self.get_items(res))
            result = pd.concat([result, items])

            yrm = int(make_one_step(yrm))

        price_col = '거래금액' if tp == 'trade' else '보증금액'
        result[price_col] = result[price_col].map(lambda x: int(x.replace(',','')))
        result['yrm'] = result.apply(lambda x: x['년'] + x['월'].zfill(2), axis=1)
        return result

