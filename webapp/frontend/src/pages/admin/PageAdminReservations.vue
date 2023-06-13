<template>
  <v-container>

    <v-row class="text-center">
      <v-col cols="12">
        <h4>Admin</h4>
        <h2>All Reservations</h2>
        <p class="dim">Listing reservations from past 3 months</p>
      </v-col>
    </v-row>

    <v-row v-if="!isFetchingReservations">
      <v-col cols="12">
        <div v-if="reservations && reservations.length > 0" style="margin-top: 50px">
          <AdminReservationTable @emitCancelReservation="cancelReservation" @emitChangeEndDate="changeEndDate" @emitRestartContainer="restartContainer" @emitShowReservationDetails="showReservationDetails" v-bind:propReservations="reservations" />
        </div>
        <p v-else class="dim text-center">No servers reserved yet.</p>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <Loading class="loading" />
      </v-col>
    </v-row>
    <UserReservationsModalConnectionDetails :reservationId="modalConnectionDetailsReservationId" v-on:emitModalClose="closeModalConnectionDetails" v-if="modalConnectionDetailsVisible && modalConnectionDetailsReservationId != null"></UserReservationsModalConnectionDetails>
  </v-container>
</template>

<script>
  const axios = require('axios').default;
  import Loading from '/src/components/global/Loading.vue';
  import AdminReservationTable from '/src/components/admin/AdminReservationTable.vue';
  import UserReservationsModalConnectionDetails from '/src/components/user/UserReservationsModalConnectionDetails.vue';
  
  export default {
    name: 'PageUserReservations',

    components: {
      Loading,
      AdminReservationTable,
      UserReservationsModalConnectionDetails
    },
    data: () => ({
      intervalFetchReservations: null,
      isFetchingReservations: false,
      reservations: [],
      justReserved: false,
      informByEmail: false,
      modalConnectionDetailsVisible: false,
      modalConnectionDetailsReservationId: null
    }),
    mounted () {
      if (localStorage.getItem("justReserved") === "true") {
        this.justReserved = true;
        localStorage.removeItem("justReserved");
      }
      if (localStorage.getItem("justReservedInformEmail") === "true") {
        this.informByEmail = true;
        localStorage.removeItem("justReservedInformEmail");
      }

      this.isFetchingReservations = true
      this.fetchReservations()
      // Keep updating reservations every 15 seconds
      this.intervalFetchReservations = setInterval(() => { this.fetchReservations()}, 15000)
    },
    methods: {
      closeModalConnectionDetails() {
        this.modalConnectionDetailsVisible = false
      },
      createReservation() {
        let hasActiveReservations = false
        this.reservations.forEach((res) => {
          if (res.status == "started" || res.status == "reserved") hasActiveReservations = true
        })

        let currentUser = this.$store.getters.user

        if (!hasActiveReservations || currentUser.role == "admin")
          this.$router.push("/user/reserve")
        else
          this.$store.commit('showMessage', { text: "You can only have one reserved or started reservation at a time. Cancel the current reservation if you need a new.", color: "red" })
      },
      fetchReservations() {
        let _this = this
        let currentUser = this.$store.getters.user
        
        axios({
          method: "get",
          url: this.AppSettings.APIServer.admin.get_reservations,
          //params: { }
          headers: {"Authorization" : `Bearer ${currentUser.loginToken}`}
        })
        .then(function (response) {
          //console.log(response)
            // Success
            if (response.data.status == true) {
              _this.reservations = response.data.data.reservations
            }
            // Fail
            else {
              console.log("Failed getting own reservations...")
              _this.$store.commit('showMessage', { text: "There was an error getting own reservations.", color: "red" })
            }
            _this.isFetchingReservations = false
        })
        .catch(function (error) {
            // Error
            if (error.response && (error.response.status == 400 || error.response.status == 401)) {
              _this.$store.commit('showMessage', { text: error.response.data.detail, color: "red" })
            }
            else {
              console.log(error)
              _this.$store.commit('showMessage', { text: "Unknown error while trying to get reservations.", color: "red" })
            }
            _this.isFetchingReservations = false
        });

        this.isFetchingReservations = false
      },
      changeEndDate(reservationId, currentEndDate) {
        let newEndDate = prompt("Enter new end date", currentEndDate);
        if (newEndDate == null || newEndDate == currentEndDate || newEndDate == "") {
          this.$store.commit('showMessage', { text: "Not changing end date.", color: "blue" })
          return;
        }
        this.$store.commit('showMessage', { text: "Changing end date.", color: "green" })

        let params = {
          "reservationId": reservationId,
          "endDate": newEndDate
        }

        let _this = this
        let currentUser = this.$store.getters.user

        axios({
          method: "post",
          url: this.AppSettings.APIServer.admin.edit_reservation,
          params: params,
          headers: {
            "Authorization" : `Bearer ${currentUser.loginToken}`
          }
        })
        .then(function (response) {
          //console.log(response)
            // Success
            if (response.data.status == true) {
              _this.$store.commit('showMessage', { text: "Reservation edited.", color: "green" })
              _this.fetchReservations()
            }
            // Fail
            else {
              console.log("Failed editing reservation...")
              console.log(response)
              let msg = response && response.data && response.data.message ? response.data.message : "There was an error editing the reservation."
              _this.$store.commit('showMessage', { text: msg, color: "red" })
            }
        })
        .catch(function (error) {
            // Error
            if (error.response && (error.response.status == 400 || error.response.status == 401)) {
              _this.$store.commit('showMessage', { text: error.response.data.detail, color: "red" })
            }
            else {
              console.log(error)
              _this.$store.commit('showMessage', { text: "Unknown error.", color: "red" })
            }
        });
      },
      cancelReservation(reservationId) {
        let result = window.confirm("Do you really want to cancel this reservation?")
        if (!result) return
        let params = {
          "reservationId": reservationId,
        }

        let _this = this
        _this.cancellingReservation = true
        let currentUser = this.$store.getters.user

        axios({
          method: "post",
          url: this.AppSettings.APIServer.reservation.cancel_reservation,
          params: params,
          headers: {
            "Authorization" : `Bearer ${currentUser.loginToken}`
          }
        })
        .then(function (response) {
          //console.log(response)
            // Success
            if (response.data.status == true) {
              _this.$store.commit('showMessage', { text: "Reservation cancelled.", color: "green" })
              _this.fetchReservations()
            }
            // Fail
            else {
              console.log("Failed removing reservation...")
              console.log(response)
              let msg = response && response.data && response.data.message ? response.data.message : "There was an error getting the hardware specs."
              _this.$store.commit('showMessage', { text: msg, color: "red" })
            }
            _this.cancellingReservation = false
        })
        .catch(function (error) {
            // Error
            if (error.response && (error.response.status == 400 || error.response.status == 401)) {
              _this.$store.commit('showMessage', { text: error.response.data.detail, color: "red" })
            }
            else {
              console.log(error)
              _this.$store.commit('showMessage', { text: "Unknown error.", color: "red" })
            }
            _this.cancellingReservation = false
        });
      },
      restartContainer(reservationId) {
        let result = window.confirm("Do you really want to restart the docker container?")
        if (!result) return
        let params = {
          "reservationId": reservationId,
        }

        let _this = this
        _this.restartingContainer = true
        let currentUser = this.$store.getters.user

        axios({
          method: "post",
          url: this.AppSettings.APIServer.reservation.restart_container,
          params: params,
          headers: {
            "Authorization" : `Bearer ${currentUser.loginToken}`
          }
        })
        .then(function (response) {
          //console.log(response)
            // Success
            if (response.data.status == true) {
              _this.$store.commit('showMessage', { text: "Container restarted succesfully.", color: "green" })
              _this.fetchReservations()
            }
            // Fail
            else {
              console.log("Failed restarting container...")
              console.log(response)
              let msg = response && response.data && response.data.message ? response.data.message : "There was an error getting the hardware specs."
              _this.$store.commit('showMessage', { text: msg, color: "red" })
            }
            _this.restartingContainer = false
        })
        .catch(function (error) {
            // Error
            if (error.response && (error.response.status == 400 || error.response.status == 401)) {
              _this.$store.commit('showMessage', { text: error.response.data.detail, color: "red" })
            }
            else {
              console.log(error)
              _this.$store.commit('showMessage', { text: "Unknown error.", color: "red" })
            }
            _this.restartingContainer = false
        });
      },
      showReservationDetails(reservationId) {
        this.modalConnectionDetailsVisible = true
        this.modalConnectionDetailsReservationId = reservationId
      }
    },
    beforeDestroy() {
      clearInterval(this.intervalFetchReservations)
    },
  }
</script>

<style scoped lang="scss">
  .loading {
    margin: 60px auto;
  }
</style>