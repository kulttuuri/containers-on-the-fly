/* All URL addresses of the API endpoints. Used by the AppSettings.js script. */
function createUrls(baseAddress) {
    let URLS = {}
    URLS.user = {}
    URLS.reservation = {}
    URLS.admin = {}
    let baseUrl = baseAddress

    let baseUserUrl = baseUrl + "user/"
    URLS.user.login = baseUserUrl + "login"
    URLS.user.check_token = baseUserUrl + "check_token"
    
    let baseReservationUrl = baseUrl + "reservation/"
    URLS.reservation.get_available_hardware = baseReservationUrl + "get_available_hardware"
    URLS.reservation.get_current_reservations = baseReservationUrl + "get_current_reservations"
    URLS.reservation.create_reservation = baseReservationUrl + "create_reservation"
    URLS.reservation.get_own_reservations = baseReservationUrl + "get_own_reservations"
    URLS.reservation.cancel_reservation = baseReservationUrl + "cancel_reservation"
    URLS.reservation.get_own_reservation_details = baseReservationUrl + "get_own_reservation_details"
    URLS.reservation.restart_container = baseReservationUrl + "restart_container"

    let baseAdminUrl = baseUrl + "admin/"
    URLS.admin.get_reservations = baseAdminUrl + "reservations"
    URLS.admin.get_users = baseAdminUrl + "users"
    URLS.admin.get_hardware = baseAdminUrl + "hardware"
    URLS.admin.get_containers = baseAdminUrl + "containers"
    URLS.admin.get_ports = baseAdminUrl + "ports"
    URLS.admin.edit_reservation = baseAdminUrl + "edit_reservation"

    return URLS;
}

module.exports = createUrls;
//export default URLS;