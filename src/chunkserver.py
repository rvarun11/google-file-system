import os
import rpyc
from rpyc.utils.server import ThreadedServer

DATA_DIR = os.path.expanduser("~")
DATA_DIR += "/gfs_root/"


class GFSChunkService(rpyc.Service):
    class exposed_GFSChunkServer:
        def exposed_write_data(self, chunk_id, data):
            """Writes data to the Chunk Server for given Chunk ID & Data"""
            local_filename = self.chunk_filename(chunk_id)
            with open(local_filename, "w") as file:
                file.write(data)
            # self.handle_table[chunk_id] = local_filename

        def exposed_get_data(self, chunk_id):
            """Returns data for a given Chunk ID"""
            local_filename = self.chunk_filename(chunk_id)
            with open(local_filename, "r") as file:
                data = file.read()
            return data

        def exposed_delete_data(self, chunk_id):
            """Deletes data from Chunk Server for given Chunk ID"""
            local_filename = self.chunk_filename(chunk_id)
            if not os.path.isfile(local_filename):
                return None
            os.remove(local_filename)

        def chunk_filename(self, chunk_id):
            local_filename = DATA_DIR + "/" + str(chunk_id) + ".gfs"
            return local_filename

        # def exposed_printf(self): # for testing
        #     print("Hello from Chunk Server")


def connect_to_master():
    """Code for Dynamic Chunk Servers"""


if __name__ == "__main__":
    # connect_to_master()
    print("GFSChunkServer is Running!")
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    t = ThreadedServer(GFSChunkService, port=8010)
    t.start()
