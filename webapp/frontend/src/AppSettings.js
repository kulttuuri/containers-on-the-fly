/**
 * Global app settings.
 */
 var AppSettings = {};

 /**
 * General settings for the app.
 */
AppSettings.General = {
  contactEmail: "support@aiserver.samk.com",
  appName: "SAMK Virtual AI Lab",
  timezone: "Europe/Helsinki", // https://day.js.org/docs/en/timezone/timezone
}

AppSettings.Login = {
  loginText: "Use your student credentials to login (not email)",
  usernameField: "Username (Student ID)",
  passwordField: "Password"
}

/**
 * API urls
 */
AppSettings.APIServer = {
  baseAddress: "http://localhost:8000/api/",
}
AppSettings.APIServer.user = {}
AppSettings.APIServer.reservation = {}
let baseUrl = AppSettings.APIServer.baseAddress
let baseUserUrl = baseUrl + "user/"
AppSettings.APIServer.user.login = baseUserUrl + "login"
AppSettings.APIServer.user.check_token = baseUserUrl + "check_token"
let baseReservationUrl = baseUrl + "reservation/"
AppSettings.APIServer.reservation.get_available_hardware = baseReservationUrl + "get_available_hardware"
AppSettings.APIServer.reservation.get_current_reservations = baseReservationUrl + "get_current_reservations"
AppSettings.APIServer.reservation.create_reservation = baseReservationUrl + "create_reservation"
AppSettings.APIServer.reservation.get_own_reservations = baseReservationUrl + "get_own_reservations"
AppSettings.APIServer.reservation.cancel_reservation = baseReservationUrl + "cancel_reservation"

export default AppSettings;