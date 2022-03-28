import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

// Global VUEX store
export const store = new Vuex.Store({
  // ##########
  // # STATES #
  // ##########
  state: {
    // For global snackbar (message) component
    snackbar: {
      text: null, // Text for snackbar
      color: "primary", // Color for snackbar
      visible: false, // Is the snackbar visible
      close: false, // Does user see close button
      timeout: 5000, // Default timeout for snackbars
      multiline: false, // Is this multiline, automatically set below
    },
  },
  // ###########
  // # GETTERS #
  // ###########
  getters: {

  },
  // #############
  // # MUTATIONS #
  // #############
  mutations: {
    // Shows global snackbar message
    showMessage(state, payload) {
      state.snackbar.text = payload.text;
      state.snackbar.color = payload.color || "primary";
      state.snackbar.close = payload.close || false;
      state.snackbar.multiline = (payload.text.length > 50) ? true : false;

      if (payload.multiline) {
        state.snackbar.multiline = payload.multiline;
      }

      if (payload.timeout) {
        state.snackbar.timeout = payload.timeout;
      }

      state.snackbar.visible = true;
    },
    // Closes global snackbar message
    closeMessage(state) {
      state.snackbar.visible = false;
      state.snackbar.multiline = false;
      state.snackbar.timeout = 5000;
      state.snackbar.text = null;
    },
  },
})