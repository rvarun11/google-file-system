# google-file-system
![status](https://img.shields.io/badge/version-0.1-85a832) 

Project is based on the paper [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf).

Project Demo - https://youtu.be/LDqfd4PvoiQ

## Changelog
- Added replication factor
- Added Create, Read, Append, Delete & List operations
- Added Remote Procedure Calls with `rpyc`

## Future Work
- Dynamic Chunk Servers: Right now the Chunk Servers have to be manually added to config file. This can be improved by making the chunk server establish a connection with master and then it is added to the chunk server table.
- Heartbeat Monitor: Master needs to regularly check for running chunk servers.

## Dependency
- rpyc

## Commands
- Create: `python client.py create <file_name>` 

- Read: `python client.py read <file_name> <data>`

- Append: `python client.py append <file_name> <string>`

- Delete: `python client.py delete <file_name>`

- List: `python client.py list`


