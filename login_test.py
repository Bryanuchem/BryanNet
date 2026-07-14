from librouteros import connect

api = connect(
    host="192.168.1.159",
    username="bryannet",
    password="BryanNet123",
    port=8728,
)

print("Connected")