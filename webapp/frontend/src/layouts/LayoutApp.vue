<template>
  <v-app v-if="isLoggedIn">
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
    data: () => ({
      show: true,
    }),
    mounted() {
      if (!this.isLoggedIn) {
        console.log("User is not logged in and trying to access logged-in users page")
        this.$router.push("/user/logout")
      }
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
    computed: {
      isLoggedIn() {
        return this.$store.getters.isLoggedIn || false;
      }
    },
    beforeRouteUpdate(to, from, next) {
      this.show = false
      next()
    },
    watch: {
      $route (to, from) {
        this.show = true
        console.log(to, from)
      }
    }
  }
</script>

<style scoped lang="scss">
</style>