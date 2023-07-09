import pandas as pd
from data.call_api import GetData
from analysis.analyzer import Analyzer
from preprocessing.preprocessor import Preprocessor
from plot.stat_table_plot import TablePlotter

if __name__ == '__main__':
    serviceKey_encoded = '%2BoAljLVOTD7bcsTkWNsO81np7%2BXxXoLi6vSBhAAkXHw073r3hcRSCLJUn2iUhYHm6sus6ty8xaD5%2BNHhgk4iiw%3D%3D'
    serviceKey_decoded = 'vzFxdH7xpXMB/rFZma+5owAjBkTdqCr+zQ40LMCvw+3IXQXshvwn7fOf1agVGjcztAo95ltWi0cMCNCAly6OTw=='
    get_data = GetData(serviceKey_decoded)
    # 다운받은 데이터를 불러오는 경우
    trade_dir = '../sample_data/trade_daejeon_yoosung.csv'
    rent_dir = '../sample_data/rent_daejeon_yoosung.csv'
    trade, rent = get_data.load_trade_rent_data(trade_dir, rent_dir)
    trade['전용면적'] = trade['전용면적'].map(lambda x: int(x))
    rent['전용면적'] = rent['전용면적'].map(lambda x: int(x))
    apts = list(set(trade['아파트'].unique()) | set(rent['아파트'].unique()))
    areas = [84] # 수익률분석은 84만 진행함.
    rent_rate_landmark = 78
    preproc = Preprocessor(apts, areas, trade, rent, '202306')
    apt_grp = preproc.monthly()

    analyzer = Analyzer()
    table_plotter = TablePlotter()
    for apt in apts:
        print(f'{apt} done')
        trade_filtered = trade[lambda x: (x['아파트'] == apt) & (x['전용면적'] == 84)]
        rent_filtered = rent[lambda x: (x['아파트'] == apt) & (x['전용면적'] == 84)]

        if trade_filtered.shape[0] == 0 or rent_filtered.shape[0] == 0:
            continue

        basic_stat = analyzer.basic_stat(trade_filtered, rent_filtered, 202211)
        table_plotter.plot(basic_stat, f'../save_fig/{apt}/', f'basic_stat_{apt}.png')

        lowest_maejeon_gap = analyzer.search_lowest_maejeon_gap(apt_grp[lambda x: x['apt'] == apt])
        if lowest_maejeon_gap.shape[0] >= 1:
            table_plotter.plot(lowest_maejeon_gap, f'../save_fig/{apt}/', f'maejeon_gap_analysis_{apt}.png')

        if '201608' not in apt_grp[lambda x: x['apt'] == apt]['yrm'].tolist():
            continue
        compare_rate_dfs = analyzer.compare_rate(apt_grp[lambda x: x['apt'] == apt], '201608', rent_rate_landmark)
        for i, df in enumerate(compare_rate_dfs):
            table_plotter.plot(df, f'../save_fig/{apt}/', f'compare_lmk_{apt}_{i}.png')