from datetime import timedelta
import logging

DOMAIN = "evonic"
BRAND = "Evonic Fires"
LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=30)
EFFECTS_REFRESH_INTERVAL = timedelta(hours=1)
CONF_TEMP_OFFSET = "temp_offset"
