import sys
import functools
import logging
import rpyc

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class GFSClient:
    def __init__(self, master):
        self.master = master  # replace with master later

    def __num_of_chunks(self, file_size):
        """Returns the number of Chunks for given Size"""
        return (file_size // self.master.chunk_size) + (
            1 if file_size % self.master.chunk_size > 0 else 0
        )

    def __write_chunks(self, chunk_ids, data):
        """Writes data to chunk servers for given List of Chunk IDs and Data"""
        chunk_data = [
            data[x : x + self.master.chunk_size]
            for x in range(0, len(data), self.master.chunk_size)
        ]

        for i, chunk_id in enumerate(chunk_ids):
            loc_id = self.master.get_chunk_loc(chunk_id)
            # write logic to convert loc_id to url
            chunk_url = loc_id
            try:
                # loc id needs to be replaced appropriately
                con = rpyc.connect(chunk_url, port=8000)
                chunk_server = con.root.GFSChunkServer
                chunk_server.write_data(chunk_id, chunk_data[i])
                self.master.update_handle_table(chunk_id, loc_id)
            except EnvironmentError:
                log.error("Chunk Server not found")
                print("WRITE ERROR: Please start chunkserver.py and try again")
                sys.exit(1)

    def create(self, file_name, data):
        """Creates a File for given File Name and Data"""
        if self.master.check_exists(file_name):
            raise Exception("WRITE ERROR: File " + file_name + " already exists")

        num_chunks = self.__num_of_chunks(len(data))
        chunk_ids = self.master.alloc(file_name, num_chunks)
        self.__write_chunks(chunk_ids, data)

    def append(self, file_name, data):
        if not self.master.check_exists(file_name):
            log.info("404: File not found")
            raise Exception("APPEND ERROR: File " + file_name + " does not exist")
        num_append_chunks = self.__num_of_chunks(len(data))
        append_chunk_ids = self.master.alloc_append(file_name, num_append_chunks)
        self.__write_chunks(append_chunk_ids, data)

    def read(self, file_name):
        """Returns the data for the given file
        NOTE: GFS paper mentions that Client asks for an offset value with the file_name,
        but for simplication we are going to read the whole file.
        However, modifications can be made to read n number of bytes.
        """

        if not self.master.check_exists(file_name):
            log.info("404: file not found")
            raise Exception("READ ERROR: File " + file_name + " does not exist")

        chunks = []
        # get all the chunk ids of the file from the master
        chunk_ids = self.master.get_chunk_ids(file_name)

        for chunk_id in chunk_ids:
            loc_id = self.master.get_chunk_loc(chunk_id)
            # write logic to convert loc_id to url
            chunk_url = loc_id
            try:
                # loc id needs to be replaced appropriately
                con = rpyc.connect(chunk_url, port=8000)
                chunk_server = con.root.GFSChunkServer
                chunk = chunk_server.get_data(chunk_id)
                chunks.append(chunk)
            except EnvironmentError:
                log.error("Chunk Server not found")
                print("WRITE ERROR: Please start chunkserver.py and try again")
                sys.exit(1)

        data = functools.reduce(lambda a, b: a + b, chunks)  # reassembling in order

        return data

    def delete(self, file_name):
        chunk_ids = self.master.get_chunk_ids(file_name)

        for chunk_id in chunk_ids:
            loc_id = self.master.get_chunk_loc(chunk_id)
            # write logic to convert loc_id to url
            chunk_url = loc_id
            try:
                con = rpyc.connect(chunk_url, port=8000)
                chunk_server = con.root.GFSChunkServer
                chunk_server.delete_data(chunk_id)
            except EnvironmentError:
                log.error("Chunk Server not found")
                print("DELETE ERROR: Please start chunkserver.py and try again")
                sys.exit(1)

        self.master.delete(file_name)


def help_on_usage():
    print("------ Help on Usage -------")
    print("To create or overwrite: client.py filename data")
    print("To read: client.py filename")
    print("To append: client.py filename data")
    print("To delete: client.py filename")


def run(args):
    try:
        con = rpyc.connect("localhost", port=2131)
        # if this doesn't work, add () at the end
        client = GFSClient(con.root.GFSMaster)
    except EnvironmentError:
        log.info("404: GFSMaster not found")
        print("GFSMaster not found")
        print("Please start master.py and try again")
        return

    if len(args) == 0:
        help_on_usage()
        return

    if args[0] == "create":
        client.create(args[1], args[2])
    elif args[0] == "read":
        client.read(args[1])
    elif args[0] == "append":
        client.append(args[1], args[2])
    elif args[0] == "delete":
        client.delete(args[1])
    else:
        log.info("Incorrect Command")
        help_on_usage()


if __name__ == "__main__":
    run(sys.argv[1:])
