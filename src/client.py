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
        chunks_data = [
            data[x : x + self.master.chunk_size]
            for x in range(0, len(data), self.master.chunk_size)
        ]
        chunk_servers = self.master.get_chunk_servers()

        for i in enumerate(chunk_ids):
            chunk_id = chunk_ids[i]
            chunk_loc = self.master.get_chunk_loc(chunk_id)
            chunk_servers[chunk_loc].write_data(chunk_id, chunks_data[i])

    def create(self, file_name, data):
        """Creates a File for given File Name and Data"""
        if self.master.check_exists(file_name):
            raise Exception("WRITE ERROR: File " + file_name + " already exists")

        num_chunks = self.__num_of_chunks(len(data))
        # allocating chunk ids to each chunk
        chunk_ids = self.master.alloc(file_name, num_chunks)
        self.__write_chunks(chunk_ids, data)

    def append(self, file_name, data):
        if not self.master.check_exists(file_name):
            log.info("404: file not found")
            raise Exception("APPEND ERROR: File " + file_name + " does not exist")
        num_append_chunks = self.__num_of_chunks(len(data))
        append_chunkuuids = self.master.alloc_append(file_name, num_append_chunks)
        self.__write_chunks(append_chunkuuids, data)

    def read(self, file_name):
        """
        Returns the data in the given file
        """
        # Note:GFS paper mentions that client only asks for the required chunk_servers
        # but we are getting all the chunk servers once, for simplication.

        if not self.master.check_exists(file_name):
            log.info("404: file not found")
            raise Exception("READ ERROR: File " + file_name + " does not exist")

        chunks = []
        # get all the chunk ids of the file from the master
        chunk_ids = self.master.get_chunk_ids(file_name)

        # *this can be CACHED by the client for some duration*
        chunk_servers = self.master.get_chunk_servers()
        for chunk_id in chunk_ids:
            # get the first loc id of chunk,
            # MIGHT REQUIRE CHANGES later on
            chunk_loc = self.master.get_chunk_loc(chunk_id)
            # write chunk data logic here, once you know how you're going to format the data
            chunk = chunk_servers[chunk_loc].get_data(chunk_id)
            chunks.append(chunk)

        data = functools.reduce(lambda a, b: a + b, chunks)  # reassembling in order

        return data

    def delete(self, filename):
        self.master.delete(filename)


def connect_chunk_server(loc_id):
    try:
        con = rpyc.connect(loc_id, port=8000)
        chunk_server = con.root.GFSChunkServer()
        return chunk_server
    except EnvironmentError:
        log.error("Chunk Server Not Found")
        print("Please start chunkserver.py and try again")
        sys.exit(1)


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
