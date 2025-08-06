# TrueNAS Pushover Adapter

Adaptation of ZTube's [TrueNAS Gotify Adapter](https://github.com/ZTube/truenas-gotify-adapter). TrueNAS does not natively provide a way to send alerts and notifications to Pushover. This repo uses the TrueNAS Slack alert integration and provides a fake slack webhook endpoint to forward alerts to a Pushover server.

Note that Slack is not required at all for this integration to work.

## Installation
1. Apps -> Discover Apps -> Custom App
    - Enter an Application Name, e.g. "truenas-pushover-adapter"
    - _Image Repository_: ghcr.io/ztube/truenas-pushover-adapter
    - _Image Tag_: main
    - Environment Variables:
        - _Name_: APPLICATION\_TOKEN
        - _Value_: [your pushover application token] e.g. F32ijd932hD2
        - _Name_: USER\_KEY
        - _Value_: [your pushover user key] e.g. cGVla2Fib29v

    - Network Configuration: 
        - Check _"Host Network"_
    - Save

OR

1. Apps -> Discover Apps -> Custom App -> Install via YAML
```yaml
services:
  truenas-pushover-adapter:
    container_name: truenas-pushover-adapter
    image: ghcr.io/savagerose/truenas-pushover-adapter:main
    restart: unless-stopped
    environment:
      - APPLICATION_TOKEN=<your pushover application token> # e.g. F32ijd932hD2
      - USER_KEY=<your pushover user or group key> # e.g. cGVla2Fib29v
    network_mode: host
```

1. System -> Alert Settings -> Add
    - _Type_: Slack
    - _Webhook URL_: http://localhost:31662
    - Click _Send Test Alert_ to test the connection
    - Save
