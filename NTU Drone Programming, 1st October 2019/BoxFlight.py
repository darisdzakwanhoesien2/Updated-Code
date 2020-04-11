#ADLABS DRONE PROGRAMMING WORKSHOP



# Import the necessary modules
import socket
import threading
import time

# IP and port of Tello
tello1_address = ('192.168.43.24', 8889)
# IP and port of local computer
local1_address = ('', 9010)
# Create a UDP connection that we'll send the command to
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
  time.sleep(delay)

# Receive the message from Tello
def receive():
  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response1, ip_address = sock1.recvfrom(128)
      
      print("Received message: from Tello EDU #1: " + response1.decode(encoding='utf-8'))
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      sock1.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

###THIS IS THE AREA YOU CAN EDIT###



# Each leg of the box will be 100 cm. Tello uses cm units by default.
box_leg_distance = 100
# Yaw 90 degrees
yaw_angle = 90
# Yaw clockwise (right)
yaw_direction = "cw"
# Put Tello into command mode
send("command", 3)
# Send the takeoff command
send("takeoff", 8)
# Loop and create each leg of the box
for i in range(4):
  # Fly forward
  send("forward " + str(box_leg_distance), 4)
  # Yaw right
  send("cw " + str(yaw_angle), 3)
# Land
send("land", 5)
# Print message
print("Mission completed successfully!")
###THIS IS PAST THE AREA YOU HAVE TO EDIT###
# Close the socket
sock1.close()
sock2.close()
