<template>
  <v-app>
    <v-app-bar app elevation="4">
      <a @click="reservations">Reservations</a>
      <a @click="profile">Profile</a>
      <a @click="logout">Logout</a>
    </v-app-bar>

    <v-main>
      <v-container>
        <slot></slot>
      </v-container>
    </v-main>
    
    <Footer />
    <Snackbar></Snackbar>
  </v-app>
</template>

<script>
  import Snackbar from '/src/components/global/Snackbar.vue';
  import Footer from '/src/components/global/Footer'

  export default {
    name: 'LayoutApp',
    components: {
      Snackbar,
      Footer,
    },
    mounted() {
      // TODO: Check that user is logged in, if not, redirect to /login
    },
    methods: {
      logout() {
        this.$router.push("/user/logout")
      },
      reservations() {
        this.$router.push("/user/reservations")
      },
      profile() {
        console.log("IMPLEMENT")
        //this.$router.push("/user/reservations")
      }
    },
  }
</script>

<style scoped lang="scss">
</style>