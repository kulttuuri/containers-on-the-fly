<template>
  <LayoutApp>
    <div id="view-login">
      <v-slide-x-transition mode="out-in">
        <PageAdminHardware />
      </v-slide-x-transition>
    </div>
  </LayoutApp>
</template>

<script>
  import LayoutApp from '/src/layouts/LayoutApp'
  import PageAdminHardware from '/src/pages/admin/PageAdminHardware'

  export default {
    name: 'ViewAdminHardware',

    components: {
      LayoutApp,
      PageAdminHardware,
    },
  }
</script>

<style scoped lang="scss">
</style>