__all__ = ['reciever_loop', 'sender_loop']

from sqs_demo import reciever
from sqs_demo import sender

def reciever_loop(sqs_name):
    reciever.reciever_loop(sqs_name)

def sender_loop(sqs_name):
    sender.sender_loop(sqs_name)