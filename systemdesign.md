## System Design Document

### Why Big Storage is hard?
1. To improve __performance__, large systems require __sharding__
2. _Sharding_ leads to _faults_
3. To improve _fault tolerance_ we have make _replications_
4. _Replications_ leads to _inconsistencies_
5. To bring _consistency_, we often require clever design where the clients and servers have to do more work, this leads to _low persformance_


### Goal for the project
To understand:
1. Working of Distributed File Systems while building a simple fault tolerant GFS.
2. Working of RPC.

### Design Goals
1. To build a client, a master server and three chunk servers with design similar to GFS.

2. **Client**
    1. Provide Create, Read, Append, Delete and List operations.
    2. All the heavy lifting and logic will reside in the client (creating chunks, managing connections, etc.)

3. **Master**
    1. It will only store the metadata (mapping of files and their respective chunks) and it has be to persistent.
    2. Chunk Size will be 8 bytes and replication factor is set to 2.
    3. Instead of having only two tables, I'll be dividing the same logic into 3 tables, namely file_table, handle_table and chunk_servers, for simplicity.
    4. I'm also assuming that the master server will always work for the system to function properly. To make the system more fault tolerant 
    and deal with master server failure, shadow copy of the master has to be created, which is beyond the scope of this project.

4. **Chunk Server**
    1. The chunk servers will be naive (no periodic heartbeats) and they'll only be used for Reading/Writing data from disk.
    2. Data will be not cached.
    3. Their location will be stored beforehand and will be accessible by the master.

5. Ability to handle faults by completing the operation in progress even if one chunk server goes down.
