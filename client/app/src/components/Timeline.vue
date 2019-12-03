<template>
  <v-container fluid>
    <v-sheet width="100%" height="100%" elevation="2">
    <v-row
      justify="center"
      class="lg-12"
      align="center"
      no-gutters>
      <v-col class="pl-5 pt-5" offset="0">
        <v-combobox
          v-model="keys"
          :items="items"
          :search-input.sync="search"
          hide-selected
          label="Search with Keywords"
          placeholder="Press enter to divide your keywords"
          multiple
          solo
          clearable
          small-chips
          >
            <template v-slot:no-data>
              <v-list-item>

                <v-list-item-content>
                  <v-list-item-title>
                    Press <kbd>enter</kbd> to add "<strong>{{ search }}</strong>"
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </template>
            <template v-slot:selection="data">
           <v-chip
              :key="JSON.stringify(data.item)"
              v-bind="data.attrs"
              color="lime lighten-5"
              :input-value="data.selected"
              :disabled="data.disabled"
              @click:close="data.parent.selectItem(data.item)"
            >
              <v-avatar
                class=" white--text"
                color="lime darken-2"
                left
                v-text="data.item.slice(0, 1).toUpperCase()"
              ></v-avatar>
              {{ data.item }}
            </v-chip>
            </template>
        </v-combobox>
      </v-col>
      <v-col sm="1" class="pb-3 pl-8">
        <v-btn class="mt-1" text large
          :loading="loading" 
          @click="submitData"
          fill-height color="lime darken-3" >Submit</v-btn>
      </v-col>

    </v-row> 
    </v-sheet>

    <v-row 
      justify="center"
      class="pt-10 lg-12"
      no-gutters>
      <v-col>
        <v-card color="lime lighten-5" v-if="plotAvailable">
        <v-sheet width="98%" class="v-sheet--offset mx-auto"
      elevation="8">
          <vue-plotly @click="fetchTable"
            :layout="layout"
            :data="plots"/>
        </v-sheet>
        <v-card-title v-if="tableAvailable">News Table</v-card-title>
        <v-data-table v-if="tableAvailable"
          :headers="headers"
          :items="docs"
          class="elevation-1"></v-data-table>
      </v-card>
      </v-col>
    </v-row>

    
  </v-container>
</template>
<style>
  .v-sheet--offset {
    top: -24px;
    position: relative;
  }
</style>
<script>
  import {
    mapActions,
    mapMutations,
    mapState
  } from 'vuex'
  import axios from 'axios'

  import VuePlotly from '@statnett/vue-plotly'

  export default {
    computed: {
        ...mapState['times', 'data']
    },
    components: {
      VuePlotly
    },
    methods: {
      ...mapActions(['getHist', 'test', 'get_histogram']),
      ...mapMutations(['setKeywords']),
      submitData () {
        this.loading = true;
        this.setKeywords(this.keys);
        var pseudoKey = ["낮"]
        for (var key in this.keys) {
          pseudoKey.push(this.keys[key])
        }
        var payload = {
          query: pseudoKey
        }
        this.getKeywordHists(payload);
        this.loading = false;
      },
      fetchTable(data) {
        console.log(data.points[0].x)
        axios.post("http://localhost:5000/table", {keywords:this.keys, start: data.points[0].x}).then((res) => {
          this.docs = res.data.data
          console.log(this.docs)
        })
        this.tableAvailable = true
      },
      getKeywordHists(payload) {
        axios.post("http://localhost:5000/hist", payload)
        .then((res) => {
          this.plots = []
          this.plotTIme = res.data.time
          this.plotData = res.data.keywords
          for (var keyword in res.data.keywords) {
            if (keyword == "낮") {
              continue
            } else {
              var plot = {
                x: res.data.time, 
                y: res.data.keywords[keyword],
                name: keyword
              };
              this.plots.push(plot)
              this.plotAvailable = true              
            }

          }
          this.loading = false;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
      }
    },
    data () {
      return {
        loading: false,
        keys: [],
        items: [],
        layout: {
          autosize: true,
          showlegend: true
        },
        search: null,
        plotAvailable: false,
        tableAvailable: false,
        plots: [],
        plotData: [],
        plotTIme: [],
        headers: [{
            text: 'Time',
            value: 'timestamp',
          },
          { text: 'Office', value: 'office' },
          { text: 'Title', value: 'title' },
          { text: 'Url', value: 'url' }],
        docs: []
      }
    },
  }
</script>