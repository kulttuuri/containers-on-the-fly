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
const axios = require('axios').default;

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
      let _this = this;
      let currentUser = this.$store.getters.user;

      axios({
        method: "get",
        url: this.AppSettings.APIServer.admin.get_group,
        params: { groupId: groupId },
        headers: { "Authorization": `Bearer ${currentUser.loginToken}` }
      })
      .then(function (response) {
        if (response.data.status == true) {
          _this.group = response.data.data.group;
        } else {
          console.log("Failed fetching group data...");
          _this.$store.commit('showMessage', { text: "There was an error fetching group data.", color: "red" });
        }
      })
      .catch(function (error) {
        if (error.response && (error.response.status == 400 || error.response.status == 401)) {
          _this.$store.commit('showMessage', { text: error.response.data.detail, color: "red" });
        } else {
          console.log(error);
          _this.$store.commit('showMessage', { text: "Unknown error.", color: "red" });
        }
      });
    },
    fetchUsers() {
      let _this = this;
      let currentUser = this.$store.getters.user;

      axios({
        method: "get",
        url: this.AppSettings.APIServer.admin.get_users,
        headers: { "Authorization": `Bearer ${currentUser.loginToken}` }
      })
      .then(function (response) {
        if (response.data.status == true) {
          _this.users = response.data.data.users;
        } else {
          console.log("Failed fetching users data...");
          _this.$store.commit('showMessage', { text: "There was an error fetching users data.", color: "red" });
        }
      })
      .catch(function (error) {
        if (error.response && (error.response.status == 400 || error.response.status == 401)) {
          _this.$store.commit('showMessage', { text: error.response.data.detail, color: "red" });
        } else {
          console.log(error);
          _this.$store.commit('showMessage', { text: "Unknown error.", color: "red" });
        }
      });
    },
    close() {
      this.dialog = false;
      this.$emit('emitModalClose');
    },
    save() {
      let _this = this;
      let currentUser = this.$store.getters.user;
      let apiEndpoint = this.isNew ? this.AppSettings.APIServer.admin.add_group : this.AppSettings.APIServer.admin.edit_group;
      let params = this.isNew ? { name: this.group.name } : { groupId: this.propData, name: this.group.name, members: this.group.members };

      axios({
        method: "post",
        url: apiEndpoint,
        params: params,
        headers: { "Authorization": `Bearer ${currentUser.loginToken}` }
      })
      .then(function (response) {
        if (response.data.status == true) {
          _this.$store.commit('showMessage', { text: "Group saved.", color: "green" });
          _this.dialog = false;
          _this.$emit('emitModalClose');
        } else {
          console.log("Failed saving group...");
          _this.$store.commit('showMessage', { text: "There was an error saving the group.", color: "red" });
        }
      })
      .catch(function (error) {
        if (error.response && (error.response.status == 400 || error.response.status == 401)) {
          _this.$store.commit('showMessage', { text: error.response.data.detail, color: "red" });
        } else {
          console.log(error);
          _this.$store.commit('showMessage', { text: "Unknown error.", color: "red" });
        }
      });
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
</style>
