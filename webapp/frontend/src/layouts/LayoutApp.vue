<template>
  <div>
    <router-view></router-view>
  </div>
  <Snackbar></Snackbar>
</template>

<script>
  import Snackbar from '/src/global/Snackbar.vue';

  export default {
    name: 'LayoutLogin',
    components: {
      Snackbar,
    },
    mounted() {
      // TODO: Check that user is logged in, if not, redirect to /login
    },
  }
</script>

<style scoped lang="scss">
</style>