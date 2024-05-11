import requests
import json
from objects import Item

base_url = 'https://prices.runescape.wiki/api/v1/osrs/'
mapping_url = base_url + '/mapping'
latest_url = base_url + '/latest'
headers = {
        'User-Agent': '@matt-fevold',
        # 'From': 'youremail@domain.example'  # This is another valid field
    }


def main():

    item_dict, failed_items = load_mapping_data()
    # print(item_dict[4405])  # just to spot check.

    response = requests.get(latest_url, headers=headers)
    # # print(response.text)

    data = json.loads(response.text)
    for item_id_str in data['data']:
        # def a better way, but this is laziness
        item_id_int = int(item_id_str)

        if item_id_int in item_dict:
            item_dict[item_id_int].high_time = data['data'][item_id_str]['highTime']
            item_dict[item_id_int].low_time = data['data'][item_id_str]['lowTime']
            item_dict[item_id_int].high_price = data['data'][item_id_str]['high']
            item_dict[item_id_int].low_price = data['data'][item_id_str]['low']
            print(item_dict[item_id_int])

    # now ready to check for any good deals on latest price!

    # item_high - item_low = profit_per_item    # todo 1% tax
    # profit_per_item * GE_limit = profit_per_4_hours
    # check if GE_limit > daily volume, probably just ignore these

    # validate profit or item price is valid for timestamps to make sure price isn't a temp spike?


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
            mapping_data.update({item.id: item})
        except KeyError:
            failed_items_ids.append(d['id'])

    return mapping_data, failed_items_ids


if __name__ == '__main__':
    main()