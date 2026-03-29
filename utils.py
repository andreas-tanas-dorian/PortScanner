import socket

def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None

def grab_banner(sock):
    try:
        sock.send(b"Hello\r\n")
        banner = sock.recv(1024).decode().strip()
        return banner if banner else "No banner"
    except:
        return "No banner"