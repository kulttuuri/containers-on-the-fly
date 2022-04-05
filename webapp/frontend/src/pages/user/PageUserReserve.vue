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
    <v-row v-if="reserveDate != null">
      <v-col cols="3" style="margin: 0 auto">
        <h2>Reservation duration</h2>
        <v-select v-model="duration" :items="reservableHours" item-text="text" item-value="value" label="Duration"></v-select>
      </v-col>
    </v-row>

    <!-- Select hardware specs & submit -->
    <!-- TODO: Loader before we fetch the available resources from the server... -->
    <v-row v-if="reserveDate != null && duration !== null" class="section">
      <v-col>
        <h2>Select Harware</h2>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import CalendarReservations from '/src/components/user/CalendarReservations.vue';
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
    },
    data: () => ({
      reserveDate: null,
      reserveType: "",
      showReservationCalendar: false,
      pickedDate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      pickedHour: {},
      reservableHours: [],
      hours: [],
      duration: null,
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
      this.pickedHour = d.getHours()
    },
    methods: {
      toggleReservationCalendar() {
        this.showReservationCalendar = !this.showReservationCalendar
      },
      reserveNow() {
        this.reserveDate = dayjs().toISOString()
        this.reserveType = "now"
        this.duration = null
      },
      reserveLater() {
        this.reserveDate = null
        this.reserveType = "pickdate"
        this.duration = null
      },
      reserveSelectedTime() {
        console.log("Reserve this..")
        let d = dayjs(this.pickedDate + " " + this.pickedHour, "YYYY-MM-DD HH")
        console.log(this.pickedDate)
        console.log(this.pickedHour)
        this.reserveDate = d.toISOString()
      },
      submitReservation() {
        console.log("IMPLEMENT: submit reservation")
        // Date picked converted to GMT+0:
        console.log(this.datePicked.tz("GMT+0"))
      },
    },
  }
</script>

<style scoped lang="scss">
  .section {
    margin-bottom: 30px;
  }
</style>