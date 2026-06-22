# Ephemeral Data

> [!IMPORTANT]
> This section builds upon the demo in the README. Make sure you've completed that first before proceeding.

By default, confdb configuration is stored within snapd. However, there are scenarios where the authoritative source of this configuration data exists outside snapd - for instance, in configuration files or databases managed by external systems. This externally-managed data is called _ephemeral data_.

Ephemeral data allows confdb to act as a view or cache of external data. To read or write ephemeral data, snapd runs hooks provided by custodian snaps. These hooks are automatically triggered by snapd when getting & setting config:

- `load-view-<plug>` - Called when snapd needs to read the latest view data from the external source.
- `save-view-<plug>` - Called when setting confdb view data to update the external source.

## Example

For this example, we'll modify the network confdb demo to read proxy configuration from a file managed by the snap. This simulates a scenario where proxy settings are managed by an external system that writes to `/var/snap/net-ctrl/common/network.env`.

### Setup

Create a configuration file at the snap's common data directory:

```console
$ cat > /var/snap/net-ctrl/common/network.env << 'EOF'
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080
FTP_PROXY=ftp://proxy.example.com
NO_PROXY=*://*.company.internal
EOF
```

### Update the Assertion

Since the data is now ephemeral, we need to mark the entries as ephemeral in the storage. The `ephemeral: true` flag tells snapd that this data should not be persisted in its internal storage, but instead should be managed through the hooks we'll implement.

See [Creating a confdb-schema Assertion by Hand](../README.md#creating-a-confdb-schema-assertion-by-hand) in the README for the full sign-and-ack workflow. The relevant change to the storage body is:

```json
{
  "storage": {
    [...]
    "schema": {
      "v1": {
        "schema": {
          "proxy": {
            "keys": "${protocol}",
            "values": {
              "schema": {
                "bypass": {
                  "type": "array",
                  "unique": true,
                  "values": "string",
                  "ephemeral": true
                },
                "url": {
                  "type": "string",
                  "ephemeral": true
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Implement the `save-view-network-proxy-admin` Hook

This hook reads the current confdb state and writes it back to the external file, ensuring that any changes made through the confdb interface are preserved in the authoritative external source.

> [!IMPORTANT]
> A `save-view-<plug>` hook must exist for a `load-view-<plug>` hook to work.

Create a `snap/hooks/save-view-network-proxy-admin` file in the net-ctrl snap:

```python
#!/usr/bin/env python3

import json
import subprocess
import os
import sys

config_file = os.path.join(os.environ["SNAP_COMMON"], "network.env")

# Get entire view in one call
result = subprocess.run(
    ["snapctl", "get", "--view", ":network-proxy-admin", "-d"],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print(f"No confdb data found: {result.stderr}")
    sys.exit(1)

# Build updates
updates = {}
bypass_lists = []
view_data = json.loads(result.stdout)
for protocol, config in view_data.items():
    if "url" in config:
        env_key = f"{protocol.upper()}_PROXY"
        updates[env_key] = config["url"]

    if "bypass" in config and config["bypass"]:
        bypass_lists.extend(config["bypass"])

if bypass_lists:
    seen = set()
    merged_bypass = []
    for item in bypass_lists:
        if item not in seen:
            seen.add(item)
            merged_bypass.append(item)
    updates["NO_PROXY"] = ",".join(merged_bypass)

# Read existing file
lines = []
if os.path.exists(config_file):
    with open(config_file) as f:
        lines = f.readlines()

# Update existing lines or track what needs to be added
updated_keys = set()
for i, line in enumerate(lines):
    for key, value in updates.items():
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated_keys.add(key)

# Add new keys that weren't found
for key, value in updates.items():
    if key not in updated_keys:
        lines.append(f"{key}={value}\n")

# Write
with open(config_file, "w") as f:
    f.writelines(lines)
```

Make the hook executable:

```console
$ chmod +x net-ctrl/snap/hooks/save-view-network-proxy-admin
```

> [!NOTE]
> These hooks use minimal error handling since it's a demo. Production implementations should include robust error handling and logging.

#### Testing

Rebuild and install the modified net-ctrl snap:

```console
$ snapcraft
Packed net-ctrl_0.2_amd64.snap
$ snap install net-ctrl_0.2_amd64.snap --dangerous
```

Change the `https` proxy URL with `snap set`:

```console
$ snap set <your-account-id>/network/proxy-admin 'https.url="http://localhost:3199/"'

$ cat /var/snap/net-ctrl/common/network.env
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://localhost:3199/
FTP_PROXY=ftp://proxy.example.com
NO_PROXY=*://*.company.internal
```

When you set the confdb value, snapd automatically triggered the `save-view-network-proxy-admin` hook. The hook read the current confdb state and updated the file, changing only the `HTTPS_PROXY` line while preserving the existing values.

### Implement the `load-view-network-proxy-admin` Hook

Now we'll implement the complementary hook that reads from the external source and populates the confdb. This closes the loop between the external source and the confdb view.

Create a `snap/hooks/load-view-network-proxy-admin` file in the net-ctrl snap:

```python
#!/usr/bin/env python3

import json
import os
import subprocess
import sys

config_file = os.path.join(os.environ["SNAP_COMMON"], "network.env")

if not os.path.exists(config_file):
    print(f"Config file {config_file} not found")
    sys.exit(1)

# Read environment variables from file
env_vars = {}
with open(config_file) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            env_vars[key] = value

# Parse NO_PROXY
bypass_list = []
if "NO_PROXY" in env_vars:
    bypass_list = [host.strip() for host in env_vars["NO_PROXY"].split(",")]

# Build config for each protocol
settings = []
for protocol, env_key in [
    ("http", "HTTP_PROXY"),
    ("https", "HTTPS_PROXY"),
    ("ftp", "FTP_PROXY"),
]:
    if env_key in env_vars:
        protocol_config = {
            "url": env_vars[env_key],
            "bypass": bypass_list
        }
        settings.append(f"{protocol}={json.dumps(protocol_config)}")

# Set
if settings:
    cmd = ["snapctl", "set", "--view", ":network-proxy-admin"] + settings
    subprocess.run(cmd)
```

Make the hook executable:

```console
$ chmod +x net-ctrl/snap/hooks/load-view-network-proxy-admin
```

#### Testing

Rebuild and install the modified net-ctrl snap:

```console
$ snapcraft
Packed net-ctrl_0.2_amd64.snap
$ snap install net-ctrl_0.2_amd64.snap --dangerous
```

Get the updated proxy config with `snap get`:

```console
$ snap get <your-account-id>/network/proxy-admin -d
{
    "http": {
        "bypass": [
            "*://*.company.internal"
        ],
        "url": "http://proxy.example.com:8080"
    },
    "https": {
        "bypass": [
            "*://*.company.internal"
        ],
        "url": "http://localhost:3199/"
    },
    "ftp": {
        "bypass": [
            "*://*.company.internal"
        ],
        "url": "ftp://proxy.example.com"
    }
}
```

When you get the confdb view, snapd automatically called the `load-view-network-proxy-admin` hook to populate the confdb view. It read from `/var/snap/net-ctrl/common/network.env`, parsed the proxy settings, and populated the confdb view with the external configuration.

🎉 **Congratulations!** You've successfully integrated external configuration sources with confdb.

## Further Reading

- [Confdb configuration mechanism > Ephemeral Data](https://snapcraft.io/docs/explanation/how-snaps-work/confdb-configuration-mechanism/#ephemeral-data)
