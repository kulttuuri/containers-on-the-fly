import Vue from 'vue'
import Vuex from 'vuex'
const axios = require('axios').default;
import AppSettings from '/src/AppSettings.js';

Vue.use(Vuex);

/* Usage of getters (nextTick is only necessary if wanting to pause execution of the component):

  this.$nextTick(function () {
    _this.$store.commit("setUser", { loginToken: loginToken, callback: (res) => {
      if (res.success)
        {
          console.log("Login succesfull..")
        }
        else
        {
          console.log("Could not login user with the given loginToken.")
        }
      }
    });
  });
*/

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
      timeout: 7000, // Default timeout for snackbars
      multiline: false, // Is this multiline, automatically set below
    },
    initializing: true, // Set to false after we have initialized the app / store
    // Information about the currently logged-in user
    user: {
      loginToken: "",
      email: "",
      role: "",
      loggedinAt: null
    }
  },
  // ###########
  // # GETTERS #
  // ###########
  getters: {
    // Gets current user data or null
    user: state => {
      return state.user || null
    },
    // Check if user is logged in or not, only in clientside
    isLoggedIn: state => {
      if (state.user && state.user.loginToken) return true
      else return false
    },
    // true if we are loading the app, false otherwise
    isInitializing: state => {
      return state.initializing
    },
  },
  // #############
  // # MUTATIONS #
  // #############
  mutations: {
    // eslint-disable-next-line
    initialiseStore(state, payload) {
      // Apply all permanent localStorage items to store here
      try {
        let user = localStorage.getItem("user")
        if (user) {
          user = JSON.parse(user)
          this.commit("setUser", {
            "loginToken": user.loginToken,
            "email": user.email,
            "role": user.role,
            "loggedinAt": user.loggedinAt
          });
        }
        else {
          state.initializing = false
        }
      }
      // eslint-disable-next-line
      catch (e) {
        console.log("Error parsing initializeStore items:", e)
      }
    },
    // Sets currently logged-in user data
    setUser(state, payload) {
      if (!payload.callback) payload.callback = () => { };

      if (!payload.loginToken) return payload.callback(Response(false, "loginToken was missing"));
      let _this = this;
      
      axios({
        method: "get",
        url: AppSettings.APIServer.user.check_token,
        headers: {"Authorization" : `Bearer ${payload.loginToken}`}
      })
      .then(function (response) {
          // Success
          if (response.data.status == true) {
            state.user.loginToken = payload.loginToken
            state.user.email = response.data.data.email
            state.user.role = response.data.data.role
            state.user.loggedinAt = new Date()
            localStorage.setItem("user", JSON.stringify(state.user))
            if (state.initializing) state.initializing = false
            return payload.callback(Response(true, "Login token OK!"));
          }
          // Fail
          else {
            console.log("Invalid token – logging user out.")
            _this.commit("logoutUser")
            if (state.initializing) state.initializing = false
            return payload.callback(Response(false, "Invalid login token."));
          }
      })
      .catch(function (error) {
          // Error
          if (error.response && error.response.status == 400) {
            return payload.callback(Response(false, error.response.data.detail));
          }
          // Unauthorized
          else if (error.response && error.response.status == 401) {
            console.log("Unauthorized – Logging user out.")
            _this.commit("logoutUser")
            if (state.initializing) state.initializing = false
            return payload.callback(Response(false, "Invalid login token."));
          }
          else {
            console.log(error)
            return payload.callback(Response(false, "Unknown error."));
          }
      });

      /*state.user.token = payload.loginToken
      state.user.email = payload.email
      localStorage.setItem("user", state.user)
      payload.callback(Response(true, "User details updated.", { "user": state.user }));*/
    },
    // Logs out the currently logged-in user, if any.
    logoutUser(state, payload) {
      if (payload && !payload.callback) payload.callback = () => { };
      state.user.loginToken = ""
      state.user.email = ""
      state.user.loggedinAt = ""
      localStorage.removeItem("user")
      payload.callback(Response(true, "User logged out succesfully", {  }));
    },
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

// ###################
// # LOCAL FUNCTIONS #
// ###################

// For generating callback responses from mutations
function Response(success, message, ...extraObjects) {
  if (success === undefined) { console.log("success on vaadittu kenttä Staten responselle."); return undefined; }
  if (!message) { console.log("message on vaadittu kenttä Staten responselle."); return undefined; }

  let returnObj = {
    success,
    message,
    "responseCreatedAt": new Date()
  }
  if (extraObjects && extraObjects != null && typeof extraObjects === 'object' && Object.keys(extraObjects).length > 0) {
    returnObj.data = extraObjects[0];
  }
  return returnObj;
}