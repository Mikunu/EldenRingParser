from extensions.utilities import trueround, get_items_ids
import os
import pandas as pd
from bs4 import BeautifulSoup


def get_armor_stats_from_dict(stats: dict) -> str:
    armor_type: str = ''
    if stats["Is Head Equipment"]:
        armor_type = 'Голова'
    elif stats["Is Body Equipment"]:
        armor_type = 'Туловище'
    elif stats["Is Arm Equipment"]:
        armor_type = 'Руки'
    elif stats["Is Leg Equipment"]:
        armor_type = 'Ноги'
    stat_s: str = f'Общее:\n' \
                  f'  Стоимость продажи: {stats["Sell Value"]}\n' \
                  f'  Вес: {stats["Weight"].replace(",", ".")}\n' \
                  f'  Часть брони: {armor_type}\n' \
                  f'Защита:\n' \
                  f'  Физич.: {trueround((1 - float(stats["Absorption - Physical"].replace(",", "."))) * 100, 1)}\n' \
                  f'  Дробящий: {trueround((1 - float(stats["Absorption - Strike"].replace(",", "."))) * 100, 1)}\n' \
                  f'  Рубящий: {trueround((1 - float(stats["Absorption - Slash"].replace(",", "."))) * 100, 1)}\n' \
                  f'  Колющий: {trueround((1 - float(stats["Absorption - Thrust"].replace(",", "."))) * 100, 1)}\n' \
                  f'  Магия: {trueround((1 - float(stats["Absorption - Magic"].replace(",", "."))) * 100, 1)}\n' \
                  f'  Огонь: {trueround((1 - float(stats["Absorption - Fire"].replace(",", "."))) * 100, 1)}\n' \
                  f'  Молния: {trueround((1 - float(stats["Absorption - Lightning"].replace(",", "."))) * 100, 1)}\n' \
                  f'  Святое: {trueround((1 - float(stats["Absorption - Holy"].replace(",", "."))) * 100, 1)}\n' \
                  f'Сопротивления:\n' \
                  f'  Яд (Имуннитет): {stats["Resist - Poison"]}\n' \
                  f'  Красная гниль (Имуннитет): {stats["Resist - Scarlet Rot"]}\n' \
                  f'  Кровотечение (Живучесть): {stats["Resist - Hemorrhage"]}\n' \
                  f'  Обморожение (Живучесть): {stats["Resist - Frost"]}\n' \
                  f'  Сон (Концент.): {stats["Resist - Sleep"]}\n' \
                  f'  Безумие (Концент.): {stats["Resist - Madness"]}\n' \
                  f'  Смерть (Физ. мощь) {stats["Resist - Blight"]}\n' \
                  f'  Баланс: {trueround(float(stats["Poise"].replace(",", ".")) * 1000)}'
    return stat_s


class ArmorParser:
    def __init__(self, path: str):
        self.base_folder_path = path
        self.df_armor: pd.DataFrame = pd.read_csv(os.path.join(path, 'EquipParamProtector.csv'),
                                                  delimiter=';', on_bad_lines='skip', low_memory=False)

    def get_stats_protector(self, item_id: int) -> dict:
        weapon = self.df_armor.loc[self.df_armor['Row ID'] == item_id]
        stats = weapon[['resistSleep',
                        'resistMadness',
                        'toughnessCorrectRate',
                        'sellValue',
                        'weight',
                        'resistPoison',
                        'resistScarlet Rot',
                        'resistBlood',
                        'resistBlight',
                        'resistFrost',
                        'defencePhysics',
                        'defenceSlash',
                        'defenceBlow',
                        'defenceThrust',
                        'defenceMagic',
                        'defenceFire',
                        'defenceLightning',
                        'defenceHoly',
                        'headEquip',
                        'bodyEquip',
                        'armEquip',
                        'legEquip', ]]
        stats = stats.to_dict('list')
        for key, value in stats.items():
            stats[key] = value[0]
        return stats

    def write_armor_to_file(self, path_to_write: str = ''):
        with open(os.path.join(self.base_folder_path, 'ProtectorNameEng.fmg.xml'), 'rb') as f:
            eng_names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, 'ProtectorName.fmg.xml'), 'rb') as f:
            names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, 'ProtectorInfo.fmg.xml'), 'rb') as f:
            captions = BeautifulSoup(f, 'lxml')

        file = open(os.path.join(path_to_write, 'armor_test.txt'), 'a', encoding='utf-8')

        items_ids = get_items_ids(self.df_armor)

        for item_id in items_ids:
            if item_id < 10500:
                continue
            name = names.find(id=item_id)
            eng_name = eng_names.find(id=item_id)
            caption = captions.find(id=item_id)
            if name is None or eng_name is None:
                continue
            try:
                info_s = f'Item ID:{item_id}\n{name.text} (англ. {eng_name.text})\n{caption.text}'
                stats_s = get_armor_stats_from_dict(self.get_stats_protector(item_id))
                result = f'{info_s}\n{stats_s}\n{"-" * 50}\n'
                result = result.replace('\n\n\n', '\n')
                file.write(result)
            except Exception as e:
                print(f'Exception with item_id: {item_id}. {e}')
