<!--
  Global snackbar component. Hooked to vuex store.
  Use with: this.$store.commit("showMessage", { text: "", color: "" });
-->
<template>
  <v-snackbar
    v-model="snackbar.visible"
    :timeout="snackbar.timeout"
    :color="snackbar.color"
    :bottom="true"
    :left="true"
    :multi-line="snackbar.multiline === true">
      {{ snackbar.text }}  
      <v-btn v-if="snackbar.close" dark @click="closeMessage">Sulje</v-btn>
  </v-snackbar>
</template>

<script>
  import { mapMutations } from "vuex"
  export default {
    computed: {
      snackbar() {
        return this.$store.state.snackbar
      }
    },
    methods: {
      ...mapMutations(["closeMessage"])
    }
  }
</script>