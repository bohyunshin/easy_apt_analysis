import pandas as pd
import numpy as np

from util.tools import *

class Preprocessor:
    def __init__(self, apts, areas, trade, rent, end_yrm):
        trade['전용면적'] = trade['전용면적'].map(lambda x: int(x))
        rent['전용면적'] = rent['전용면적'].map(lambda x: int(x))
        self.rent = rent[lambda x: (x['아파트'].isin(apts)) & (x['전용면적'].isin(areas))]
        self.trade = trade[lambda x: (x['아파트'].isin(apts)) & (x['전용면적'].isin(areas))]
        self.apts = apts
        self.areas = areas
        self.end_yrm = end_yrm


    def monthly(self):
        trade_grp = pd.DataFrame()
        rent_grp = pd.DataFrame()
        for apt in self.apts:
            for area in self.areas:
                trade_grp = self._monthly(trade_grp, self.trade, apt, area, '거래금액')
                rent_grp = self._monthly(rent_grp, self.rent, apt, area, '보증금액')

        if trade_grp.shape[0] == 0 or rent_grp.shape[0] == 0:
            return pd.DataFrame()

        trade_grp['datetime'] = trade_grp['yrm'].map(lambda x: make_datetime(x))
        rent_grp['datetime'] = rent_grp['yrm'].map(lambda x: make_datetime(x))

        apt_grp = pd.merge(trade_grp, rent_grp, how='left', on=['yrm', 'datetime', 'apt', 'area'])
        apt_grp['yrm'] = apt_grp['yrm'].astype(str)

        return apt_grp

    def _monthly(self, data_grp, data_raw, apt, area, price_col):
        tmp = data_raw[lambda x: (x['아파트'] == apt) & (x['전용면적'] == area) & (x['층'] >= 4)].\
                groupby(['yrm','전용면적'])[price_col].mean().\
                to_frame().reset_index(). \
                sort_values(by='yrm')
        if tmp.shape[0] >= 1:
            return pd.concat([data_grp, self.get_yrms_prices(tmp, apt, area, self.end_yrm, price_col)])
        else:
            return data_grp

    def get_yrms_prices(self, apt_grp, apt_name, area, end_yrm, price_col):
        yrms, prices = [], []
        yrm_before, yrm_after = 2000, 2000
        price_before, price_after = 0, 0
        for index, row in apt_grp.iterrows():
            yrm_after, price_after = str(int(row['yrm'])), int(row[price_col])
            if index == 0:
                yrms.append(yrm_after)
                prices.append(price_after)
                yrm_before = yrm_after
                price_before = price_after
            else:
                # 저번달 이력과 이번달 이력이 연속할 때,
                if make_one_step(yrm_before) == yrm_after:
                    yrms.append(yrm_after)
                    prices.append(price_after)
                # 거래 이력이 두달 연속 존재하지 않을 때,
                # 저번달 거래 이력을 거래 이력이 있기 전 달까지 추가함.
                else:
                    yrm_before = make_one_step(yrm_before)
                    while yrm_before != yrm_after:
                        yrms.append(yrm_before)
                        prices.append(price_before)
                        yrm_before = make_one_step(yrm_before)
                    yrms.append(yrm_after)
                    prices.append(price_after)
                yrm_before = yrm_after
                price_before = price_after
        # 현재까지 거래 안 된 단지들 처리
        while yrm_after != end_yrm:
            yrm_after = make_one_step(yrm_after)
            yrms.append(yrm_after)
            prices.append(price_after)

        return pd.DataFrame({'yrm': yrms, price_col: prices, 'apt': apt_name, 'area': area})