# LOG FILTER

## Description

This is a simple log filter that can be used to filter out log messages from a log file.

like this:

```bash
[07/06 08:20:56] [35] [ap] [service0] start=0x3c265ef8 size=8192 user=0x2c680cef
[07/06 08:20:56] [35] [ap] [service0] service0_init: service0 is unlocked, tag=init
[07/06 08:20:57] [35] [ap] [asd] start_asd_server: started, server: asdserver
[07/06 08:20:57] [35] [ap] [service1] parse_service_config: table is null
[07/06 08:20:57] [35] [ap] [service1] load_services: frameware version update, reload file...
[07/06 08:20:57] [35] [ap] [asd] asd: begin load file: /files//666/resource.bin
[07/06 08:20:57] [35] [sen] [service2] load_server_from_file: begin load server file: /files//666/resource.bin
[07/06 08:20:57] [31] [ap] [asd] stack_init: Firmware Version: 0x114514
[07/06 08:20:57] [31] [cp] [service1] stack_init: Stack Init Success:0
```

## Usage

```bash
$ ./log_filter.py -h

usage: log_filter.py [-h] [-d DATE] [-i TID] [-c CORE] [-e EXTRA] [-t TYPE] [-x CONTENT] [-o] [-a] path

Log Parser

positional arguments:
  path                  Path to log file

options:
  -h, --help            show this help message and exit
  -d DATE, --date DATE  Date
  -i TID, --tid TID     Thread ID
  -c CORE, --core CORE  Core
  -e EXTRA, --extra EXTRA
                        Extra
  -t TYPE, --type TYPE  Type
  -x CONTENT, --content CONTENT
                        Content
  -o, --only-content    Only print content
  -a, --all-categories  Get all categories
```

## Example

### Filter by `ap` core and `service0` type

```bash
./log_filter.py log.log -c ap -t service0
```

> [07/06 08:20:56] [35] [ap] [service0] start=0x3c265ef8 size=8192 user=0x2c680cef
> [07/06 08:20:56] [35] [ap] [service0] service0_init: service0 is unlocked, tag=init

### Filter by `asd` type

```bash
./log_filter.py log.log -t asd
```

> ./log_filter.py log.log -t asd
> [07/06 08:20:57] [35] [ap] [asd] start_asd_server: started, server: asdserver
> [07/06 08:20:57] [35] [ap] [asd] asd: begin load file: /files//666/resource.bin
> [07/06 08:20:57] [31] [ap] [asd] stack_init: Firmware Version: 0x114514

### Filter by `asd` type and only print content

```bash
./log_filter.py log.log -t asd -o
```

> ./log_filter.py log.log -t asd
> start_asd_server: started, server: asdserver
> asd: begin load file: /files//666/resource.bin
> stack_init: Firmware Version: 0x114514

