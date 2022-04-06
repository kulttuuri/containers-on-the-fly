/**
 * Global app settings.
 */
 var AppSettings = {};

 /**
 * General settings for the app.
 */
AppSettings.General = {
  contactEmail: "support@aiserver.samk.com"
}

AppSettings.APIServer = {
  baseAddress: "http://localhost:8000/api/",
}
AppSettings.APIServer.user = {}
AppSettings.APIServer.reservation = {}
let baseUrl = AppSettings.APIServer.baseAddress
AppSettings.APIServer.user.login = baseUrl + "user/login"
AppSettings.APIServer.user.check_token = baseUrl + "user/check_token"
AppSettings.APIServer.reservation.get_available_hardware = baseUrl + "reservation/get_available_hardware"
AppSettings.APIServer.reservation.create_reservation = baseUrl + "reservation/create_reservation"

export default AppSettings;