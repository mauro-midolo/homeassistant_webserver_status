DOMAIN = "webserver_status"

SENSOR = "sensor"
PLATFORMS = [SENSOR]

#Configuration 
CONF_ALIAS_VAR="webserver_name"
CONF_URL_VAR="webserver_url"
CONF_SLL_CHECK_VAR="webserver_ssl_check"

#Update Inteval
CONF_SCAN_INTERVAL = "ping_interval"
DEFAULT_SCAN_INTERVAL = 60