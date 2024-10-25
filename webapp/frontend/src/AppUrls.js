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
    URLS.reservation.extend_reservation = baseReservationUrl + "extend_reservation"

    let baseAdminUrl = baseUrl + "admin/"
    URLS.admin.get_reservations = baseAdminUrl + "reservations"
    URLS.admin.get_users = baseAdminUrl + "users"
    URLS.admin.get_hardware = baseAdminUrl + "hardware"
    URLS.admin.get_containers = baseAdminUrl + "containers"
    URLS.admin.get_computers = baseAdminUrl + "computers"
    URLS.admin.get_computer = baseAdminUrl + "computer"
    URLS.admin.get_container = baseAdminUrl + "container"
    URLS.admin.save_container = baseAdminUrl + "save_container"
    URLS.admin.save_computer = baseAdminUrl + "save_computer"
    URLS.admin.remove_container = baseAdminUrl + "remove_container"
    URLS.admin.remove_computer = baseAdminUrl + "remove_computer"
    URLS.admin.get_ports = baseAdminUrl + "ports"
    URLS.admin.edit_reservation = baseAdminUrl + "edit_reservation"
    URLS.admin.get_groups = baseAdminUrl + "groups"
    URLS.admin.add_group = baseAdminUrl + "add_group"
    URLS.admin.remove_group = baseAdminUrl + "remove_group"
    URLS.admin.edit_group = baseAdminUrl + "edit_group"
    URLS.admin.add_user_to_group = baseAdminUrl + "add_user_to_group"
    URLS.admin.remove_user_from_group = baseAdminUrl + "remove_user_from_group"

    return URLS;
}

module.exports = createUrls;
//export default URLS;
