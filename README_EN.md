# Overview
I developed an online chat messenger, which is a distributed system allowing clients to establish and manage their own chat rooms using server resources. For user management, I utilized a hash table to track users in memory, assigning each client a unique token for secure identification. Socket programming was employed for Inter-Process Communication (IPC), choosing SOCK_STREAM type TCP sockets to ensure reliable bidirectional communication for critical operations such as joining and creating chat rooms, and token generation.

After the initial connection establishment, I switched to SOCK_DGRAM type UDP sockets for live message relay within the chat rooms. This UDP connection prioritizes speed and efficiency over TCP's reliability, accepting the possibility of minimal packet loss for real-time communication.

# Objective
- Learn about the client-server model and how it is utilized in distributed applications.
- Understand the operating system's process structure and how to generate new processes using system calls such as exec and fork.
- Learn about handling child processes inheriting the state of parent processes.
- Grasp the concept of inter-process communication (IPC) and understand how it is used for processes to send data to other processes locally or over a network.
- Build IPC connections using anonymous pipes and named pipes.
- Utilize Unix sockets to establish bidirectional IPC connections between different computers.
- Study the fundamentals of networking, including the five network layers and the main protocols associated with each.
- Explore the internal and external structure of the World Wide Web.
- Establish bidirectional connections between clients and servers over the Internet using TCP network sockets, enabling data transmission.
- Perform low-overhead data transmission between clients and servers over the Internet using UDP network sockets.
- Encode and decode data into bits when sending data streams between client and server processes.
- Understand the basics of creating custom protocols used by clients and servers during the protocol creation process.

# Methodology Per Project
- Develop client and server applications to build a distributed application.
-  Use the AF_INET protocol in the socket domain. The AF_INET domain utilizes the IPv4 internet protocol for data exchange over the internet.
- Use SOCK_STREAM type sockets, also known as TCP connections, which provide ordered, reliable, bidirectional byte streams for communication between clients and servers.
- Perform UDP connections using SOCK_DGRAM type sockets, allowing messages to be sent to other processes as datagrams.
- Encode data into bits for transmission through sockets, and decode received bits back into data.
- Design and create a protocol for reading data streams. This protocol includes headers and bodies, and both clients and servers must convert bits to data according to the protocol specifications.


