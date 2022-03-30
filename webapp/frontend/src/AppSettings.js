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
let baseUrl = AppSettings.APIServer.baseAddress
AppSettings.APIServer.user.login = baseUrl + "user/login"
AppSettings.APIServer.user.check_token = baseUrl + "user/check_token"

export default AppSettings;