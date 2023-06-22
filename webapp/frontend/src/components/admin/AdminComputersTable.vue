<template>
  <div>
    <a v-if="hasLongItems" class="link-toggle-read-all" @click="toggleReadAll">{{ !readAll ? "Read all" : "Read less" }}</a>
    <v-data-table
      :headers="table.headers"
      :items="data"
      :sort-by="'computerId'"
      :sort-desc="true"
      class="elevation-1">

      <!-- Actions -->
      <template v-slot:item.actions="{item}">
        <a class="link-action" @click="emitEditComputer(item.computerId)">Edit Computer</a>
        <a class="link-action" @click="emitRemoveComputer(item.computerId)">Remove Computer</a>
      </template>
    </v-data-table>
  </div>
</template>

<script>
  import { DisplayTime } from '/src/helpers/time.js'

  export default {
    name: 'AdminComputersTable',
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
          { text: 'Computer ID', value: 'computerId' },
          { text: 'Public', value: 'public' },
          { text: 'name', value: 'name' },
          { text: 'IP', value: 'ip' },
          { text: 'Created At', value: 'createdAt' },
          { text: 'Updated At', value: 'updatedAt' },
          { text: 'Actions', value: 'actions' },
        ],
      }
    }),
    mounted () {
      this.data = this.propItems
    },
    methods: {
      emitEditComputer(computerId) {
        this.$emit('emitEditComputer', computerId)
      },
      emitRemoveComputer(computerId) {
        this.$emit('emitRemoveComputer', computerId)
      },
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