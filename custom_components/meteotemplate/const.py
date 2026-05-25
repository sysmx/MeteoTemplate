"""Constants for the Meteotemplate integration."""

DOMAIN = "meteotemplate"

DEFAULT_NAME = "Meteotemplate"
# Seconds. The DB behind Meteotemplate typically updates every ~5 min,
# so polling faster than ~60s just hammers your neighbour's server for nothing.
DEFAULT_SCAN_INTERVAL = 120
MIN_SCAN_INTERVAL = 30
