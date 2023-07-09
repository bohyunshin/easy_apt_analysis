from data.call_api import GetData

if __name__ == '__main__':
    serviceKey_encoded = '%2BoAljLVOTD7bcsTkWNsO81np7%2BXxXoLi6vSBhAAkXHw073r3hcRSCLJUn2iUhYHm6sus6ty8xaD5%2BNHhgk4iiw%3D%3D'
    serviceKey_decoded = 'vzFxdH7xpXMB/rFZma+5owAjBkTdqCr+zQ40LMCvw+3IXQXshvwn7fOf1agVGjcztAo95ltWi0cMCNCAly6OTw=='
    gu_code = 30200 # 대전시 서구

    get_data = GetData(serviceKey_decoded)
    trade = get_data.get_all_data(202306, gu_code, 'trade')
    rent = get_data.get_all_data(202306, gu_code, 'rent')
    rent = rent[lambda x: x['월세금액'] == '0']

    trade.to_csv('../sample_data/trade_daejeon_yoosung.csv', index=False)
    rent.to_csv('../sample_data/rent_daejeon_yoosung.csv', index=False)
