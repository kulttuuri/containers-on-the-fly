<template>
  <LayoutApp>
    <div id="view-login">
      <v-slide-x-transition mode="out-in">
        <PageAdminUsers />
      </v-slide-x-transition>
    </div>
  </LayoutApp>
</template>

<script>
  import LayoutApp from '/src/layouts/LayoutApp'
  import PageAdminUsers from '/src/pages/admin/PageAdminUsers'

  export default {
    name: 'ViewAdminUsers',

    components: {
      LayoutApp,
      PageAdminUsers,
    },
  }
</script>

<style scoped lang="scss">
</style>