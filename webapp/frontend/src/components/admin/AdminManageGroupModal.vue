<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">{{ isNew ? 'Create Group' : 'Edit Group' }}</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="group.name" label="Group Name"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="group.members"
                :items="users"
                item-text="email"
                item-value="userId"
                label="Group Members"
                multiple
                chips
                deletable-chips
              ></v-select>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'AdminManageGroupModal',
  props: {
    propData: {
      type: [Object, String],
      required: true,
    },
  },
  data: () => ({
    dialog: false,
    group: {
      name: '',
      members: [],
    },
    users: [],
    isNew: false,
  }),
  watch: {
    propData: {
      handler(newVal) {
        if (newVal === 'new') {
          this.isNew = true;
          this.group = { name: '', members: [] };
        } else {
          this.isNew = false;
          this.fetchGroup(newVal);
        }
        this.dialog = true;
      },
      immediate: true,
    },
  },
  methods: {
    fetchGroup(groupId) {
      // Fetch group data from backend
      // This is a placeholder, replace with actual API call
      this.group = {
        name: 'Example Group',
        members: [1, 2],
      };
    },
    fetchUsers() {
      // Fetch users data from backend
      // This is a placeholder, replace with actual API call
      this.users = [
        { userId: 1, email: 'user1@example.com' },
        { userId: 2, email: 'user2@example.com' },
      ];
    },
    close() {
      this.dialog = false;
      this.$emit('emitModalClose');
    },
    save() {
      // Save group data to backend
      // This is a placeholder, replace with actual API call
      this.dialog = false;
      this.$emit('emitModalClose');
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
</style>
