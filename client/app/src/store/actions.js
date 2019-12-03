import axios from 'axios'

var elasticsearch = require('elasticsearch')
const {PythonShell} = require('python-shell');
// let pyshell = new PythonShell('/Users/jeong-yujin/Library/CloudStorage/iCloudDrive/Documents/GitHub/NewsVisualization/server/test.py')

var client = new elasticsearch.Client({
  host: 'localhost:9200',
  log: 'trace'
})
const index = "visual_news"
const root = 'http://localhost:5000/'
const basic_time_body = {
  aggs: {
    4: {
      date_histogram: {
        field: "timestamp",
        interval: "30d",
        time_zone: "Asia/Seoul",
        min_doc_count: 1
      },
      aggs: {
        5: {
          filters: {
            filters: {}
          }
        }
      }
    }
  },
  size: 0,
  stored_fields: [
    "*"
  ],
  docvalue_fields: [
    {
      field: "timestamp",
      format: "date_time"
    }
  ],
  query: {
    bool: {
      must: [
        {
          bool: {
            should: [
            ],
            minimum_should_match: 1
          }
        },
        {
          range: {
            timestamp: {
              format: "strict_date_optional_time",
              gte: "2006-08-09T02:10:11.452Z",
              lte: "2019-08-09T02:10:11.452Z"
            }
          }
        }
      ],
      filter: [
        {
          match_all: {}
        }
      ]
    }
  }
}


function make_hist_body (keywords) {
  var should = []
  var filters = {}
  for (var i; i < keywords.length; i++) {
    keyword = keywords[i]

    var phrase = {
        match_phrase: {title: keyword}
    }
    var query_string = {query: keyword}
    filters[keyword] = {query_string: query_string}
    should.push(phrase)

    basic_time_body[aggs][4][aggs][5][filters][filters] = filters
    console.log(basic_time_body)

    basic_time_body[query][bool][must][0][bool][should] = should
  }
  
  return basic_time_body
}

function get (body) {    
  results = es.search(index=index, body=body)
  return results['aggregations']['title']['buckets']
}

export default {
  get_histogram(context, payload) {
    console.log(payload)
    const path = root + "hist"
    axios.post(path, payload)
      .then((res) => {
        context.commit('setTimes', res.data.time)
        context.commit('setData', res.data.keywords)
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
      });
  },
  test (context, payload) {
    var options = {
      mode: 'json',
      pythonPath: '',
      pythonOptions: ['-u'],
      scriptPath: '/Users/jeong-yujin/Library/CloudStorage/iCloudDrive/Documents/GitHub/NewsVisualization/server',
      args: ['감자']
    };
    PythonShell.run('test.py', options, function(err, resuts) {
      console.log(results)
    })
  },
  async getHist (context, payload) {
    console.log(payload);
    var hist_body = make_hist_body(payload["query"]);
    console.log('hist_body')
    console.log(hist_body)
    const results = await client.search({
      index: index,
      body: hist_body
    })
    console.log(results)
    // data = results['aggregations']['4']['buckets']
    // return get_hist (payload)
  }
}