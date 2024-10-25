# Registries Demo

## Create

### Manually

To get the current timestamp, run `date -Iseconds --utc`.

#### Sign & Acknowledge

```console
$ snap sign -k <key-name> proxy-registry.json > proxy-registry.assert
$ snap ack proxy-registry.assert
```

##### "cannot resolve prerequisite assertion"

```console
$ snap known --remote account account-id=<account-id> > /tmp/account.assert
$ snap ack /tmp/account.assert

$ snap known --remote account-key public-key-sha3-384=<key-sha-digest> > /tmp/account-key.assert
$ snap ack /tmp/account-key.assert
```

### With Snapcraft

...

## Build & Install Snaps

### Net-Ctrl

```console
$ cd net-ctrl
$ snapcraft
Packed net-ctrl_0.1_amd64.snap

$ snap install net-ctrl_0.1_amd64.snap --dangerous
net-ctrl 0.1 installed
```

### Browser

```console
$ cd browser
$ snapcraft
Packed browser_0.1_amd64.snap

$ snap install browser_0.1_amd64.snap --dangerous
browser 0.1 installed
```

## Registries

```console
$ snap connect net-ctrl:proxy-control
$ snap connections net-ctrl
Interface  Plug                    Slot       Notes
registry   net-ctrl:proxy-control  :registry  manual

$ snap connect browser:proxy-observe
$ snap connections browser
Interface  Plug                   Slot       Notes
network    browser:network        :network   -
registry   browser:proxy-observe  :registry  manual

$ sudo net-ctrl.sh -c 'snapctl set --view :proxy-control https.url=http://proxy.example.com'
$ sudo net-ctrl.sh -c 'snapctl set --view :proxy-control ftp.url=ftp://proxy.example.com'
$ sudo snap set f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/proxy/control-proxy 'https.bypass=["https://127.0.0.1", "https://localhost"]'

$ net-ctrl.sh -c 'snapctl get --view :proxy-control https'
{
    "ftp": {
        "url": "ftp://proxy.example.com"
    },
    "https": {
        "bypass": [
            "https://127.0.0.1",
            "https://localhost"
        ],
        "url": "http://proxy.example.com"
    }
}
```

## Proxy

```console
$ docker run -d --name squid-container -e TZ=UTC -p 3128:3128 ubuntu/squid:5.2-22.04_beta
$ docker logs -f squid-container
[...]
1729879108.361   2812 172.17.0.1 TCP_TUNNEL/200 5435 CONNECT example.com:443 - HIER_DIRECT/93.184.215.14 -
1729879154.849   1618 172.17.0.1 TCP_TUNNEL/200 5458 CONNECT example.com:443 - HIER_DIRECT/93.184.215.14 -
```
