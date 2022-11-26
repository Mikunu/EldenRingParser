import pandas as pd


def trueround(number: int | float, places=0):
    place = 10 ** places
    rounded = (int(number * place + 0.5 if number >= 0 else -0.5)) / place
    if rounded == int(rounded):
        rounded = int(rounded)
    return rounded


def get_items_ids(df: pd.DataFrame):
    items = df[['ID', 'Name']]
    items_mask = pd.notnull(items['Name'])
    items = items[items_mask]
    ids = []
    for row in items.itertuples():
        ids.append(row[1])
    return ids


# todo: marked for deletion
def sort_by_sort_id(df: pd.DataFrame):
    return df.sort_values(by=['Sort ID'])


def get_required_stats_from_dict(requirements: dict) -> str:
    return f'Требования: ' \
           f'Сил: {requirements["properStrength"]}, ' \
           f'Лов: {requirements["properAgility"]}, ' \
           f'Муд: {requirements["properMagic"]}, ' \
           f'Вер: {requirements["properFaith"]}, ' \
           f'Кол: {requirements["properLuck"]}'
