from extensions.utilities import get_items_ids, get_required_stats_from_dict
import os
import pandas as pd
from bs4 import BeautifulSoup


def get_weapon_stats_from_dict(weapon_stats: dict) -> str:
    return f'Атака: ' \
           f'Физическ.: {weapon_stats["attackBasePhysics"]} ' \
           f'Магия: {weapon_stats["attackBaseMagic"]}, ' \
           f'Огонь: {weapon_stats["attackBaseFire"]}, ' \
           f'Молния: {weapon_stats["attackBaseThunder"]}, ' \
           f'Святое: {weapon_stats["attackBaseDark"]}, ' \
           f'Крит. удар: {weapon_stats["throwAtkRate"] + 100}\n' \
           f'Защита :' \
           f'Физическ.: {weapon_stats["physGuardCutRate"]}, ' \
           f'Магия: {weapon_stats["magGuardCutRate"]}, ' \
           f'Огонь: {weapon_stats["fireGuardCutRate"]}, ' \
           f'Молния: {weapon_stats["thunGuardCutRate"]}, ' \
           f'Святое: {weapon_stats["darkGuardCutRate"]}, ' \
           f'Усил. блок {weapon_stats["staminaGuardDef"]}\n' \
           f'Вес: {weapon_stats["weight"]}, ' \
           f'Цена: ' \
           f'Покупка: [NO INFO], ' \
           f'Продажа: {weapon_stats["sellValue"]}'


class WeaponParser:

    def __init__(self, path: str):
        self.base_folder_path = path
        self.df_weapon: pd.DataFrame = pd.read_csv(os.path.join(self.base_folder_path, 'stats/EquipParamWeapon.csv'),
                                                   delimiter=',', index_col=False)
        self.df_weapon_art: pd.DataFrame = pd.read_csv(os.path.join(self.base_folder_path, 'stats/SwordArtsParam.csv'),
                                                   delimiter=',', index_col=False)

    def get_weapon_stats(self, item_id: int) -> dict:
        """
        Get weapon stats from EquipParamWeapon.csv file

        :param item_id: weapon id
        :return: dict with weapon's stats
        """
        weapon = self.df_weapon.loc[self.df_weapon['ID'] == item_id]
        weapon_stats = weapon[['attackBasePhysics',
                               'attackBaseMagic',
                               'attackBaseFire',
                               'attackBaseThunder',
                               'attackBaseDark',
                               'attackBaseStamina',
                               'throwAtkRate',
                               'physGuardCutRate',
                               'magGuardCutRate',
                               'fireGuardCutRate',
                               'thunGuardCutRate',
                               'darkGuardCutRate',
                               'staminaGuardDef',
                               'weight',
                               'sellValue',
                               'weaponCategory']]
        weapon_stats = weapon_stats.to_dict('list')
        for key, value in weapon_stats.items():
            weapon_stats[key] = value[0]

        return weapon_stats

    def get_weapon_art(self, item_id: int):
        weapon_art_row = self.df_weapon.loc[self.df_weapon['ID'] == item_id]
        return weapon_art_row['swordArtsParamId'].item()

    def get_required_stats(self, item_id: int):
        weapon = self.df_weapon.loc[self.df_weapon['ID'] == item_id]
        requirements = weapon[['properStrength', 'properAgility', 'properMagic',
                               'properFaith', 'properLuck']]
        requirements = requirements.to_dict('list')
        for key, value in requirements.items():
            requirements[key] = value[0]
            if requirements[key] == 0:
                requirements[key] = '-'

        return requirements

    def write_weapons_to_file(self, path_to_write: str = ''):
        with open(os.path.join(self.base_folder_path, r'ru/WeaponName.fmg.xml'), 'rb') as f:
            names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, r'en/WeaponName.fmg.xml'), 'rb') as f:
            eng_names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, r'ru/WeaponCaption.fmg.xml'), 'rb') as f:
            captions = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, r'ru/ArtsName.fmg.xml'), 'rb') as f:
            arts_names = BeautifulSoup(f, 'lxml')

        with open(os.path.join(self.base_folder_path, r'ru/ArtsCaption.fmg.xml'), 'rb') as f:
            arts_captions = BeautifulSoup(f, 'lxml')

        print('All weapon data loaded')

        file = open(os.path.join(path_to_write, 'weapons.txt'), 'w', encoding='utf-8')

        items_ids = get_items_ids(self.df_weapon)
        prev_item_id = -1
        for item_id in items_ids:

            if item_id < 1000000 or item_id >= 50000000:  # Weapons between 110000 and 50000000
                continue

            item_id = item_id // 10000 * 10000
            if item_id == prev_item_id:
                continue
            name = names.find(id=item_id)
            eng_name = eng_names.find(id=item_id)
            caption = captions.find(id=item_id)
            weapon_art_id = self.get_weapon_art(item_id)

            weapon_art = self.df_weapon_art.loc[self.df_weapon_art['ID'] == weapon_art_id]
            weapon_art_fp_cons_dict = weapon_art[['useMagicPoint_L1', 'useMagicPoint_L2',
                                             'useMagicPoint_R1', 'useMagicPoint_R2']].to_dict('list')
            weapon_art_fp_cons = weapon_art_fp_cons_dict[
                max(weapon_art_fp_cons_dict, key=weapon_art_fp_cons_dict.get)][0]

            if weapon_art_id == 0:
                art_name = '<text></text>'
                art_caption = '<text></text>'
            else:
                art_name = arts_names.find(id=weapon_art_id)
                art_caption = arts_captions.find(id=weapon_art_id)

            if name is None or eng_name is None or caption is None or art_name is None or art_caption is None:
                print(f'Problem with {item_id}')
                continue
            prev_item_id = item_id
            try:
                info_s = f'{name.text} (англ. {eng_name.text})\n{caption.text}\n' \
                         f'{art_caption.text}\n' \
                         f'Траты ОК: {weapon_art_fp_cons}'
                requirements_s = get_required_stats_from_dict(self.get_required_stats(item_id))
                stats_s = get_weapon_stats_from_dict(self.get_weapon_stats(item_id))
                result = f'{info_s}\n{requirements_s}\n{stats_s}\n{"-" * 50}\n'
                result = result.replace('\n\n\n', '\n')
                file.write(result)
                # print(f'"{name.text}" proceeded')
            except Exception as e:
                print(f'Exception with item_id: {item_id}. {e}')

        print('All weapon proceeded')
