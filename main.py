from parsers.weapon_parser import WeaponParser
from parsers.armor_parser import ArmorParser
from parsers.magic_parser import MagicParser


def main():
    base_folder = r'C:\Users\nonam\Desktop\EldenRing\newbf'
    path_to_save = r'C:\Users\nonam\Desktop\EldenRing\output'

    weapon_parser = WeaponParser(base_folder)
    weapon_parser.write_weapons_to_file(path_to_save)

    # armor_parser = ArmorParser(base_folder)
    # armor_parser.write_armor_to_file(path_to_save)
    #
    # magic_parser = MagicParser(base_folder)
    # magic_parser.write_magic_to_file(path_to_save)


if __name__ == '__main__':
    main()
