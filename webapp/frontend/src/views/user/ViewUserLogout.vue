<template>
  <div>
  </div>
</template>

<script>
  export default {
    name: 'ViewUserLogout',

    components: {
    },
    mounted() {
      let _this = this
      this.$store.commit("logoutUser", { callback: (res) => {
        console.log(res)
        console.log("logged out...")
        _this.$router.push("/")
      }})
      
    },
  }
</script>

<style scoped lang="scss">
</style>