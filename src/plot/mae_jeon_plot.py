import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
import os

sns.set_style('darkgrid')
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

class ApartmentPricePlotter:
    def __init__(self, apt_grp, apts, areas, colr2cycle=None):
        """
        color2cycle: {color : [from_datetime, to_datetime]}
        [example]
        color2region = {
        '#EF9A9A':[ # 상승기
            (datetime(2009,9,1), datetime(2012,12,1)),
        ],
        'lightskyblue':[ # 하락기
            (datetime(2019,5,1), datetime(2019,11,1)),
        ],
         'lightgreen':[ # 보합기
             (datetime(2013,1,1), datetime(2014,7,1))
         ]
        }
        """
        self.apt_grp = apt_grp
        self.apts = apts
        self.areas = areas
        self.colr2cycle = colr2cycle

    def plot(self):
        for i, apt in enumerate(self.apts):
            print(f'{apt} done: {i} out of {len(self.apts)}')
            for area in self.areas:
                apt_df = self.apt_grp[lambda x: (x['apt'] == apt) & (x['area'] == area)]
                if apt_df.shape[0] == 0:
                    continue
                plt.figure(figsize=(30, 15))
                sns.lineplot(x='datetime', y='보증금액', linewidth=2.5,
                                  data=apt_df, color='green')
                ax = sns.lineplot(x='datetime', y='거래금액', linewidth=2.5,
                                  data=apt_df, color='mediumblue')
                self.title_legend(ax, apt, area)
                self.axis()
                if self.colr2cycle != None:
                    self.background_color(ax)
                os.makedirs(f'../save_fig/{apt}', exist_ok=True)
                plt.savefig(f'../save_fig/{apt}/{apt}_{area}.png', bbox_inches='tight')
                # plt.show()

    def background_color(self, ax):
        for color, region in self.colr2cycle.items():
            for (start, end) in region:
                ax.axvspan(start, end, color=color, alpha=0.5)
        min_dt = self.apt_grp['datetime'].min()
        max_dt = self.apt_grp['datetime'].max()
        plt.xlim((min_dt, max_dt))

    def title_legend(self, ax, apt, area):

        plt.title(f'{apt} 전용 {area} 매매, 전세 추이', fontsize=30, weight='bold')
        # plt.setp(ax.get_legend().get_texts(), fontsize='20')  # for legend text
        # plt.setp(ax.get_legend().get_title(), fontsize='25')  # for legend title

    def axis(self):
        plt.xlabel('날짜', fontsize=30, weight='bold')
        plt.ylabel('가격', fontsize=30, weight='bold')
        plt.xticks(rotation=45, fontsize=25, weight='bold')
        plt.yticks(fontsize=25, weight='bold')
