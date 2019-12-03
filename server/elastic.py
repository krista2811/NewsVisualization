from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch()

url = "http://localhost:9200"
cnt = 1
limit = 500000
index = "visual_news"

basic_time_body = {
  "aggs": {
    "4": {
      "date_histogram": {
        "field": "timestamp",
        "interval": "1M",
        "time_zone": "Asia/Seoul",
        "min_doc_count": 1
      },
      "aggs": {
        "5": {
          "filters": {
            "filters": {
              "감지": {
                "query_string": {
                  "query": "감지",
                  "analyze_wildcard": True
                }
              },
              "고구마": {
                "query_string": {
                  "query": "고구마",
                  "analyze_wildcard": True
                }
              },
              "옥수수": {
                "query_string": {
                  "query": "옥수수",
                  "analyze_wildcard": True
                }
              }
            }
          }
        }
      }
    }
  },
  "size": 0,
  "_source": {
    "excludes": []
  },
  "stored_fields": [
    "*"
  ],
  "script_fields": {},
  "docvalue_fields": [
    {
      "field": "timestamp",
      "format": "date_time"
    }
  ],
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "should": [
              {
                "match_phrase": {
                  "title": "감자"
                }
              },
              {
                "match_phrase": {
                  "title": "고구마"
                }
              },
              {
                "match_phrase": {
                  "title": "옥수수"
                }
              }
            ],
            "minimum_should_match": 1
          }
        },
        {
          "range": {
            "timestamp": {
              "format": "strict_date_optional_time",
              "gte": "2006-08-09T02:10:11.452Z",
              "lte": "2019-08-09T02:10:11.452Z"
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

basic_table_body = {
  "size": 500,
  "sort": [{
    "timestamp": "asc"
    }
  ],
  "stored_fields": [
    "*"
  ],
  "script_fields": {},
  "_source": {
    "excludes": []
  },
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "should": [
              {
                "match_phrase": {
                  "title": "감자"
                }
              },
              {
                "match_phrase": {
                  "title": "고구마"
                }
              },
              {
                "match_phrase": {
                  "title": "옥수수"
                }
              }
            ],
            "minimum_should_match": 1
          }
        },
        {
          "range": {
            "timestamp": {
              "format": "strict_date_optional_time",
              "gte": "2011-09-22T15:00:00.000Z",
              "lt": "2011-09-23T03:00:00.000Z"
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
  },
}

def make_hist_body(keywords):
    new_body = basic_time_body
    should = []
    filters = {}
    for keyword in keywords:
        phrase = {
            "match_phrase": {"title": keyword}
        }
        query_string = {"query": keyword}
        filters[keyword] = {"query_string": query_string}
        should.append(phrase)

    new_body['aggs']['4']['aggs']['5']['filters']['filters'] = filters
    new_body['query']['bool']['must'][0]['bool']['should'] = should

    return new_body

def make_table_body(keywords, start, end):
  new_body = basic_table_body
  should = []
  for keyword in keywords:
      phrase = {
          "match_phrase": {"title": keyword}
      }
      query_string = {"query": keyword}
      should.append(phrase)
  new_body['query']['bool']['must'][0]['bool']['should'] = should
  new_body['query']['bool']['must'][1]['range']['timestamp'] = {
              "format": "strict_date_optional_time",
              "gte": start,
              "lt": end
            }
  return new_body 

def get(body):
    results = es.search(index=index, body=body)
    return results['aggregations']['title']['buckets']

def get_hist(keywords):
    hist_body = make_hist_body(keywords)
    results = es.search(index=index, body=hist_body)
    return results['aggregations']['4']['buckets']

def get_table(keywords, start, end):
    table_body = make_table_body(keywords, start, end)
    results = es.search(index=index, body=table_body)
    return results['hits']
