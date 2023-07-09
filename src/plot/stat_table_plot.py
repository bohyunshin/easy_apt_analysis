import matplotlib.pyplot as plt
import os

class TablePlotter:
    def __init__(self):
        return

    def plot(self, df, save_dir, file_name):
        fig, ax = plt.subplots()

        # # hide axes
        # fig.patch.set_visible(False)
        # ax.axis('off')
        # ax.axis('tight')
        # ax.set_fontsize(30)
        # ax.table(cellText=df.values, colLabels=df.columns, loc='center', fontsize=30)
        #
        # fig.tight_layout()
        # plt.savefig(save_dir, dpi=2000)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        the_table = plt.table(cellText=df.values,
                              colLabels=df.columns,
                              loc='center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(7)
        fig.tight_layout()
        os.makedirs(save_dir, exist_ok=True)
        plt.savefig(save_dir+file_name, dpi=2000)