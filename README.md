# Registries Demo

## Create

To get the current timestamp, run `date -Iseconds --utc`.

## Sign & Acknowledge

```console
$ snap sign -k <key-name> proxy-registry.json > proxy-registry.assert
$ snap ack proxy-registry.assert
```

### "cannot resolve prerequisite assertion"

```console
$ snap known --remote account account-id=<account-id> > account.assert
$ snap ack account.assert

$ snap known --remote account-key public-key-sha3-384=<key-sha-digest> > account-key.assert
$ snap ack account-key.assert
```

## Build & Install Snaps

### Custodian

```console
$ cd proxy-custodian
$ snapcraft
Packed proxy-custodian_0.1_amd64.snap

$ snap install proxy-custodian_0.1_amd64.snap --dangerous
```

### Browser

```console
$ cd browser
$ snapcraft

$ snap install browser_0.1_amd64.snap --dangerous
```

## Registries

```console
$ snap connect proxy-custodian:proxy-control
$ sudo proxy-custodian.sh -c 'snapctl set --view :proxy-control https.url=https://127.0.0.1'
$ sudo snap set f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/proxy/control-proxy 'https.bypass=["localhost","127.0.0.1"]'

$ proxy-custodian.sh -c 'snapctl get --view :proxy-control https'
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
