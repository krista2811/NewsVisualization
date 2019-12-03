from elasticsearch import Elasticsearch
from elasticsearch import helpers
from tqdm import tqdm

def parse_oid_aid(url):
    oid_aid = url.split("&")[-2:]
    return {'oid': oid_aid[0].split("=")[1], 'aid': oid_aid[1].split("=")[1]}

def parse_mil(res, es):
    actions = []
    cnt = 0
    for res_data in res['hits']['hits']:
        # print(res_data)
        try:
            oid = res_data['_source']['oid']
            cnt += 1
        except KeyError:
            # update item value
            try:
                oid_aid = parse_oid_aid(res_data['_source']['url'])
                doc = {"oid": oid_aid['oid'], "aid": oid_aid['aid']}

                action = {
                '_op_type': 'update',
                "_index": 'ver1',
                "_id": res_data['_id'],
                'doc': doc}
                actions.append(action)
            except KeyError:
                print(res_data['_source'])
                pass
    if len(actions) > 0: 
        print("already has oid_aid: {}, new: {}".format(cnt, len(actions)))
        helpers.bulk(es, actions)

es = Elasticsearch(['http://localhost:9200'])
doc = {
"size": 10000,
'query': {
    "bool": {
      "must": [
        {
          "range": {
            "timestamp": {
              "format": "strict_date_optional_time",
              "gte": "2019-03-16T05:26:08.836Z",
              "lte": "2019-04-04T00:00:00.000Z"
            }
          }
        }
      ],
      "filter": [
        {
          "match_all": {}
        }
      ],
      "must_not": [
        {
          "exists": {
            "field": "oid"
          }
        }
      ]
      }
}
}
tot = 900000

res = es.search(index='ver1', body=doc, scroll='1m')
scrollId = res['_scroll_id']
parse_mil(res, es)

for i in tqdm(range(int(tot/10000)+2)):
    res = es.scroll(scroll_id=scrollId, scroll='1m')
    scrollId = res['_scroll_id']
    parse_mil(res, es)
