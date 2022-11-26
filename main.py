import os
from parsers.weapon_parser import WeaponParser
from parsers.armor_parser import ArmorParser
from parsers.magic_parser import MagicParser

ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(ROOT_FOLDER, 'files', 'input')
output_folder = os.path.join(ROOT_FOLDER, 'files', 'output')


def main():
    weapon_parser = WeaponParser(input_folder)
    weapon_parser.write_weapons_to_file(output_folder)

    armor_parser = ArmorParser(input_folder)
    armor_parser.write_armor_to_file(output_folder)

    magic_parser = MagicParser(input_folder)
    magic_parser.write_magic_to_file(output_folder)


if __name__ == '__main__':
    main()
