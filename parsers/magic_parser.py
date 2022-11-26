from extensions.utilities import get_items_ids
import os
import pandas as pd
from bs4 import BeautifulSoup


def get_magic_stats_from_dict(stats: dict) -> str:
    if stats['ezStateBehaviorType'] == 0:
        magic_school_type = 'Магия'
    else:
        magic_school_type = 'Молитва'
    stat_s = f'Общее:\n' \
             f'  Вид заклинания: {magic_school_type}\n' \
             f'  Расход ОК: {stats["mp"]}\n' \
             f'  Расход выносливости: : {stats["stamina"]}\n' \
             f'  Ячейки: {stats["slotLength"]}\n' \
             f'  Длительность: {stats["effectEndurance"]}\n' \
             f'Требования:\n' \
             f'  Муд: {stats["requirementIntellect"]}\n' \
             f'  Вер: {stats["requirementFaith"]}\n' \
             f'  Кол: {stats["requirementLuck"]}'
    return stat_s


class MagicParser:
    def __init__(self, path: str):
        self.base_folder_path = path
        self.df_magic: pd.DataFrame = pd.read_csv(os.path.join(path, 'stats/Magic.csv'),
                                                  delimiter=',', on_bad_lines='skip', low_memory=False)
        self.df_duration: pd.DataFrame = pd.read_csv(os.path.join(path, 'stats/SpEffectParam.csv'),
                                                     delimiter=',', on_bad_lines='skip', low_memory=False)

    def get_stats_magic(self, item_id: int):
        magic = self.df_magic.loc[self.df_magic['ID'] == item_id]
        eng_name = magic.iloc[0]['Name']

        # region Duration
        # todo Fix Duration
        '''
        duration_id = magic[['refId1']]

        try:
            duration = self.df_duration.loc[self.df_duration['ID'] == duration_id][
                ['effectEndurance']].to_dict('list')['effectEndurance'][0]
        except KeyError as err_name:
            print(f'{err_name} with {item_id} ({eng_name})')
            duration = '-'
        '''
        # endregion
        stats = magic[['requirementLuck',
                       'requirementIntellect',
                       'requirementFaith',
                       'mp',
                       'stamina',
                       'slotLength',
                       'analogDexterityMin',
                       'analogDexterityMax',
                       'ezStateBehaviorType']]
        stats = stats.to_dict('list')
        stats['effectEndurance'] = '-'
        for key, value in stats.items():
            stats[key] = value[0]
        return stats

    def write_magic_to_file(self, path_to_write: str = ''):
        with open(os.path.join(self.base_folder_path, 'en/GoodsName.fmg.xml'), 'rb') as f:
            eng_names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, 'ru/GoodsName.fmg.xml'), 'rb') as f:
            names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, 'ru/GoodsInfo.fmg.xml'), 'rb') as f:
            captions = BeautifulSoup(f, 'lxml')
        # I don't know why I wrote this and why it's useless
        with open(os.path.join(self.base_folder_path, 'ru/GoodsInfo2.fmg.xml'), 'rb') as f:
            captions2 = BeautifulSoup(f, 'lxml')

        file = open(os.path.join(path_to_write, 'magic.txt'), 'w', encoding='utf-8')

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
