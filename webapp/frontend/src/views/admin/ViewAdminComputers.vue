<template>
  <LayoutApp>
    <div id="view-login">
      <v-slide-x-transition mode="out-in">
        <PageAdminComputers />
      </v-slide-x-transition>
    </div>
  </LayoutApp>
</template>

<script>
  import LayoutApp from '/src/layouts/LayoutApp'
  import PageAdminComputers from '/src/pages/admin/PageAdminComputers'

  export default {
    name: 'ViewAdminComputers',

    components: {
      LayoutApp,
      PageAdminComputers,
    },
  }
</script>

<style scoped lang="scss">
</style>