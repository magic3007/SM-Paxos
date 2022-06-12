# SM-Paxos
🕹 A <u>**S**</u>tate <u>**M**</u>achine asynchronous consensus protocol based on <u>**Paxos**</u> protocol.

## Getting Start
- **Install the Dependency**

```bash
pip install -r requirements.txt
```

- **Autogen the Python Code for `grpc` and `protobuf`**

```bash
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=. ./kv.proto
```
If you finish running this command without error, you will see two new files `kv_pb2_grpc.py` and `ky_pb2.py` in current directory.
