<template>
  <LayoutApp>
    <div id="view-login">
      <v-slide-x-transition mode="out-in">
        <PageAdminGroups />
      </v-slide-x-transition>
    </div>
  </LayoutApp>
</template>

<script>
  import LayoutApp from '/src/layouts/LayoutApp'
  import PageAdminGroups from '/src/pages/admin/PageAdminGroups'

  export default {
    name: 'ViewAdminGroups',

    components: {
      LayoutApp,
      PageAdminGroups,
    },
  }
</script>

<style scoped lang="scss">
</style>
