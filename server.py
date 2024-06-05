import socket
import threading

### Performs calculations returns result ###
def perform_operation(operation, operand1 = 0, operand2 = 0):
    
    # set 32 bit boundries
    MIN_SIZE = -2**31
    MAX_SIZE = (2**31)-1

    # Performs the correct operations defaults to exit via 'q' (EXIT) input
    if operation == '+':
        result = operand1 + operand2
    elif operation == '-':
        result = operand1 - operand2
    elif operation == '*':
        result = operand1 * operand2
    elif operation == '/':

        # Handle Division by zero return -1
        if operand2 == 0:
            result = -1
        else:
            result = operand1 // operand2
    else:
        result= -1

    # Handle overflor by returning -1
    if (result <= MIN_SIZE or result >= MAX_SIZE):
        result = -1
    return result

### Receives data from client returns the result ###
def client_handler(cs,address):

    while True:

        # Recieve the operation from client
        operation_ = cs.recv(1)
        
        # checks if client intialized a disconnect or if no data was entered
        if not operation_ or operation_.decode() == 'q':
            break  
            
        # Convert client operation to String  
        operation = operation_.decode()

        # Convert client operand to int
        operand1_ = cs.recv(4)
        operand1 = int.from_bytes(operand1_, byteorder='big', signed=True)
        
        # Convert client operand to int
        operand2_ = cs.recv(4)
        operand2 = int.from_bytes(operand2_, byteorder='big', signed=True)

        # Calculate final result of the equation
        result = perform_operation(operation, operand1, operand2)

        # Send result back to client
        cs.send(result.to_bytes(4, byteorder='big', signed=True))\
    
    # Close Web Socket
    cs.close()

    print(f"Connection from {address} Disconnected!")

def main():

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((socket.gethostname(),2024))
    s.listen(5)

    while True:

        # Accept incoming Connection
        cs, address = s.accept()
        print(f"Connection from {address} successful!")

        # Use threads to handle numerous clients at once
        client_handler_thread=threading.Thread(target=client_handler, args=(cs,address,))
        client_handler_thread.start()

main()

