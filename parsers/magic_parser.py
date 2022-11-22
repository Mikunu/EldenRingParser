from extensions.utilities import get_items_ids
import os
import pandas as pd
from bs4 import BeautifulSoup


def get_magic_stats_from_dict(stats: dict) -> str:
    if stats['Magic School Type'] == 0:
        magic_school_type = 'Магия'
    else:
        magic_school_type = 'Молитва'
    stat_s = f'Общее:\n' \
             f'  Вид заклинания: {magic_school_type}\n' \
             f'  Расход ОК: {stats["FP Cost"]}\n' \
             f'  Расход выносливости: : {stats["Stamina Cost"]}\n' \
             f'  Ячейки: {stats["Slot Usage"]}\n' \
             f'  Длительность: {stats["duration"]}\n' \
             f'  Ловкость скорость каста минимум: {stats["DEX Casting Speed Min"]}\n' \
             f'  Ловкость скорость каста максимум: {stats["DEX Casting Speed Max"]}\n' \
             f'Требования:\n' \
             f'  Муд: {stats["Requirement: INT"]}\n' \
             f'  Вер: {stats["Requirement: FTH"]}\n' \
             f'  Кол: {stats["Requirement: ARC"]}'
    return stat_s


class MagicParser:
    def __init__(self, path: str):
        self.base_folder_path = path
        self.df_magic: pd.DataFrame = pd.read_csv(os.path.join(path, 'Magic.csv'),
                                                  delimiter=';', on_bad_lines='skip', low_memory=False)
        self.df_duration: pd.DataFrame = pd.read_csv(os.path.join(path, 'SpEffectParam.csv'),
                                                     delimiter=';', on_bad_lines='skip', low_memory=False)

    def get_stats_magic(self, item_id: int):
        magic = self.df_magic.loc[self.df_magic['Row ID'] == item_id]
        eng_name = magic.iloc[0]['Row Name']
        duration = \
            self.df_duration.loc[self.df_duration['Row Name'] == eng_name][['Duration']].to_dict('list')['Duration']
        stats = magic[['Requirement: ARC',
                       'Requirement: INT',
                       'Requirement: FTH',
                       'FP Cost',
                       'Stamina Cost',
                       'Slot Usage',
                       'DEX Casting Speed Min',
                       'DEX Casting Speed Max',
                       'Magic School Type']]
        stats = stats.to_dict('list')
        stats['duration'] = duration
        for key, value in stats.items():
            stats[key] = value[0]
        return stats

    def write_magic_to_file(self, path_to_write: str = ''):
        with open(os.path.join(self.base_folder_path, 'GoodsNameEng.fmg.xml'), 'rb') as f:
            eng_names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, 'GoodsName.fmg.xml'), 'rb') as f:
            names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, 'GoodsInfo.fmg.xml'), 'rb') as f:
            captions = BeautifulSoup(f, 'lxml')
        # I don't know why I wrote this and why it's useless
        with open(os.path.join(self.base_folder_path, 'GoodsInfo2.fmg.xml'), 'rb') as f:
            captions2 = BeautifulSoup(f, 'lxml')

        file = open(os.path.join(path_to_write, 'magic.txt'), 'a', encoding='utf-8')

        items_ids = get_items_ids(self.df_magic)

        for item_id in items_ids:
            name = names.find(id=item_id)
            eng_name = eng_names.find(id=item_id)
            caption = captions.find(id=item_id)

            if name is None or eng_name is None:
                continue
            try:
                info_s = f'Item ID: {item_id}\n{name.text} (англ. {eng_name.text})\n{caption.text}'
                stats_s = get_magic_stats_from_dict(self.get_stats_magic(item_id))
                result = f'{info_s}\n{stats_s}\n{"-" * 50}\n'
                result = result.replace('\n\n\n', '\n')
                file.write(result)
            except Exception as e:
                print(f'Exception with item_id: {item_id}. {e}')
