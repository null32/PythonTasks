import signal
import boto3

should_stop = False
def ctrc_stop(sig, frame):
    global should_stop
    should_stop = True

def reciever_loop(sqs_name):
    signal.signal(signal.SIGINT, ctrc_stop)

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName = sqs_name)

    print('Waiting for messages, send Ctrl+C to exit')
    while not should_stop:
        msgs = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=10)
        for msg in msgs:
            print(f'<= msg(id: {msg.message_id}): {msg.body}')
            msg.delete()
    print("bye")