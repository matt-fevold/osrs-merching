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
    print(item_dict[4405])  # just to spot check.

    # response = requests.get(latest_url, headers=headers)
    # # print(response.text)
    #
    # data = json.loads(response.text)
    # for item_id in data['data']:
    #     # print(item_id)
    #     # print(data['data'][str(item_id)])
    #     # print(mapping_data[item_id])
    #     pass

    # item_stats = data['data'][str(item_id)]
    # high_price = item_stats['high']
    # high_time = item_stats['highTime']
    # low_price = item_stats['low']
    # low_time = item_stats['lowTime']

    # get GE limit

    # print(response.text)

    # print(data['data'])  # probably store this one DB.
    # for item in data:
    #     print(item['name'])

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