<template>
  <LayoutLogin>
    <div id="view-login">
      <v-slide-x-transition mode="out-in">
        <PageLogin />
      </v-slide-x-transition>
    </div>
    <Footer />
  </LayoutLogin>
</template>

<script>
  import LayoutLogin from '/src/layouts/LayoutLogin'
  import PageLogin from '/src/pages/common/PageLogin'
  import Footer from '/src/components/global/Footer'

  export default {
    name: 'ViewLogin',

    components: {
      PageLogin,
      Footer,
      LayoutLogin,
    },
    mounted() {
      // TODO: If user is already logged in, redirect to app
    },
  }
</script>

<style scoped lang="scss">
  #view-login {
    margin: 50px auto;
    text-align: center;
  }
</style>