# A Registries* Demo

> *registries might be renamed

Turn on registries: `snap set system experimental.registries=true`

## Create

You can create a registry assertion manually where you sign it itself or you can use `snapcraft` which gives you an editor, signs the assertion, & uploads it to the Store.

### Manually

Create a `network-registry.json` file and put your assertion there.

The `body` must be in a very specific format so run your json through `jq` like so: `echo '{...}' | jq -S | jq -sR`.

To get the current `timestamp`, run `date -Iseconds --utc`.

#### Sign & Acknowledge

```console
$ snap sign -k <key-name> network-registry.json > network-registry.assert
$ snap ack network-registry.assert
```

##### "cannot resolve prerequisite assertion"

```console
$ snap known --remote account account-id=<account-id> > /tmp/account.assert
$ snap ack /tmp/account.assert￼

$ snap known --remote account-key public-key-sha3-384=<key-sha-digest> > /tmp/account-key.assert
$ snap ack /tmp/account-key.assert
```

### With Snapcraft

Register for an Ubuntu One (staging) account [here](https://login.staging.ubuntu.com/) and for a Store (staging) account [here](https://dashboard.staging.snapcraft.io/).

We need to use staging since the registries API is disabled on production:

```console
$ snapcraft edit-registries <account-id> network --key-name=<key-name>
Store operation failed:
- feature-disabled: Registries API is disabled
```

#### Login

```console
$ export UBUNTU_ONE_SSO_URL="https://login.staging.ubuntu.com"
$ export STORE_DASHBOARD_URL="https://dashboard.staging.snapcraft.io"
$ snapcraft login
```

#### Setup Keys

```console
$ snapcraft create-key <key-name>
$ snapcraft register-key <key-name>
```

#### Create a New Registry

```console
$ snapcraft whoami
email: <email>
username: <username>
id: <account-id>
permissions: package_access, package_manage, package_metrics, package_push, package_register, package_release, package_update
channels: no restrictions
expires: 2025-10-25T08:38:11.000Z

$ snapcraft edit-registries <account-id> network --key-name=<key-name>
Successfully created revision 1 for 'network'.

$ snapcraft list-registries
Account ID                        Name      Revision  When
<account-id>                      network          1  2024-10-2
```

#### API

The API documentation is available [here](https://dashboard.snapcraft.io/docs/reference/v2/en/registries.html).\
Install [surl](https://snapcraft.io/surl) to interact with it.

```console
$ surl -a staging -s staging -e <email>
{
  "account": {
    "id": "<account-id>",
    "email": "<email>",
    "username": "<username>",
    "name": "<your name>"
  },
  "channels": null,
  "packages": null,
  "permissions": [
    "package_access"
  ],
  "store_ids": null,
  "expires": "2025-04-23T00:00:00.000",
  "errors": []
}

$ surl -a staging https://dashboard.staging.snapcraft.io/api/v2/registries | jq
{
  "assertions": [
    {
      "headers": {
        "account-id": "<account-id>",
        "authority-id": "<account-ids>",
        "body-length": "92",
        "name": "network",
        "revision": "1",
        "sign-key-sha3-384": "RFxSEcXp9jocWM85Hm9m62JOtXKvu1k5toUXUZ6RGw20Md3WlZaf7P-SpZ_ed1wD",
        "timestamp": "2024-10-25T08:55:22Z",
        "type": "registry",
        "views": {
          "wifi-setup": {
            "rules": [
              {
                "access": "write",
                "request": "ssids",
                "storage": "wifi.ssids"
              }
            ]
          }
        }
      },
      "body": "{\n  \"storage\": {\n    \"schema\": {\n      \"wifi\": {\n        \"values\": \"any\"\n      }\n    }\n  }\n}"
    }
  ]
}
```

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

$ sudo net-ctrl.sh -c 'snapctl set --view :proxy-control https.url=https://proxy.example.com'
$ sudo net-ctrl.sh -c 'snapctl set --view :proxy-control ftp.url=ftp://proxy.example.com'
$ sudo snap set f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/control-proxy 'https.bypass=["https://127.0.0.1", "https://localhost"]'

$ net-ctrl.sh -c 'snapctl get --view :proxy-control'
{
    "ftp": {
        "url": "ftp://proxy.example.com"
    },
    "https": {
        "bypass": [
            "https://127.0.0.1",
            "https://localhost"
        ],
        "url": "https://proxy.example.com"
    }
}
```

## Proxying

Run a docker container on the host (`proxy.example.com`) or locally:

```console
$ docker run -d --name squid-container -e TZ=UTC -p 3128:3128 ubuntu/squid:5.2-22.04_beta
```

```console
$ browser "https://example.com"

╭──────────────────────────────────────────────────────────────────────────────────────────────╮
│                                        Example Domain                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯


This domain is for use in illustrative examples in documents. You may use this domain in
literature without prior coordination or asking for permission.


More information... (https://www.iana.org/domains/example)

```

```console
$ docker logs -f squid-container
[...]
1729879108.361   2812 172.17.0.1 TCP_TUNNEL/200 5435 CONNECT example.com:443 - HIER_DIRECT/93.184.215.14 -
1729879154.849   1618 172.17.0.1 TCP_TUNNEL/200 5458 CONNECT example.com:443 - HIER_DIRECT/93.184.215.14 -
```

## Hooks

### browser/proxy-observe-view-changed

```console
$ sudo net-ctrl.sh -c 'snapctl set --view :proxy-control https.url="http://localhost:3199/"'
$ snap changes
ID   Status  Spawn                     Ready                     Summary
[...]
692  Done    today at 10:32 CET        today at 10:32 CET        Modify registry "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network"
$ snap tasks 692
Status  Spawn               Ready               Summary
Done    today at 10:32 CET  today at 10:32 CET  Clears the ongoing registry transaction from state (on error)
Done    today at 10:32 CET  today at 10:32 CET  Run hook proxy-observe-view-changed of snap "browser"
Done    today at 10:32 CET  today at 10:32 CET  Commit changes to registry "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network"
Done    today at 10:32 CET  today at 10:32 CET  Clears the ongoing registry transaction from state
$ cat /var/snap/browser/common/view-changed-proxy-observe
{
    "ftp": {
        "url": "ftp://proxy.example.com"
    },
    "https": {
        "bypass": [
            "https://127.0.0.1",
            "https://localhost"
        ],
        "url": "http://localhost:3199/"
    }
}
```

### net-ctrl/change-view-proxy-control

```console
$ sudo net-ctrl.sh -c 'snapctl set --view :proxy-control https.url="not a url?"'
$ snap changes
ID   Status  Spawn                     Ready                     Summary
[...]
708  Error   today at 11:40 CET        today at 11:40 CET        Modify registry "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network"
$ snap tasks 708
Status  Spawn               Ready               Summary
Undone  today at 11:43 CET  today at 11:43 CET  Clears the ongoing registry transaction from state (on error)
Error   today at 11:43 CET  today at 11:43 CET  Run hook change-view-proxy-control of snap "net-ctrl"
Hold    today at 11:43 CET  today at 11:43 CET  Run hook proxy-observe-view-changed of snap "browser"
Hold    today at 11:43 CET  today at 11:43 CET  Commit changes to registry "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network"
Hold    today at 11:43 CET  today at 11:43 CET  Clears the ongoing registry transaction from state

......................................................................
Run hook change-view-proxy-control of snap "net-ctrl"

2024-10-30T13:43:38+03:00 ERROR run hook "change-view-proxy-control": failed to validate url: not a url?
```

## Addendum
