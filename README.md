# google-file-system
Ongoing project based on the [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf)

## Notice:
    - Added basic CREATE, READ, APPEND & DELETE operations
    - Working on adding Remote Procedure Calls with `rpyc`
    - Will add `list` command to the commands

## Dependency
- rpyc

### Commands
- `python client.py create <file_name>` 
Creates a new file with given `<file_name>`
- `python client.py append <file_name> <string>`
Appends `<string>` to file `<file_name>`
- `python client.py read <file_name> <data>`
Reads `<data>` of the file `<file_name>`
- `python client.py delete <file_name>`
Deletes file `<file_name>`
- `python client.py list <prefix>`
TO BE ADDED: Lists all files whose absolute path have prefix `<prefix>`

## Demo
To be added soon
