# google-file-system
![status](https://img.shields.io/badge/status-ongoing-85a832) 

Project is based on the paper [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf)

## Changelog
- Added Create, Read, Append & Delete operations
- Working on adding Remote Procedure Calls with `rpyc`

## Future Work
- Heartbeat monitor: Master needs to regularly check for running chunk servers.
- Dynamic Chunk Servers: Right now the Chunk Servers have to be manually added to config file. This can be improved by making the chunk server establish a connection with master and then it is added to the chunk server table.
- Creating replicas of chunks across Chunk Servers, based on the replication factor (usually set to 3). The replication factor must be maintained. So if a chunk server does go down, then all its chunks must be replicated to other servers (edge cases to be handled appropriately)  

## Dependency
- rpyc

## Commands
- Create: `python client.py create <file_name>` 

- Read: `python client.py read <file_name> <data>`

- Append: `python client.py append <file_name> <string>`

- Delete: `python client.py delete <file_name>`

## Demo
To be added soon
