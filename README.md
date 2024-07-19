# ChatClient

### Run example:
```cmd
python3 main_server.py # will initilaize server client
python3 main_client.py # will create new client that connect to this server
python3 main_ai.py # will create "ai bot" client that connect to this server
```

### Outputs
```python
# Server
2024-07-19 14:14:56 [info     ] Chat server started on localhost:12345
2024-07-19 14:15:05 [info     ] Accepted new connection from 127.0.0.1:55672 username:raza
2024-07-19 14:15:08 [info     ] Received message from raza: hi
2024-07-19 14:15:22 [info     ] Accepted new connection from 127.0.0.1:55673 username:ishay
2024-07-19 14:15:44 [info     ] Received message from raza: how are u?

# Client 1
Enter your username: raza
raza | hi
Server| ishay joined the chat.
raza | how are u?

# Client 2
Enter your username: ishay
raza| how are u?

```