from collections import defaultdict
from datetime import datetime
from .settings import BASE_DIR


class PepParsePipeline:

    def __init__(self):
        self.status_counter = defaultdict(int)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        total = sum(self.status_counter.values())
        datetime.now()

        with open(
                f'{BASE_DIR}/results/status_summary_{datetime.now()}.csv',
                mode='w',
                encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status, count in self.status_counter.items():
                print(f'{status}, {count}', file = f)
            f.write(f'Total,{total}\n')
