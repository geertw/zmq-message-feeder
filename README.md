# ZeroMQ Message Feeder

This tool reads all messages in a plaintext file or gzip file and
sends those messages to connected clients. This tool creates a ZeroMQ
pub/sub socket to which one (or more) clients can connect.

You can use this tool to performance test a ZeroMQ implementation, or
to feed it with a set of test messages.

Features:

* Read one or more input files
* Read directly from gzip'ed files (.gz extension)
* Send message plaintext or gzip'ed
* Allows for basic performance and stress testing

## Usage

`zmq-message-feeder.py [-h] [-b BIND] [-g] [-d DELAY] FILE [FILE ...]`

### Examples

Broadcast a set of messages (one message per line):

```
./zmq-message-feeder.py messages.txt
```

Use multiple gzip'ed files as input:

```
./zmq-message-feeder.py -m messages01.gz messages02.gz messages03.gz
```

Send messages as gzip:

```
./zmq-message-feeder.py -g messages.txt
```

## Requirements

* python2
* pyzmq
* gzip
* argparse

## License

Copyright (c) 2015 Geert Wirken

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
