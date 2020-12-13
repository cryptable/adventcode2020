import os
import sys
import struct
import threading

PIPE_IN = '/tmp/qemupipe.in'
PIPE_OUT = '/tmp/qemupipe.out'


def print_info_thread(arg1):
    pipe_out = os.open(PIPE_OUT, os.O_RDONLY)
    while True:
        data = read_message(pipe_out)
        print("cmd {} data {}".format(data[0], data[1]))
    os.close(pipe_out)


def char_out(kar):
    sys.stdout.write(kar)


def encode_cmd(cmd: int) -> bytes:
    return struct.pack(">B", cmd)


def encode_msg_size(size: int) -> bytes:
    return struct.pack(">I", size)


def decode_msg_size(size_bytes: bytes) -> int:
    return struct.unpack(">I", size_bytes)[0]


def read_data(pipe, length):
    data = b''
    while length > 0:
        piece = os.read(pipe, length)
        data += piece
        length -= len(piece)
    return data


def create_msg(cmd, content: bytes) -> bytes:
    size = len(content)
    return encode_cmd(cmd) + encode_msg_size(size) + content


def read_message(pipe):
    cmd = read_data(pipe, 1)
    print("cmd {}".format(cmd))
    msg_lg_bytes = read_data(pipe, 4)
    print("lg {}".format(len(msg_lg_bytes)))
    msg_lg = decode_msg_size(msg_lg_bytes)
    print("lg {}".format(msg_lg))
    msg_data = read_data(pipe, msg_lg)
    return (cmd, msg_data)


if __name__ == '__main__':
    print('Open Pipe')

    pipe_in = os.open(PIPE_IN, os.O_WRONLY)
    try:
        x = threading.Thread(target=print_info_thread, args=(1,))
        x.start()
        msg = create_msg(2, "Help!".encode("utf-8"))
        print("Write message")
        kar = os.write(pipe_in, msg)
        print("Message written, read message")
    finally:
        os.close(pipe_in)
    x.join(30)