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
$ snap known --remote account account-id=<account-id> > account.assert
$ snap ack account.assert

$ snap known --remote account-key public-key-sha3-384=<key-sha-digest> > account-key.assert
$ snap ack account-key.assert
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

$ sudo net-ctrl.sh -c 'snapctl set --view :proxy-control https.url=https://127.0.0.1'
$ sudo snap set f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/proxy/control-proxy 'https.bypass=["localhost","127.0.0.1"]'

$ net-ctrl.sh -c 'snapctl get --view :proxy-control https'
```

## Miscellaneous

```json
{
    "storage": {
        "aliases":  {
            "protocol": {
                "type": "string",
                "choices": [
                    "http",
                    "https",
                    "ftp"
                ]
            }
        },
        "schema": {
            "config": {
                "keys": "$protocol",
                "values": {
                    "schema": {
                    "url": "string",
                        "bypass": {
                            "type": "array",
                            "unique": true,
                            "values": "string"
                        }
                    }
                }
            }
        }
    }
}
```
