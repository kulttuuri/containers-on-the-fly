<template>
  <v-container class="text-center">
    <v-row>
      <v-col>
        <h1>Reserve Server</h1>
      </v-col>
    </v-row>

  <v-row>
    <v-col class="section">
      <a color="primary" style="margin-bottom: 20px" @click="toggleReservationCalendar">
        {{ !showReservationCalendar ? "Show" : "Hide" }} Reservation Calendar
      </a>
      <CalendarReservations v-if="showReservationCalendar" />
    </v-col>
  </v-row>

    <!-- Reserve now or for later? -->
    <v-row class="section">
      <v-col cols="12">
        <h2>When do you need the server?</h2>
      </v-col>
      <v-col cols="12">
        <v-btn :color="reserveType == 'now' ? 'success' : 'primary'" style="margin: 0px 10px" @click="reserveNow">Reserve Now</v-btn>
        <v-btn :color="reserveType == 'pickdate' ? 'success' : 'primary'" @click="reserveLater">Reserve for later</v-btn>
      </v-col>
    </v-row>

    <!-- Pick a Date -->
    <v-row v-if="reserveType == 'pickdate'" class="section">
      <v-row justify="center">
        <v-col cols="12">
          <h2>Pick a date and time</h2>
        </v-col>

        <v-col cols="4">
          <v-date-picker value="" v-model="pickedDate" :min="new Date().toISOString().substr(0, 10)"></v-date-picker>
        </v-col>
        <v-col cols="3">
          <v-select v-model="pickedHour" :items="hours" item-text="text" item-value="value" label="Starting Hour"></v-select>
          <v-btn color="primary" @click="reserveSelectedTime">Select this day and time</v-btn>
        </v-col>
      </v-row>
      <!--<v-btn color="primary" @click="reserveLater">Reserve for later</v-btn>-->
    </v-row>

    <!-- For how long -->
    <v-row v-if="reserveDate != null" class="section">
      <v-col cols="3" style="margin: 0 auto">
        <h2>Reservation duration</h2>
        <v-select v-model="reserveDuration" :items="reservableHours" item-text="text" item-value="value" label="Duration"></v-select>
      </v-col>
    </v-row>

    <!-- Get available computers and resources -->
    <v-row v-if="reserveDate != null && reserveDuration" class="section">
      <v-col cols="12">
        <v-btn color="primary" @click="fetchAvailableHardware">Get available computers and hardware</v-btn>
      </v-col>
    </v-row>

    <!-- Loading computers and their hardware specs... -->
    <v-row v-if="reserveDate && reserveDuration && fetchingComputers" class="section">
      <v-col>
        <Loading />
      </v-col>
    </v-row>

    <!-- Select container -->
    <v-row v-if="reserveDate != null && reserveDuration !== null && !fetchingComputers && allComputers">
      <v-col cols="12">
        <h2>Select Container</h2>
        <v-row>
          <v-col cols="3" style="margin: 0 auto">
            <v-select v-model="container" :items="containers" item-text="text" item-value="value" label="Container"></v-select>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- Select computer, hardware specs & submit -->
    <v-row v-if="reserveDate != null && reserveDuration !== null && !fetchingComputers && allComputers && container" class="section">      
      <v-col cols="12">
        <h2>Select Computer</h2>
        <v-row>
          <v-col cols="3" style="margin: 0 auto">
            <v-select v-model="computer" v-on:change="computerChanged" :items="computers" item-text="text" item-value="value" label="Computer"></v-select>
          </v-col>
        </v-row>
      </v-col>

      <v-row v-if="computer && hardwareData">
        <v-col cols="12">
          <h2>Select Hardware</h2>
          <v-row v-for="spec in hardwareData" :key="spec.name" class="spec-row">
            <v-col cols="12">
              <h3>{{ spec.type }}</h3>
            </v-col>
            <v-col cols="6" style="margin: 0 auto">
              <v-slider :min="spec.minimumAmount" :thumb-size="60" ticks="always" v-model="selectedHardwareSpecs[spec.hardwareSpecId]" :max="spec.maximumAmountForUser" thumb-label="always">
                <template v-slot:thumb-label="{ value }">
                  {{ value + " " + spec.format }}
                </template>
              </v-slider>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-row>

    <v-row v-if="computer && hardwareData">
      <v-col cols="12">
        <v-btn color="primary" @click="submitReservation">Create Reservation</v-btn>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
  import CalendarReservations from '/src/components/user/CalendarReservations.vue';
  import Loading from '/src/components/global/Loading.vue';

  const axios = require('axios').default;
  import dayjs from "dayjs";
  var utc = require('dayjs/plugin/utc')
  var timezone = require('dayjs/plugin/timezone')
  var customParseFormat = require('dayjs/plugin/customParseFormat')
  dayjs.extend(utc)
  dayjs.extend(timezone)
  dayjs.extend(customParseFormat)

  export default {
    name: 'PageUserReserve',
    components: {
      CalendarReservations,
      Loading,
    },
    data: () => ({
      reserveDate: null,
      reserveType: "",
      showReservationCalendar: false,
      pickedDate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      pickedHour: {},
      reservableHours: [],
      hours: [],
      reserveDuration: null,
      fetchingComputers: false, // True if we are fetching computers and their hardware data from the server
      allComputers: null, // Contains all computers from server and their hardware data
      allContainers: null, // Contains all containers from server and their hardware data
      computer: null, // Model for the currently selected computer dropdown
      computers: null, // Contains a list of all computer items for the computer dropdown
      container: null, // Model for the currently selected container dropdown
      containers: null, // Contains a list of all container items for the container dropdown
      hardwareData: null, // Contains hardware data for the currently selected computer
      selectedHardwareSpecs: {}, // Selected hardware specs for the current computer
      isSubmittingReservation: false, // Set to true when user is submitting the reservation
    }),
    mounted() {
      let d = new Date()

      let hours = []
      for (let i = 1; i < 72; i++) {
        hours.push( { "text": i + " hours", "value": i } )
      }
      this.reservableHours = hours
      //this.duration = { "text": "8 hours", "value": 8 }

      let dayHours = []
      for (let i = 0; i < 24; i++) {
        let current = i < 10 ? "0" + i : i
        dayHours.push( { "text": i + ":00", "value": current } )
      }
      this.hours = dayHours
      this.pickedHour = d.getHours() < 10 ? "0"+d.getHours() : d.getHours.toString()
    },
    methods: {
      computerChanged() {
        let currentComputerId = this.computer
        let data = null
        this.allComputers.forEach((comp) => {
          if (comp.computerId == currentComputerId) data = comp.hardwareSpecs
        })
        this.hardwareData = data
        
        // Set default values for hardware specs
        let selectedHardwareSpecs = {}
        this.hardwareData.forEach((spec) => {
          selectedHardwareSpecs[spec.hardwareSpecId] = spec.defaultAmountForUser
        })
        this.selectedHardwareSpecs = selectedHardwareSpecs
      },
      toggleReservationCalendar() {
        this.showReservationCalendar = !this.showReservationCalendar
      },
      reserveNow() {
        this.reserveDate = dayjs().toISOString()
        this.reserveType = "now"
        this.reserveDuration = null
      },
      reserveLater() {
        this.reserveDate = null
        this.reserveType = "pickdate"
        this.reserveDuration = null
      },
      reserveSelectedTime() {
        if (!this.pickedDate) return this.$store.commit('showMessage', { text: "Please select day.", color: "red" })
        if (!this.pickedHour) return this.$store.commit('showMessage', { text: "Please select hour.", color: "red" })
        let d = dayjs(this.pickedDate + " " + this.pickedHour, "YYYY-MM-DD HH")
        this.reserveDate = d.toISOString()
      },
      fetchAvailableHardware() {
        this.fetchingComputers = true
        let _this = this
        this.computer = null
        let currentUser = this.$store.getters.user
        
        axios({
          method: "get",
          url: this.AppSettings.APIServer.reservation.get_available_hardware,
          params: { "date": dayjs(this.reserveDate).tz("GMT+0").toISOString() },
          headers: {"Authorization" : `Bearer ${currentUser.loginToken}`}
        })
        .then(function (response) {
          //console.log(response)
            // Success
            if (response.data.status == true) {
              _this.allComputers = response.data.data.computers
              _this.allContainers = response.data.data.containers
              let computers = []
              _this.allComputers.forEach((computer) => {
                computers.push({ "value": computer.computerId, "text": computer.name })
              });
              _this.computers = computers
              
              let containers = []
              _this.allContainers.forEach((container) => {
                containers.push({ "value": container.containerId, "text": container.name })
              });
              _this.containers = containers
            }
            // Fail
            else {
              console.log("Failed getting hardware data...")
              _this.$store.commit('showMessage', { text: "There was an error getting the hardware specs.", color: "red" })
            }
            _this.fetchingComputers = false
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
            _this.fetchingComputers = false
        });
      },
      submitReservation() {
        this.isSubmittingReservation = true
        let _this = this
        let currentUser = this.$store.getters.user
        let computerId = this.computer
        console.log("selected computerId: ", this.computer)
        console.log("selected containerId: ", this.container)
        console.log("Selected hardware specs", {...this.selectedHardwareSpecs})
        console.log("Duration:", this.reserveDuration)
        let params = {
          "date": dayjs(this.reserveDate).tz("GMT+0").toISOString(),
          "computerId": computerId,
          "duration": this.reserveDuration,
          "containerId": this.container,
          "hardwareSpecs": {...this.selectedHardwareSpecs}
        }

        axios({
          method: "post",
          url: this.AppSettings.APIServer.reservation.create_reservation,
          params: params,
          headers: {
            "Authorization" : `Bearer ${currentUser.loginToken}`,
            "Content-Type": "multipart/form-data"
            }
        })
        .then(function (response) {
          //console.log(response)
            // Success
            if (response.data.status == true) {
              _this.allComputers = response.data.data.computers
              let computers = []
              _this.allComputers.forEach((computer) => {
                computers.push({ "value": computer.computerId, "text": computer.name })
              });
              _this.computers = computers
            }
            // Fail
            else {
              console.log("Failed getting hardware data...")
              _this.$store.commit('showMessage', { text: "There was an error getting the hardware specs.", color: "red" })
            }
            _this.fetchingComputers = false
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
            _this.fetchingComputers = false
        });
      },
    },
  }
</script>

<style scoped lang="scss">
  .section {
    margin-bottom: 50px;
  }

  h2 {
    margin-bottom: 10px;
  }
  
  .spec-row {
    margin-bottom: 10px;
  }
</style>