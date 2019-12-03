<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title color="primary" class="headline text-uppercase">
        <span>News</span>
        <span class="font-weight-light">Visualization</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        text
        href="https://github.com/krista2811/NewsVisualization"
        target="_blank"
      >
        <span class="mr-2">Latest Release</span>
      </v-btn>
    </v-app-bar>

    <v-content>
      <v-container fluid fill-height>
        <v-row justify="center" align="center" no-gutters>

          <Timeline/>      
        </v-row>  
      </v-container>
      
      <!-- <HelloWorld/> -->
    </v-content>
    <v-footer padless color="primary" elevation="4">
      <v-col class="text-center" cols="12">News Visualization</v-col>
    </v-footer>
  </v-app>
</template>

<script>
import Timeline from './components/Timeline';

export default {
  name: 'App',
  components: {
    Timeline
  },
  data: () => ({
    //
  }),
};
</script>
