from match_client.match import Match
from match_client.match.ttypes import User

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from sys import stdin


def operate(op, user_id, username, score):
    # Make socket
    transport = TSocket.TSocket('127.0.0.1', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Match.Client(protocol)

    # Connect!
    transport.open()

    user = User(user_id, username, score) # 添加用户

    # 如果选项为增加用户则执行增加用户函数，反之执行删除用户函数
    if op == "add":
        client.add_user(user, "")
    elif op == "remove":
        client.remove_user(user, "")


    # Close!
    transport.close()

def main():
    # 从终端读入信息
    for line in stdin:
        op, user_id, username, score = line.split(' ')
        operate(op, int(user_id), username, int(score))

if __name__ == "__main__":
    main()
