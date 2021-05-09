import sys
import functools
from urllib.parse import urlparse
import rpyc

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class GFSClient:
    def __init__(self, master):
        self.master = master
        # bringing all chunkservers at once for simplification
        # GFS design states to only reqd servers and cache them for short duration
        self.chunk_servers = self.master.get_chunk_servers()

    def __get_host_key(self, loc_id):
        items = self.chunk_servers[loc_id]
        host = items[0]
        key = items[1]
        return host, key

    def __get_host_port(self, loc_id):
        chunk_url = self.chunk_servers[loc_id]
        parsed = urlparse(chunk_url)
        host = parsed.hostname
        port = parsed.port

        return host, port

    def __num_of_chunks(self, file_size):
        """Returns the number of Chunks for given Size"""
        chunk_size = self.master.get_chunk_size()
        return (file_size // chunk_size) + (1 if file_size % chunk_size > 0 else 0)

    def __write_chunks(self, chunk_ids, data):
        """Writes data to chunk servers for given List of Chunk IDs and Data"""
        chunk_size = self.master.get_chunk_size()
        chunk_data = [data[x : x + chunk_size] for x in range(0, len(data), chunk_size)]
        for i, chunk_id in enumerate(chunk_ids):
            loc_ids = self.master.get_loc_ids(chunk_id)
            for loc_id in loc_ids:
                host, port = self.__get_host_port(loc_id)
                try:
                    con = rpyc.connect(host, port=port)
                    chunk_server = con.root.GFSChunkServer()
                    chunk_server.write_data(chunk_id, chunk_data[i])
                except EnvironmentError:
                    log.info("Cannot establish connection with Chunk Server")

        sys.exit(1)

    def create(self, file_name, data):
        """Creates a File for given File Name and Data"""
        if self.master.check_exists(file_name):
            raise Exception("Write Error: File " + file_name + " already exists")

        num_chunks = self.__num_of_chunks(len(data))
        chunk_ids = self.master.alloc(file_name, num_chunks)
        self.__write_chunks(chunk_ids, data)

    def append(self, file_name, data):
        if not self.master.check_exists(file_name):
            print("(404) File not found")
            raise Exception("Append Error: File " + file_name + " does not exist")

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
            print("(404) File not found")
            raise Exception("Read Error: File " + file_name + " does not exist")

        chunks = []
        # get all the chunk ids of the file from the master
        chunk_ids = self.master.get_chunk_ids(file_name)

        for chunk_id in chunk_ids:
            loc_ids = self.master.get_loc_ids(chunk_id)
            for loc_id in loc_ids:
                host, port = self.__get_host_port(loc_id)
                try:
                    con = rpyc.connect(host, port=port)
                    chunk_server = con.root.GFSChunkServer()
                    chunk = chunk_server.get_data(chunk_id)
                    chunks.append(chunk)
                    break
                except EnvironmentError:
                    log.info("Cannot establish connection with Chunk Server")

        data = functools.reduce(lambda a, b: a + b, chunks)  # reassembling in order

        print(data)

    def delete(self, file_name):
        """Connects with chunk servers and Deletes all the chunks of the file"""
        chunk_ids = self.master.get_chunk_ids(file_name)
        for chunk_id in chunk_ids:
            loc_ids = self.master.get_loc_ids(chunk_id)
            for loc_id in loc_ids:
                host, port = self.__get_host_port(loc_id)
                try:
                    con = rpyc.connect(host, port=port)
                    chunk_server = con.root.GFSChunkServer()
                    chunk_server.delete_data(chunk_id)
                except EnvironmentError:
                    log.info("Cannot establish connection with Chunk Server")

            self.master.delete_chunk(chunk_id)

        self.master.delete_file(file_name)
        sys.exit(1)

    def list(self):
        files = self.master.list_files()
        print("-------------- Files in the GFS --------------")
        for file in files:
            print(file)


def help_on_usage():
    print("-------------- Help on Usage --------------")
    print("-> To create or overwrite: client.py filename data")
    print("-> To read: client.py filename")
    print("-> To append: client.py filename data")
    print("-> To delete: client.py filename")


def run(args):
    try:
        # Client and Master are running on the same machine so we predefined the host
        # port should be same as MASTER_PORT in the config file
        con = rpyc.connect("localhost", port=4531)
        client = GFSClient(con.root.GFSMaster())
    except EnvironmentError:
        print("Cannot establish connection with GFSMaster")
        print("Connection Error: Please start master.py and try again")
        sys.exit(1)

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
    elif args[0] == "list":
        client.list()
    else:
        print("Incorrect Command")
        help_on_usage()


if __name__ == "__main__":
    run(sys.argv[1:])
