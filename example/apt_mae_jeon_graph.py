import pandas as pd
from data.call_api import GetData
from preprocessing.preprocessor import Preprocessor
from plot.mae_jeon_plot import ApartmentPricePlotter

if __name__ == '__main__':
    serviceKey_encoded = '%2BoAljLVOTD7bcsTkWNsO81np7%2BXxXoLi6vSBhAAkXHw073r3hcRSCLJUn2iUhYHm6sus6ty8xaD5%2BNHhgk4iiw%3D%3D'
    serviceKey_decoded = 'vzFxdH7xpXMB/rFZma+5owAjBkTdqCr+zQ40LMCvw+3IXQXshvwn7fOf1agVGjcztAo95ltWi0cMCNCAly6OTw=='
    get_data = GetData(serviceKey_decoded)
    # 다운받은 데이터를 불러오는 경우
    trade_dir = '../sample_data/trade_daejeon_yoosung.csv'
    rent_dir = '../sample_data/rent_daejeon_yoosung.csv'
    trade, rent = get_data.load_trade_rent_data(trade_dir, rent_dir)
    apts = list(set(trade['아파트'].unique()) | set(rent['아파트'].unique()))
    areas = [59, 84]
    preproc = Preprocessor(apts, areas, trade, rent, '202306')
    apt_grp = preproc.monthly()
    if apt_grp.shape[0] >= 1:
        plotter = ApartmentPricePlotter(apt_grp, apts, areas)
        plotter.plot()