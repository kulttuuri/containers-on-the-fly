<template>
  <div>
    <a v-if="hasLongItems" class="link-toggle-read-all" @click="toggleReadAll">{{ !readAll ? "Read all" : "Read less" }}</a>
    <v-data-table
      :headers="table.headers"
      :items="data"
      :sort-by="'userId'"
      :sort-desc="true"
      class="elevation-1">
      <!-- userId -->
      <template v-slot:item.status="{item}">
        {{ item.userId }}
      </template>
      <!-- Email -->
      <template v-slot:item.startDate="{item}">
        {{ parseTime(item.startDate) }}
      </template>
      <!-- Created At -->
      <template v-slot:item.createdAt="{item}">
        {{ parseTime(item.createdAt) }}
      </template>
    </v-data-table>
  </div>
</template>

<script>
  import { DisplayTime } from '/src/helpers/time.js'

  export default {
    name: 'AdminUsersTable',
    props: {
      propItems: {
        type: Array,
        required: true,
      }
    },
    data: () => ({
      data: [],
      readAll: false,
      hasLongItems: false,
      table: {
        headers: [
          { text: 'userId', value: 'userId' },
          { text: 'email', value: 'email' },
          { text: 'createdAt', value: 'createdAt' },
          { text: 'actions', value: 'actions' },
        ],
      }
    }),
    mounted () {
      this.data = this.propItems
    },
    methods: {
      toggleReadAll() {
        this.readAll = !this.readAll;
      },
      getText(text) {
        if (this.readAll) return text;
        else {
          if (!this.hasLongItems) this.hasLongItems = true;
          return text.slice(0,10) + "...";
        }
      },
      parseTime(timestamp) {
        return DisplayTime(timestamp)
      },
    },
    watch: {
      propItems: {
        handler(newVal) {
          this.data = newVal
        },
        immediate: true,
      },
    },
  }
</script>

<style scoped lang="scss">
  .link-action {
    display: block;
    min-width: 150px;
    margin: 10px 0px;
  }

  .link-toggle-read-all {
    margin-bottom: 20px;
    font-size: 14px;
    display: inline-block;
    padding-left: 15px;
    width: auto;
  }
</style>