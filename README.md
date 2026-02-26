# dns_notify

A command-line tool to send a DNS NOTIFY message (RFC 1996) to a nameserver.

## Overview

DNS NOTIFY is a mechanism defined in [RFC 1996](https://www.rfc-editor.org/rfc/rfc1996) that allows a primary nameserver to notify secondary nameservers that zone data has changed, prompting them to initiate a zone transfer. This script lets you send such a notification manually — useful for testing zone transfer setups, triggering immediate replication, or diagnosing NOTIFY handling on a nameserver.

The script sends a DNS message with:
- Opcode: `NOTIFY` (4)
- Flag: `AA` (Authoritative Answer)
- Question section: the zone name with type `SOA`

## Requirements

Python 3.7+ and [dnspython](https://www.dnspython.org/):

```
pip install dnspython
```

## Usage

```
dns_notify.py [-h] [-p PORT] [-t SECS] [--tcp] zone server
```

### Positional arguments

| Argument | Description |
|---|---|
| `zone` | Zone name to notify (e.g. `example.com`) |
| `server` | Target nameserver — hostname, short name, or IP address |

### Options

| Option | Default | Description |
|---|---|---|
| `-p PORT`, `--port PORT` | `53` | Destination UDP/TCP port |
| `-t SECS`, `--timeout SECS` | `5.0` | Seconds to wait for a response |
| `--tcp` | — | Use TCP instead of UDP |
| `-h`, `--help` | — | Show help and exit |

## Examples

Send a NOTIFY to a nameserver by hostname:
```
./dns_notify.py example.com ns1.example.com
```

Send a NOTIFY to a server by IP address:
```
./dns_notify.py example.com 192.0.2.53
```

Use a non-standard port:
```
./dns_notify.py example.com ns1.example.com -p 5353
```

Use TCP transport:
```
./dns_notify.py example.com ns1.example.com --tcp
```

Set a shorter timeout:
```
./dns_notify.py example.com ns1.example.com -t 2
```

### Example output

```
NOTIFY sent for zone 'example.com' to ns1.example.com (192.0.2.53):53
Response rcode: NOERROR
```

A response of `NOERROR` means the server acknowledged the NOTIFY. `NOTAUTH` indicates the server is not authoritative for the zone. `NOTIMP` or `REFUSED` means the server does not support or is rejecting NOTIFY messages.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | NOTIFY sent and response received |
| `1` | Error (resolution failure, timeout, network error) |
