# Changelog

All notable changes to the Behaverse Devices Schema are documented in this file.

## [26.0810] - 2026-08-10

### Added

- Initial release of the `devices` family: the `Device` table specifying `devices.csv` —
  one row per recording device at the dataset root, keyed by `device_id`. Groups: identity
  (`platform`, `os_version`), display (`screen_size_cm`, `screen_resolution`,
  `screen_refresh_rate`, `device_pixel_ratio`, `screen_count`), calibration (`px_per_cm`
  with method, timestamp, and `pixel_aspect_verified`), capability (`camera_present`,
  `microphone_present`, `touch_capable`, `input_devices`), and provenance
  (`screen_size_source`/`px_per_cm_source` — `auto` · `confirmed` · `calibrated` ·
  `declined` — plus `dpi_raw` for audit). Physical lengths are centimetres (÷100 maps to
  BIDS' metres). Runs link to devices via the trial family's `StudyflowLog.device_id`;
  run-lifetime facts (engine, viewing distance) deliberately stay on the run log.
