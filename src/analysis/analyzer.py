import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

class Analyzer:
    def __init__(self):
        return

    def basic_stat(self, trade, rent, yrm_from):
        recent_trade = trade[lambda x: x['yrm'] >= yrm_from]
        recent_rent = rent[lambda x: x['yrm'] >= yrm_from]
        max_trade = trade['거래금액'].max()
        max_rent = rent['보증금액'].max()
        max_trade_yrm = trade[lambda x: x['거래금액'] == max_trade]['yrm'].tolist()[0]
        max_rent_yrm = rent[lambda x: x['보증금액'] == max_rent]['yrm'].tolist()[0]
        trade_cnt = recent_trade.shape[0]
        rent_cnt = recent_rent.shape[0]
        return pd.DataFrame(
            [[max_trade_yrm, max_trade, max_rent_yrm,  max_rent, trade_cnt, rent_cnt]],
            columns=['매매 전고점 시기\n(년/월)', '매매 전고점', '전세 전고점 시기\n(년/월)', '전세 전고점', f'{yrm_from}부터\n매매 거래량(건)', f'{yrm_from}부터\n전세 거래량(건)']
        )

    def search_lowest_maejeon_gap(self, data):
        """
        search for period which produces highest return rate
        """
        data = data.sort_values(by='yrm')
        data['maejeon_gap'] = data['거래금액'] - data['보증금액']
        data['rent_rate'] = round(data['보증금액'] / data['거래금액'] * 100, 2)

        # search for period with lowest maejeon_gap
        lowest_gap = data[lambda x: x['maejeon_gap'] > 0]['maejeon_gap'].min()
        if pd.isna(lowest_gap):
            return pd.DataFrame()
        buy_price = data[lambda x: x['maejeon_gap'] == lowest_gap]['거래금액'].tolist()[0]
        buy_yrm = data[lambda x: x['maejeon_gap'] == lowest_gap]['yrm'].tolist()[0]
        rent_rate = data[lambda x: x['maejeon_gap'] == lowest_gap]['rent_rate'].tolist()[0]

        # search for period with highest return of rate
        rate = -1
        sell_price_, sell_yrm_ = -1, -1
        for i, row in data.iterrows():
            if row['yrm'] <= buy_yrm:
                continue
            sell_price, sell_yrm = row['거래금액'], row['yrm']
            now_rate = self.rate_of_return(lowest_gap, buy_price, sell_price)
            if now_rate > rate:
                rate = now_rate
                sell_price_ = sell_price
                sell_yrm_ = sell_yrm
        return pd.DataFrame(
            [[buy_yrm, lowest_gap, rent_rate, buy_price, sell_yrm_, sell_price_, rate]],
            columns=['최저갭 시기 (년/월)', '최저갭', '최고전세가율(%)', '최저갭 매매가', '매도 시기(년/월)', '매도가', '수익률(%)']
        )

    def compare_rate(self, data, yrm, jeonsaega_rate_landmark):
        buy_info = data[lambda x: x['yrm'] == yrm]
        for i, row in buy_info.iterrows():
            buy_price = row['거래금액']
            rent_price = row['보증금액']
            maejeon_gap = row['거래금액'] - row['보증금액']
            rent_rate = round(rent_price / buy_price * 100, 2)

        data = data[lambda x: x['yrm'] > yrm]
        rate = -1
        sell_price_, sell_yrm_ = -1, -1
        for index, row in data.iterrows():
            sell_price, sell_yrm = row['거래금액'], row['yrm']
            now_rate = self.rate_of_return(maejeon_gap, buy_price, sell_price)
            if now_rate > rate:
                rate = now_rate
                sell_price_ = sell_price
                sell_yrm_ = sell_yrm
        return pd.DataFrame(
            [[yrm, jeonsaega_rate_landmark, buy_price, rent_rate]],
            columns=['랜드마크 비교시기(년/월)', '랜드마크 전세가율(%)', '매수가', '매수시 전세가율(%)']
        ), pd.DataFrame(
            [[sell_yrm_, sell_price_, rate]],
            columns=['매도시기(년/월)', '매도가', '수익률(%)']
        )

    def rate_of_return(self, mae_jeon_gap, buy_price, sell_price):
        if mae_jeon_gap <= 0:  # 플러프피 / 무피 투자
            return np.infty
        else:
            # (매도가격 - 매수가격) / 투자금
            return round((sell_price - buy_price) / mae_jeon_gap * 100, 2)