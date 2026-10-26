DOMAIN = "webserver_status"

SENSOR = "sensor"
PLATFORMS = [SENSOR]

#Configuration 
CONF_ALIAS_VAR="webserver_name"
CONF_URL_VAR="webserver_url"
CONF_SLL_CHECK_VAR="webserver_ssl_check"
CONF_LINK_URL_VAR="webserver_link_url"
CONF_LAST_CHECK_VAR="webserver_last_check"

#Update Inteval
CONF_SCAN_INTERVAL = "ping_interval"
DEFAULT_SCAN_INTERVAL = 60

#Request Timeout
CONF_TIMEOUT = "timeout"
DEFAULT_TIMEOUT = 5
