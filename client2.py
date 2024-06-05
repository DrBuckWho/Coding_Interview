import socket, sys

### This function sends Operator and both operands to the server then return an output value
def send_client_data(cs,operation, operand1, operand2):
    
    # Send the operation
    cs.send(operation.encode())

    # Send the first operand (4 bytes signed 32-bit big-endian)
    cs.send(operand1.to_bytes(4, byteorder='big', signed=True))

    # Send the second operand (4 bytes signed 32-bit big-endian)
    cs.send(operand2.to_bytes(4, byteorder='big', signed=True))

    # Receive and decode the response (4 bytes, signed 32-bit big-endian)
    response = cs.recv(4)
    result = int.from_bytes(response, byteorder='big', signed=True)

    return result


def main():

    cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cs.connect((socket.gethostname(), 2024))
    
    while True:
            
            ### Command Line Optional for test case testing ###
            operation = sys.argv[1]
            operand1 = int(sys.argv[2])
            operand2 = int(sys.argv[3])

            # If exit is chosen send disconnect trigger to server
            if operation == 'q':
                cs.sendall(operation.encode())
                break
            
            # Calls the function to operation and operands to the server returns the servers response
            result = send_client_data(cs, operation, operand1, operand2)
            print(f"Result: {result}")

    # Close Web Socket
    cs.close()
    print("Disconnected")

main()