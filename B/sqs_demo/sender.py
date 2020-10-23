import boto3

def sender_loop(sqs_name):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName = sqs_name)

    print('Enter messages, Send Ctrl+C or Ctrl+D to exit')
    while True:
        try:
            msg = input()
        except:
            break
        if len(msg) == 0:
            break

        resp = queue.send_message(MessageBody = msg)
        if not 'MessageId' in resp:
            print(f'=> {resp}')
        else:
            print(f'=> msg(id: {resp["MessageId"]}): {msg}')
    print('bye')