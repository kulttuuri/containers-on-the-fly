<template>
  <v-data-table
    :headers="table.headers"
    :items="reservations"
    :sort-by="'createdAt'"
    :sort-desc="true"
    class="elevation-1">
    <!-- Status -->
    <template v-slot:item.status="{item}">
      <v-chip :color="getStatusColor(item.status)">{{item.status}}</v-chip>
    </template>
    <!-- Reserve date -->
    <template v-slot:item.createdAt="{item}">
      {{ parseTime(item.createdAt) }}
    </template>
    <!-- Start date -->
    <template v-slot:item.startDate="{item}">
      {{ parseTime(item.startDate) }}
    </template>
    <!-- End date -->
    <!-- Start date -->
    <template v-slot:item.endDate="{item}">
      {{ parseTime(item.endDate) }}
    </template>
    <!-- Actions -->
    <template v-slot:item.actions="{item}">
      <a v-if="item.status == 'reserved' || item.status == 'started'" @click="emitCancelReservation(item.reservationId)">Cancel Reservation</a>
    </template>
  </v-data-table>
</template>

<script>
  import { DisplayTime } from '/src/helpers/time.js'

  export default {
    name: 'UserReservationTable',
    props: {
      propReservations: {
        type: Array,
        required: true,
      }
    },
    data: () => ({
      reservations: [],
      cancellingReservation: false,
      table: {
        headers: [
          {
            text: 'Status',
            align: 'start',
            sortable: false,
            value: 'status',
          },
          { text: 'Reserved', value: 'createdAt' },
          { text: 'Starts', value: 'startDate' },
          { text: 'Ends', value: 'endDate' },
          { text: 'actions', value: 'actions' },
        ],
      }
    }),
    mounted () {
      this.reservations = this.propReservations
    },
    methods: {
      emitCancelReservation(reservationId) {
        this.$emit('emitCancelReservation', reservationId)
      },
      getStatusColor(status) {
        if (status == "reserved") return "primary"
        else if (status == "started") return "green"
        else if (status == "stopped") return "red"
      },
      parseTime(timestamp) {
        return DisplayTime(timestamp)
      },
    },
    watch: {
      propReservations: {
        handler(newVal) {
          this.reservations = newVal
        },
        immediate: true,
      },
    },
  }
</script>

<style scoped lang="scss">
</style>