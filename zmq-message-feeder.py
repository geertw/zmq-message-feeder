#!/usr/bin/env python

"""
ZeroMQ Message Feeder

This tool reads all messages in a plaintext file or gzip file and
sends those messages to connected clients. This tool creates a ZeroMQ
pub/sub socket to which one (or more) clients can connect. You can
use this tool to performance test a ZeroMQ implementation, or to feed
it with a set of test messages.

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
"""

import zmq
import time
import gzip
import argparse
from cStringIO import StringIO

# Initialise argparse
parser = argparse.ArgumentParser(
    description='This tool reads all messages in a plaintext file or gzip file and \
sends those messages to connected clients. This tool creates a ZeroMQ \
pub/sub socket to which one (or more) clients can connect. You can \
use this tool to performance test a ZeroMQ implementation, or to feed \
it with a set of test messages.')

parser.add_argument('-b', '--bind', action='store', default='tcp://127.0.0.1:12345', help='bind address (default: tcp://127.0.0.1:12345)')
parser.add_argument('-g', '--send-gzip', dest='send_gzip', action='store_true')
parser.add_argument('-d', '--delay', action='store', default='1', help='delay (in seconds) before sending (default: 1s)')
parser.add_argument('-e', '--envelope', action='store', default='', help='envelope')
parser.add_argument('-m', '--message-mode', dest='message_mode', action='store_true', help='enable message mode: treat each file as a full message. Default: treat each line as a new message')

parser.add_argument('FILE', nargs='+',
    action='store', help='input file (text or .gz)')

args = parser.parse_args()

# Prepare ZMQ
context = zmq.Context()
 
publisher = context.socket(zmq.PUB)
publisher.setsockopt(zmq.SNDHWM, 0)
publisher.bind(args.bind)

# Read and prepare messages:
msg_count = 0
messages = []

print "Binding to %s" % args.bind

print "Preparing..."

def prepare_message(contents):
    global args
    global messages

    if (args.send_gzip == True):
        out = StringIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(contents)
        message = out.getvalue()
    else:
        message = contents

    messages.append(message)


for filename in args.FILE:
    # Open a plain text or GZIP file:
    if filename.endswith('.gz'):
        inputfile = gzip.open(filename, 'rb')
    else:
        inputfile = open(filename, 'r')

    with inputfile as f:
        if args.message_mode:
            # Read all lines (combined they are a new message)
            message = f.read()
            prepare_message(message)
        else:
            # Read all lines (each line is a new message)
            for line in f:
                prepare_message(line)

# Optional start delay
if args.delay > 0:
    print "Waiting %.2f sec." % float(args.delay)
    time.sleep(float(args.delay))

# Send messages
start = time.time()
msg_count = len(messages)
print "Starting to send %s messages" % msg_count

for message in messages:
    publisher.send_multipart([args.envelope, message])

# Statistics:
print "Sent %s messages in %.2f sec." % (msg_count, time.time() - start)
