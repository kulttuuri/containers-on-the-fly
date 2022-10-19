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
    <template v-slot:item.endDate="{item}">
      {{ parseTime(item.endDate) }}
    </template>
    <!-- Resources -->
    <template v-slot:item.resources="{item}">
      {{ getResources(item.reservedHardwareSpecs) }}
    </template>
    <!-- Container Status -->
    <template v-slot:item.containerStatus="{item}">
      {{ item.reservedContainer.containerStatus }}
    </template>
    <!-- Actions -->
    <template v-slot:item.actions="{item}">
      <a class="link-action" v-if="item.status == 'reserved' || item.status == 'started'" @click="emitCancelReservation(item.reservationId)">Cancel Reservation</a>
      <a v-if="item.status == 'started'" @click="emitShowReservationDetails(item.reservationId)">Show Details</a>
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
          { text: 'Resources', value: 'resources' },
          { text: 'Container Status', value: 'containerStatus' },
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
      emitShowReservationDetails(reservationId) {
        this.$emit('emitShowReservationDetails', reservationId)
      },
      getStatusColor(status) {
        if (status == "reserved") return "primary"
        else if (status == "started") return "green"
        else if (status == "stopped") return "red"
      },
      parseTime(timestamp) {
        return DisplayTime(timestamp)
      },
      getResources(specs) {
        if (specs) {
          let resources = ""
          for (let i = 0; i < specs.length; i++) {
            resources += specs[i].amount + " " + specs[i].format
            if (i != specs.length - 1) resources += ", "
          }
          return resources
        }
        return ""
      }
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
  .link-action {
    margin: 0px 15px;
  }
</style>