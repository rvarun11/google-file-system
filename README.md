# google-file-system
Ongoing project based on the [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf)

## Notice
- Added basic CREATE, READ, APPEND & DELETE operations
- Working on adding Remote Procedure Calls with `rpyc`
- Add folder functionality
- Add `list` command

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
