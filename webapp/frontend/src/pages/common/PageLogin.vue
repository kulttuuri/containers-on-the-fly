<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('/src/assets/images/front_bg.jpg')"
          class="my-3"
          contain
          height="350"
        />
      </v-col>

      <v-col class="mb-4">
        <h3 class="color-violet dim">Login to</h3>
        <h1 class="color-violet">SAMK AI Server</h1>
      </v-col>

      <v-col class="mb-5" cols="12">
        <v-form ref="form" v-model="form['valid']" lazy-validation>
          <v-text-field style="max-width: 300px; margin: 0 auto;" label="Email Address" v-model="form['email']" :rules="validation['email']" required></v-text-field>
          <v-text-field style="max-width: 300px; margin: 0 auto;" label="Password" v-model="form['password']" :rules="validation['password']" required></v-text-field>
          <v-btn :disabled="!form['valid']" color="success" @click="submitLoginForm" label="Login">Login</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  const axios = require('axios').default;
  
  export default {
    name: 'PageLogin',

    data: () => ({
      snackbar: true,
      form: {
        email: "",
        password: "",
        valid: true,
      },
      validation: {
        email: [
          v => !!v || 'Email is required',
        ],
        password: [
          v => !!v || 'Password is required',
        ],
      }
    }),
    methods: {
      submitLoginForm() {
        if (!this.$refs.form.validate()) return
        console.log(this.form.username)
        //console.log(this.form.password)
        console.log(this.form.valid)
        let _this = this
        axios.get(this.AppSettings.APIServer.address + 'user/login', {
          auth: {
            username: this.form.email,
            password: this.form.password,
          }})
          .then(function (response) {
            // Success
            if (response.data && response.data.success) {
              // Set user data and token to local storage, redirect to containers page
              localStorage.setItem("loginToken", response.data.loginToken)
            }
            else {
              console.log("Failed to login.")
              _this.$store.commit('showMessage', { text: response.data.message, color: "red" })
            }
          })
          .catch(function (error) {
            // Error
            console.log(error)
            _this.$store.commit('showMessage', { text: "Unknown error.", color: "alert" })
          })
          .then(function () {
            // always executed
          });
      }
    }
  }
</script>
