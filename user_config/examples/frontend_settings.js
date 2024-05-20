/**
 * Global app settings.
 */
 var AppSettings = {};

 /**
 * General settings for the app.
 */
 AppSettings.General = {
  contactEmail: "support@youremaildomain.com",
  appName: "Containers on the fly",
  timezone: "Europe/Helsinki", // https://day.js.org/docs/en/timezone/timezone
 }
 
 AppSettings.Login = {
  loginText: "Login with your credentials.",
  usernameField: "Username",
  passwordField: "Password"
 }
 
 /**
 * API urls
 */
 AppSettings.APIServer = {
  baseAddress: "http://localhost:8000/api/",
 }
 const createUrls = require("./AppUrls.js");
 AppSettings.APIServer = createUrls(AppSettings.APIServer.baseAddress);
 
 export default AppSettings;