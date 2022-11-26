from extensions.utilities import trueround, get_items_ids
import os
import pandas as pd
from bs4 import BeautifulSoup


def get_armor_stats_from_dict(stats: dict) -> str:
    armor_type: str = ''
    if stats["headEquip"]:
        armor_type = 'Голова'
    elif stats["bodyEquip"]:
        armor_type = 'Туловище'
    elif stats["armEquip"]:
        armor_type = 'Руки'
    elif stats["legEquip"]:
        armor_type = 'Ноги'
    stats_template = (
        'Шаблон:Броня',
        [
            f'Баланс={trueround(float(stats["toughnessCorrectRate"]) * 1000)}',
            f'Вес={stats["weight"]}',
            f'Дробящий={trueround((1 - float(stats["blowDamageCutRate"])) * 100, 1)}',
            f'Живучесть={stats["resistBlood"]}',
            f'Защита от магии={trueround((1 - float(stats["magicDamageCutRate"])) * 100, 1)}',
            f'Защита от молнии={trueround((1 - float(stats["thunderDamageCutRate"])) * 100, 1)}',
            f'Защита от огня={trueround((1 - float(stats["fireDamageCutRate"])) * 100, 1)}',
            f'Защита от света={trueround((1 - float(stats["darkDamageCutRate"])) * 100, 1)}',
            f'Иммунитет={stats["resistPoison"]}',
            f'Колющий={trueround((1 - float(stats["thrustDamageCutRate"])) * 100, 1)}',
            f'Концентрация={stats["resistMadness"]}',
            f'Покупка={stats["basicPrice"]}',
            f'Продажа={stats["sellValue"]}',
            f'Рубящий={trueround((1 - float(stats["slashDamageCutRate"])) * 100, 1)}',
            f'Тип брони={armor_type}',
            f'Физ. мощь={stats["resistCurse"]}',
            f'Физический урон={trueround((1 - float(stats["neutralDamageCutRate"])) * 100, 1)}'
        ]
    )

    return stats_template


class ArmorParser:
    def __init__(self, path: str):
        self.base_folder_path = path
        self.df_armor: pd.DataFrame = pd.read_csv(os.path.join(path, 'stats/EquipParamProtector.csv'),
                                                  delimiter=',', on_bad_lines='skip', low_memory=False)

    def get_stats_protector(self, item_id: int) -> dict:
        weapon = self.df_armor.loc[self.df_armor['ID'] == item_id]
        stats = weapon[[
            'headEquip',
            'bodyEquip',
            'armEquip',
            'legEquip',
            'basicPrice',
            'sellValue',
            'weight',
            'resistPoison',
            'resistBlood',
            'resistFreeze',
            'resistCurse',
            'resistSleep',
            'resistMadness',
            'neutralDamageCutRate',
            'slashDamageCutRate',
            'blowDamageCutRate',
            'thrustDamageCutRate',
            'magicDamageCutRate',
            'fireDamageCutRate',
            'thunderDamageCutRate',
            'darkDamageCutRate',
            'toughnessCorrectRate',
        ]]
        stats = stats.to_dict('list')
        for key, value in stats.items():
            stats[key] = value[0]
        return stats

    def write_armor_to_file(self, path_to_write: str = ''):
        with open(os.path.join(self.base_folder_path, 'en/ProtectorName.fmg.xml'), 'rb') as f:
            eng_names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, 'ru/ProtectorName.fmg.xml'), 'rb') as f:
            names = BeautifulSoup(f, 'lxml')

        file = open(os.path.join(path_to_write, 'armor_data.txt'),
                    'a', encoding='utf-8')

        items_ids = get_items_ids(self.df_armor)

        for item_id in items_ids:
            if item_id < 10500:  # means that it's not an armor item
                continue
            name = names.find(id=item_id)
            eng_name = eng_names.find(id=item_id)
            if name is None or eng_name is None:
                continue
            try:
                title = f'Item ID:{item_id}\n{name.text} (англ. {eng_name.text})\n'
                parsed_stats = get_armor_stats_from_dict(self.get_stats_protector(item_id))
                result = f'{title}\n{parsed_stats}\n{"-" * 50}\n'
                result = result.replace('\n\n\n', '\n')
                file.write(result)
            except Exception as e:
                print(f'Exception with item_id: {item_id}. {e}')
