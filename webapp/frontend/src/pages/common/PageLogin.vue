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
          <v-text-field type="email" style="max-width: 300px; margin: 0 auto;" label="Email Address" v-model="form['email']" :rules="validation['email']" required></v-text-field>
          <v-text-field type="password" style="max-width: 300px; margin: 0 auto;" label="Password" v-model="form['password']" :rules="validation['password']" required></v-text-field>
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
        let _this = this
        let bodyFormData = new FormData()
        bodyFormData.append("username", this.form.email)
        bodyFormData.append("password", this.form.password)

        axios({
          method: "post",
          url: this.AppSettings.APIServer.user.login,
          data: bodyFormData,
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(function (response) {
            // Success
            if (response.data && response.data.access_token) {
              // Set user data
              _this.$store.commit("setUser", { loginToken: response.data.access_token, callback: (res) => {
                //console.log(res)
                if (res.success)
                  {
                    _this.$router.push("/user/reservations");
                  }
                  else
                  {
                    _this.$store.commit('showMessage', { text: "Error logging in.", color: "red" })
                  }
                }
              });
              // TODO: Redirect to containers page
            }
            else {
              console.log("Failed to login.")
              _this.$store.commit('showMessage', { text: response.data.message, color: "red" })
            }
        })
        .catch(function (error) {
            // Error
            if (error.response && error.response.status == 400) {
              _this.$store.commit('showMessage', { text: error.response.data.detail, color: "alert" })
            }
            else {
              console.log(error)
              _this.$store.commit('showMessage', { text: "Unknown error.", color: "alert" })
            }
        });
      }
    }
  }
</script>
