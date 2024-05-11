import requests
import json
from objects import Item

base_url = 'https://prices.runescape.wiki/api/v1/osrs/'
mapping_url = base_url + '/mapping'
latest_url = base_url + '/latest'
volume_url = base_url + '/volumes'
headers = {
    'User-Agent': '@matt-fevold',
    # 'From': 'youremail@domain.example'  # This is another valid field
}

# the wiki_id for items to ignore for any reason, seasonal, certain worlds, etc
ignored_items = [22647,]

def main():
    # todo check failed_items at some point, could be value there!
    items, failed_items = load_mapping_data()
    items = load_pricing_data(items)
    items = load_volume_data(items)
    items = filter_ignored_ids(items, ignored_items)

    # for item in items:
    #     print(items[item])
    # now ready to check for any good deals on latest price!

    # item_high - item_low = profit_per_item    # todo 1% tax
    possibly_profitable_items = []
    failed_profitable_check = []

    for item in items:
        try:
            item = items[item]
            profit_per_item_sold = item.high_price - item.low_price
            profit_per_GE_limit = profit_per_item_sold * item.limit

            # trades more than GE limit, possibly want to multiply by some factor
            # over_trading_threshold = (item.volume - item.limit) > 0

            # 100k
            if profit_per_GE_limit > 100000:  # and over_trading_threshold:
                possibly_profitable_items.append(item)
        except TypeError:
            # todo some missing item price data, check those later
            failed_profitable_check.append(item)

    for item in possibly_profitable_items:
        print(item)
        print("expected profit", (item.high_price - item.low_price) * item.limit)

    print("total:")
    print("  items: ", len(items))
    print("  failed_items: ", len(failed_items))
    print("  possibly_profitable_items: ", len(possibly_profitable_items))
    print("  failed_profitable_check", len(failed_profitable_check))

    # profit_per_item * GE_limit = profit_per_4_hours
    # check if GE_limit > daily volume, probably just ignore these

    # validate profit or item price is valid for timestamps to make sure price isn't a temp spike?


def filter_ignored_ids(items, ignore_list):
    for ignore in ignore_list:
        items.pop(ignore)

    return items


def load_pricing_data(items):
    response = requests.get(latest_url, headers=headers)

    data = json.loads(response.text)
    for item_id_str in data['data']:
        # def a better way, but this is laziness
        item_id_int = int(item_id_str)

        if item_id_int in items:
            items[item_id_int].high_time = data['data'][item_id_str]['highTime']
            items[item_id_int].low_time = data['data'][item_id_str]['lowTime']
            items[item_id_int].high_price = data['data'][item_id_str]['high']
            items[item_id_int].low_price = data['data'][item_id_str]['low']

    return items


def load_volume_data(items):
    response = requests.get(volume_url, headers=headers)

    data = json.loads(response.text)
    # print(data)
    for item_id_str in data['data']:
        # def a better way, but this is laziness
        item_id_int = int(item_id_str)

        if item_id_int in items:
            items[item_id_int].volume = data['data'][item_id_str]
            items[item_id_int].volume_time = data['timestamp']

    return items



# returns a tuple (dict, list)
# a dict of all items for easy lookup
# a list of id's that are missing some key (possibly worth looking into!!)
# todo - load this from file or DB, not API call since data doesn't change often.
def load_mapping_data():
    mapping_data = {}
    failed_items_ids = []

    response = requests.get(mapping_url, headers=headers)
    data = json.loads(response.text)

    for d in data:
        try:
            item = Item(d['id'], d['name'], d['limit'], d['members'], d['highalch'])
            mapping_data.update({item.wiki_id: item})
        except KeyError:
            failed_items_ids.append(d['id'])

    return mapping_data, failed_items_ids


if __name__ == '__main__':
    main()
