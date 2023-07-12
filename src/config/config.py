import yaml
import os
from pathlib import Path


class commonColumnNamesConfig:
    trade: str
    rent: str
    area: str
    year: str
    month: str

    def __init__(self, raw_config: dict[str, any]):
        self.trade = raw_config.get('trade', '')
        self.rent = raw_config.get('rent', '')
        self.area = raw_config.get('area', '')
        self.year = raw_config.get('year', '')
        self.month = raw_config.get('month', '')


class crawlDataConfig:
    trade_url: str
    rent_url : str
    service_key_decoded: str
    save_data_directory: str

    def __init__(self, raw_config: dict[str, any]):
        self.trade_url = raw_config.get('tradeUrl', '')
        self.rent_url = raw_config.get('rentUrl', '')
        self.service_key_decoded = raw_config.get('serviceKeyDecoded', '')
        self.save_data_directory = raw_config.get('saveDataDirectory', '')


class analyzerConfig:
    basic_stat: dict
    search_lowest_maejeongap: dict

    def __init__(self, raw_config: dict[str, any]):
        self.basic_stat = raw_config.get('basicStat', '')
        self.search_lowest_maejeongap = raw_config.get('searchLowestMaejeonGap', '')


class preprocessorConfig:
    end_year_month: str

    def __init__(self, raw_config: dict[str, any]):
        self.end_year_month = raw_config.get('endYearMonth', '')


class plotConfig:
    maejeon_plot: dict
    stat_table_plot: dict

    def __init__(self, raw_config: dict[str, any]):
        self.maejeon_plot = raw_config.get('maeJeonPlot', '')
        self.stat_table_plot = raw_config.get('statTablePlot', '')


class Config:
    def __init__(self):
        if not os.getenv('PROJECT_ROOT_PATH'):
            raise Exception("PROJECT_ROOT_PATH env variable not set")
        self.project_root_path = Path(os.getenv('PROJECT_ROOT_PATH'))
        with self.project_root_path.joinpath("./configs/config.yaml").open("r") as yaml_path:
            self._content = yaml.safe_load(yaml_path)
        self.common_column_names = self._content["commonColumnNames"]
        self.crawl_data = self._content["crawlData"]
        self.analyzer = self._content["analyzer"]
        self.preprocessor = self._content["preprocessor"]
        self.plot = self._content["plot"]

if __name__ == "__main__":
    config = Config()
    print(config.plot)