<template>
  <div>
    <slot></slot>
    <Footer />
    <Snackbar></Snackbar>
  </div>
</template>

<script>
  import Snackbar from '/src/components/global/Snackbar.vue';
  import Footer from '/src/components/global/Footer'

  export default {
    name: 'LayoutLogin',
    components: {
      Snackbar,
      Footer,
    },
  }
</script>

<style scoped lang="scss">
</style>