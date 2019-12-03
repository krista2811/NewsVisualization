<template>
  <v-container fill-height>
    <v-row
      :align="center"
      :justify="center">
      <v-col>
        <v-combobox
          class="ma-5"
          v-model="keys"
          :items="items"
          label="Search with Keywords"
          placeholder="Press enter to divide your keywords"
          multiple
          chips
          >
        </v-combobox>
      </v-col>
    </v-row>
    
  </v-container>
</template>

<script>
  export default {
    data () {
      return {
        keys: [],
        items: []
      }
    },
  }
</script>