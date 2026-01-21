# Confdb APIs

## Snapd's API

The API documentation is available [here](https://snapcraft.io/docs/snapd-api#heading--confdb).

## Store's Confdb Schema API

Register for an Ubuntu One (staging) account [here](https://login.staging.ubuntu.com/) and for a Store (staging) account [here](https://dashboard.staging.snapcraft.io/).

```console
$ export UBUNTU_ONE_SSO_URL="https://login.staging.ubuntu.com"
$ export STORE_DASHBOARD_URL="https://dashboard.staging.snapcraft.io"
$ snapcraft login
```

The API documentation is available [here](https://dashboard.staging.snapcraft.io/docs/reference/v2/en/confdb-schemas.html).\
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

$ surl -a staging https://dashboard.staging.snapcraft.io/api/v2/confdb-schemas | jq
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
        "type": "confdb-schema",
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

To fetch the full signed assertion, run:

```console
$ curl --silent --header "Accept: application/x.ubuntu.assertion" https://assertions.staging.ubuntu.com/v1/assertions/confdb-schemas/<account-id>/<confdb-schema>
type: confdb-schema
authority-id: 10ptdA3uXGo7P7DCvMk9wSgKnHiYKEV0
revision: 1
account-id: 10ptdA3uXGo7P7DCvMk9wSgKnHiYKEV0
name: net
timestamp: 2024-10-25T08:55:22Z
views:
  wifi-setup:
    rules:
      -
        access: write
        request: ssids
        storage: wifi.ssids
body-length: 92
sign-key-sha3-384: RFxSEcXp9jocWM85Hm9m62JOtXKvu1k5toUXUZ6RGw20Md3WlZaf7P-SpZ_ed1wD

{
  "storage": {
    "schema": {
      "wifi": {
        "values": "any"
      }
    }
  }
}

AcLBcwQAAQoAHRYhBL09/H3Nqvu18UELh5IhgQJaoqEDBQJnG1z7AAoJEJIhgQJaoqEDmLIQAKYT
veCnwPt3oLtX0m6gcHxr7ggyhIoMNGfe7jx2v64kI8ZrgLYM/rhEUnBKce4oG3tVpRBDfh2UttQq
pixb0PCwsSgpIhRqP+bzcxcff7py+PidKxEobLjGRVMMQVT4dQJw3LqgKMTqmPVqNgXszoFViKLH
7UAWannUanE0CbckBFq5t1aunPH4KXXeW1DW1CCJlpRLaWZwqPQNM/EEEC2KQU6PoyE94VU2Jdm2
6DiBEjENo2mcEWWuQXuTa9L4OsbtU3c3PbO3s5SlNd+jraGof4c1L58kzDE7hpxBI/1pGCF9172u
aPbCEav8N9FNfRifIi2hj/IgSS4vyrnSW4jrB7wfTYRu8PiltQeIqV1kfwO3xFtigHggBAsL/jK/
ISKUA6h5EAc2yG7y5xEE4SaXGmWoQ3YaeR4RNQHx9NjJ5MQKYtpprtfpPZUc9JMfRMSIMPFG1EM+
ldfd4UWQYYQdnWrZc5PRlBlC7K4wTVOaF6BSduAX38ZM8EOPcc3Mf18Fj5uHOpW4PDOynQ6Lb8k3
yidmyylvvmpB0DS1e3xLY2PNHMwZ9/UsO3kzegUIMSCVixn3vXbFx91W4GU2tVFi5jW35xkvx0nk
xOAyEc2EBedXwu57XuIELIleoNm5+SUqAG9X97z/m8w6qHww57Lpwd8fEADgNDanDDNhtfZG
```
