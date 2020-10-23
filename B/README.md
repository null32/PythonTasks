# Usage
```sh
python3 sqs_demo {s,r} <sqs_name>
```

## Example for sender
Run package
```sh
python3 sqs_demo s PySQSTest
```
and enter any text. You will get simillar result:
```
< test message
> => msg(id: d3d12130-5858-45c8-9f89-de1f5eaa4b36): test message
```

## Example for reciever
Run package
```sh
python3 sqs_demo r PySQSTest
```
and wait for messages. You will get simillar result:
```
<= msg(id: d3d12130-5858-45c8-9f89-de1f5eaa4b36): test message
```