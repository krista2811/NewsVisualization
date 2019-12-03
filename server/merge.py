from elasticsearch import Elasticsearch
from elasticsearch import helpers
from os import walk
import json
from datetime import datetime, date

es = Elasticsearch()

url = "http://localhost:9200"
cnt = 1
limit = 500000
index = "ver1"

mainpath = "/Users/jeong-yujin/Downloads/main/main"

body = {
"_source": {
"excludes": []
},
"stored_fields": [
"*"
],
"script_fields": {},
"query": {
"bool": {
"must": [
{
"match_phrase": {
"url": {
"query": "oid=056&aid=0010687912"
}
}
},
{
"range": {
"timestamp": {
"format": "strict_date_optional_time",
"gte": "2004-09-19T03:39:09.012Z",
"lte": "2019-09-19T03:39:09.012Z"
}
}
}
],
"filter": [
{
"match_all": {}
}
],
"should": [],
"must_not": []
}
}
}

def parseDate (expose, date):
    (bf, af) = list(map(lambda x: x.strip(), expose.split("~")))
    return (parseOneDate(bf, date), parseOneDate(af, date))

def parseOneDate (rawdate, date):
    # print(rawdate)
    (md, hm) = rawdate.split(" ")[:2]
    (month, day) = md.split("/")
    (hour, minute) = hm.split(":")
    return datetime(date.year, int(month), int(day), int(hour), int(minute))

for (dirpath, dirnames, filenames) in walk(mainpath):
    for filename in filenames:
        print(filename)
        with open(dirpath+"/"+filename, encoding="utf-8") as file:
            f = json.loads(file.read())

            for data in f:
                url = data['url']
                basedate = datetime.strptime(filename.split(".")[0], "%Y-%m-%d")
                try:
                    expose = data['expose']
                    (beforedata, afterdata) = parseDate(expose, basedate)
                except KeyError:
                    # no exposure time data available in this section, just assign 00:00 ~ 23:59
                    beforedata = datetime(basedate.year, basedate.month, basedate.day, 0, 0)
                    afterdata = datetime(basedate.year, basedate.month, basedate.day, 23, 59)

                oid_aid = "&".join(url.split("&")[-2:])

                #search for the right doc
                body['query']['bool']['must'][0]['match_phrase']['url']['query'] = oid_aid
                res = es.search(index=index, body=body)

                for res_data in res['hits']['hits']:
                    # update item value
                    es.update(index=index, id=res_data['_id'], body={"doc": {
                      "main": "true", "main_start": beforedata.isoformat(), "main_end": afterdata.isoformat()
                      }})



