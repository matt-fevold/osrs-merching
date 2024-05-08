import requests
import json


def main():
    base_url = 'https://prices.runescape.wiki/api/v1/osrs/'

    item_id = 28924
    latest_url = base_url + '/latest?id=' + str(item_id)

    headers = {
        'User-Agent': '@matt-fevold',
        # 'From': 'youremail@domain.example'  # This is another valid field
    }

    response = requests.get(latest_url, headers=headers)
    print(response.text)


    data = json.loads(response.text)
    print(data['data'])  # or `print data['two']` in Python 2

    item_stats = data['data'][str(item_id)]
    high_price = item_stats['high']
    high_time = item_stats['highTime']
    low_price = item_stats['low']
    low_time = item_stats['lowTime']

    # get GE limit

    mapping_url = base_url + '/mapping?id=' + str(item_id)
    print(item_stats)
    response = requests.get(mapping_url, headers=headers)
    print(response.text)

    data = json.loads(response.text)
    # print(data['data'])
    # for item in data:
    #     print(item['name'])



if __name__ == '__main__':
    main()