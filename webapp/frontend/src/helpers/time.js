import dayjs from "dayjs";
var utc = require('dayjs/plugin/utc')
var timezone = require('dayjs/plugin/timezone')
dayjs.extend(utc)
dayjs.extend(timezone)
import AppSettings from '/src/AppSettings.js'

/**
 * Returns the given timestamp in application's timezone and parses it in human-readable format.
 * Example return: "04.02.2022 12:23"
 */
function DisplayTime(timestamp) {
  // Add UTC +0 abbreviation to end of the timestamp if it is already not there
  if (timestamp.slice(-1) !== "Z") timestamp = timestamp + "Z"
  // Parse to current timezone
  let time = dayjs(timestamp).tz(AppSettings.General.timezone)
  return time.format("DD.MM.YYYY HH:mm")
}

export { DisplayTime }