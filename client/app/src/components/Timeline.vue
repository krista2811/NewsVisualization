<template>
  <v-container>
    <v-combobox
      v-model="keys"
      :items="items"
      label="Press enter to get your keywords"
      multiple>
    </v-combobox>
  </v-container>
</template>

<script>
  export default {
    data () {
      return {
        select: ['Vuetify', 'Programming'],
        items: [
          'Programming',
          'Design',
          'Vue',
          'Vuetify',
        ],
      }
    },
  }
</script>