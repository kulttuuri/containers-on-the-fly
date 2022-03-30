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
    mounted() {
      // TODO: Check user login, redirect back to /login if user is not logged in
    },
  }
</script>

<style scoped lang="scss">
</style>