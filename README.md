# google-file-system
![status](https://img.shields.io/badge/version-0.1-85a832) 

Project is based on the paper [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf).

Project Demo - https://youtu.be/LDqfd4PvoiQ

Index - [Changelog](#changelog) | [Dependency](#dependency) | [Commamnds](#commands) | [Architecture](#architecture)


## Changelog
- Added Remote Procedure Calls with `rpyc`
- Added replication factor
- Added Create, Read, Append, Delete & List operations


## Dependency
- rpyc

## Commands
- Create: `python client.py create <file_name>` 

- Read: `python client.py read <file_name> <data>`

- Append: `python client.py append <file_name> <string>`

- Delete: `python client.py delete <file_name>`

- List: `python client.py list`


## Architecture

The following architecture is based on the design goals mentioned below.

![GFS Architecture](https://github.com/rvarun11/google-file-system/blob/main/architecture.png)


### Why Big Storage is hard?
1. To improve __performance__, large systems require __sharding__
2. _Sharding_ leads to _faults_
3. To improve _fault tolerance_ we need make _replications_
4. _Replications_ leads to _inconsistencies_
5. To bring _consistency_, we often require clever design where the clients and servers have to do more work, this leads to _low performance_


### Goal for the project
To understand:
1. Working of Distributed File Systems while building a simple fault tolerant GFS.
2. Working of RPCs.

### Design Goals & Assumptions
1. To build a client, a master server and three chunk servers with design similar to GFS.


2. **Master**
    1. It will only store the metadata (mapping of files and their respective chunks) and it has be to persistent.
    2. Chunk Size will be 8 bytes and replication factor is set to 2.
    3. Instead of having only two tables, I'll be dividing the same logic into 3 tables, namely file_table, handle_table and chunk_servers, for simplicity.
    4. I'm also assuming that the master server will always work for the system to function properly. To make the system more fault tolerant 
    and deal with master server failure, shadow copy of the master has to be created, which is beyond the scope of this project.
   
3. **Client**
    1. Provide Create, Read, Append, Delete and List operations.
    2. All the heavy lifting and logic will reside in the client (creating chunks, managing connections, etc.)
    3. Since the chunk size is only 8 bytes, we'll be reading the entire chunk at a time, instead of giving byte range to be read, as done in the
    actual GFS.
    
    
4. **Chunk Server**
    1. The chunk servers will be naive (no periodic heartbeats) and they'll only be used for Reading/Writing data from disk.
    2. Data will be not cached.
    3. Their location will be stored beforehand and will be accessible by the master.
    4. All replicas are given equal priority, instead of 

6. Ability to handle faults by completing the operation in progress even if one chunk server goes down.


### Language Specifications
Due to time constraints, simplicity was favoured over a complex and more apt design, as in the actual GFS. 
So, I decided to go with Python and [RPyC](https://rpyc.readthedocs.io/en/latest/docs/theory.html#theory) instead of using something like C++ and gRPC which would've been better for learning.

### Future Work
Dynamic Chunk Servers: Right now the Chunk Servers are naive have to be manually configured so that they can be used. This can be improved upon by making chunk servers establish a connection with master and then adding its URI to the the chunk server table. This will allow building of additional features like the Heartbeat Monitor. 
