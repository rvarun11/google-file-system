# google-file-system
![status](https://img.shields.io/badge/status-ongoing-85a832) 

Project is based on the paper [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf)

## Notice
- Added basic CREATE, READ, APPEND & DELETE operations
- Working on adding Remote Procedure Calls with `rpyc`
- Will add later:
  - replicas of chunks across servers based on the replication factor 
  - `list` command  
  - heartbeat monitor

## Dependency
- rpyc

## Commands
- Create: `python client.py create <file_name>` 

- Read: `python client.py read <file_name> <data>`

- Append: `python client.py append <file_name> <string>`

- Delete: `python client.py delete <file_name>`

- List (coming soon): `python client.py list <prefix>`

## Demo
To be added soon
