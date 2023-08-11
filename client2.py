import socket
import threading
import os

HOST = '192.168.197.190'
PORT = 12345

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode("utf-8"))
        except:
            break

def receive_file(connection, filename):
    try:
        with open(filename, 'wb') as file:
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                file.write(data)
            print(f"File '{filename}' berhasil didownload.")
    except Exception as e:
        print(f"Error: {e}")

def send_file(client_socket, file_path):
    file_type = file_path.split(".")[-1].lower()
    file_size = os.path.getsize(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    message = f"!file {file_type} {file_size} {file_name}"
    client_socket.send(message.encode("utf-8"))

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)

    print(f"File {file_path} sent successfully.")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Input username from the client
    username = input("Enter your username: ")
    client_socket.send(username.encode("utf-8"))

    # Input groupname from the client
    groupname = input("Enter your group name: ")
    client_socket.send(groupname.encode("utf-8"))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        print("Berhasil terhubung sama server, ALHAMDULILLAH")
        print("Kalo mau unicast, kamu bisa pake '@username pesan' contoh '@Nikko hai'")
        print("Kalo mau multicast, kamu bisa pake '$namagrup pesan' contoh '$heavenhold hai'")
        print("Kalo mau Broadcast, kamu bisa pake '*Broadcast pesan' contoh '*Broadcast hai'")
        message = input()

        if message == "exit":
            client_socket.send(message.encode("utf-8"))
            break
        elif message.startswith("@"):
            parts = message.split(" ", 1)
            recipient = parts[0][1:]
            message = parts[1]
            full_message = "@{} {}".format(recipient, message)
        elif message.startswith("$"):
            parts = message.split(" ", 1)
            group = parts[0][1:]
            message = parts[1]
            full_message = "${} {}".format(group, message)
        elif message.startswith("!file"):
            file_path = message.split(" ")[1]
            send_file(client_socket, file_path)
            continue
        else:
            full_message = message

        client_socket.send(full_message.encode("utf-8"))

    client_socket.close()

if __name__ == "__main__":
    main()
