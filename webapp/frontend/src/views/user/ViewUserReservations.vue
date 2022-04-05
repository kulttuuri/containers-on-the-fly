<template>
  <LayoutApp>
    <div id="view-login">
      <v-slide-x-transition mode="out-in">
        <PageUserReservations />
      </v-slide-x-transition>
    </div>
  </LayoutApp>
</template>

<script>
  import LayoutApp from '/src/layouts/LayoutApp'
  import PageUserReservations from '/src/pages/user/PageUserReservations'

  export default {
    name: 'ViewUserReservations',

    components: {
      LayoutApp,
      PageUserReservations,
    },
  }
</script>

<style scoped lang="scss">
</style>