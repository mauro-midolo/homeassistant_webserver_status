# Home Assistant Webserver status Integration
[![CI](https://github.com/mauro-midolo/homeassistant_webserver_status/actions/workflows/ci.yml/badge.svg)](https://github.com/mauro-midolo/homeassistant_webserver_status/actions/workflows/ci.yml)
[![GitHub Release](https://img.shields.io/github/v/release/mauro-midolo/homeassistant_webserver_status)](https://github.com/mauro-midolo/homeassistant_webserver_status/releases/latest)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/docs/faq/custom_repositories)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=mauro-midolo_homeassistant_webserver_status&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=mauro-midolo_homeassistant_webserver_status)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=mauro-midolo_homeassistant_webserver_status&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=mauro-midolo_homeassistant_webserver_status)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=mauro-midolo_homeassistant_webserver_status&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=mauro-midolo_homeassistant_webserver_status)

[![Donate](https://img.shields.io/static/v1?label=PayPal&message=Buy%20Me%20a%20Coffee&color=green&logo=PayPal)](https://paypal.me/mauromi?country.x=IT&locale.x=it_IT)

The Home Assistant Webserver Status integration allows you to monitor the status of a specific web page or web server through HTTP or HTTPS protocols within Home Assistant.

## Features
- Monitoring the status of a web page or web server.
- Supports for HTTP and HTTPS protocols.
- Supports the deactivation of the SSL validity check
- Configurable update interval and request timeout (Integration options)
- Optional link URL (defaults to the monitored url), shown as "Visit" on the device page and as the `url` attribute of the status sensor
- When the webserver is offline, the `error` attribute of the status sensor tells why (DNS, connection, SSL, timeout)
- Integration icon and logo in Home Assistant (2026.3 or later)

## Installation
1. Install integration via HACS using "Custom repositories"
2. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Webserver Status Integration".
3. Enters the url of the server you want to monitor

## Support the project with a donation
This project is open source and free, but if you want to support us and help us continue to maintain and improve it, you can make a donation through PayPal. 
Any contribution, no matter how small, is greatly appreciated and will help us keep the project active and healthy. Thank you for your support!

[![Donate](https://img.shields.io/static/v1?label=PayPal&message=Buy%20Me%20a%20Coffee&color=green&logo=PayPal)](https://paypal.me/mauromi?country.x=IT&locale.x=it_IT)
