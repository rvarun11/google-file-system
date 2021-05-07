# google-file-system
Ongoing project based on the [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf)

## Notice:
- Added basic CREATE, READ, APPEND & DELETE operations
- Working on adding Remote Procedure Calls with `rpyc`
- Will add `list` command to the commands

## Dependency
- rpyc

### Commands
- CREATE: `python client.py create <file_name>` 

- READ: `python client.py read <file_name> <data>`

- APPEND: `python client.py append <file_name> <string>`

- DELETE: `python client.py delete <file_name>`

- `python client.py list <prefix>`
    - TO BE ADDED: Lists all files whose absolute path have prefix `<prefix>`

## Demo
To be added soon
