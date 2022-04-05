<template>
  <v-container>
    <v-row class="text-center">
      <v-col>
        <v-btn color="success" large @click="createReservation">Reserve Server</v-btn>
      </v-col>
    </v-row>

    <v-row class="text-center mt-10">
      <v-col class="mb-4">
        <h2>Your Reservations</h2>
        <p class="dim">No servers reserved yet.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'PageUserReservations',

    methods: {
      createReservation() {
        this.$router.push("/user/reserve")
      }
    }
  }
</script>
