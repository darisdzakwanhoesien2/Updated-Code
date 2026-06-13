#ADLABS DRONE PROGRAMMING WORKSHOP

# Import the necessary modules
import socket
import threading
import time

# IP and port of Tello
tello1_address = ('192.168.10.1', 8889)
# IP and port of local computer
local1_address = ('', 9000)
# Create a UDP connection that we'll send the command to
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Avoid hanging forever on recv if the drone is off / unreachable.
sock1.settimeout(1.0)
# Bind to the local address and port
sock1.bind(local1_address)

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
  # Try to send the message otherwise print the exception
  try:
    sock1.sendto(message.encode(), tello1_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  # Delay for a user-defined period of time
  # Tello expects a small gap between commands; without this you can drop/ignore commands.
  time.sleep(delay)

# Receive the message from Tello
def receive(stop_event):
  # Continuously loop and listen for incoming messages
  while not stop_event.is_set():
    # Try to receive the message otherwise print the exception
    try:
      response1, ip_address = sock1.recvfrom(128)
      
      print("Received message: from Tello EDU #1: " + response1.decode(encoding='utf-8'))
    except socket.timeout:
      continue
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      sock1.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
stop_event = threading.Event()
receiveThread = threading.Thread(target=receive, args=(stop_event,))
receiveThread.daemon = True
receiveThread.start()

###THIS IS THE AREA YOU CAN EDIT###

def main():
  # Each leg of the box will be 100 cm. Tello uses cm units by default.
  box_leg_distance = 100
  yaw_angle = 90

  # Put Tello into command mode
  send("command", 3)
  send("takeoff", 8)

  for _ in range(4):
    send(f"forward {box_leg_distance}", 4)
    send(f"cw {yaw_angle}", 3)

  send("land", 5)
  print("Mission completed successfully!")

if __name__ == "__main__":
  try:
    main()
  finally:
    stop_event.set()
    try:
      sock1.close()
    except Exception:
      pass
###THIS IS PAST THE AREA YOU HAVE TO EDIT###
