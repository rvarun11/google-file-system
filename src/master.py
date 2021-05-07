import uuid
import rpyc
from rpyc.utils.server import ThreadedServer
import config


class GFSMasterService(rpyc.Service):
    class exposed_GFSMaster:
        def __init__(self):
            self.chunk_size = config.CHUNK_SIZE  # currently taking 8 bytes per chunk
            self.num_chunk_servers = config.NUM_CHUNK_SERVERS
            self.file_table = {}  # maps filename to list of chunk ids
            self.handle_table = {}  # maps chunk id to list of loc ids
            self.chunk_servers = config.CHUNK_SERVERS  # maps loc id to Chunk Server URL

        def exposed_check_exists(self, file_name):
            """Returns True for given File Name if its exists"""
            return True if file_name in self.file_table else False

        def exposed_get_chunk_ids(self, file_name):
            """Returns a List of Chunk IDs for given File Name"""
            return self.file_table[file_name]

        def exposed_get_chunk_loc(self, chunk_id):
            """Returns a List of Chunk Servers for given Chunk ID"""
            return self.handle_table[chunk_id]

        def exposed_get_chunk_servers(self):
            """Returns a List of all available Chunk Servers"""
            return self.chunk_servers

        def exposed_delete(self, filename):
            """TBA: Deletes file for given File Name"""

        def exposed_alloc(self, file_name, num_chunks):
            """Returns a List of Chunk IDs for given File Name & its No. of Chunks"""
            chunk_ids = self.alloc_chunks(num_chunks)
            self.file_table[file_name] = chunk_ids
            return chunk_ids

        def exposed_alloc_append(self, file_name, num_append_chunks):
            """XXXX"""
            append_chunk_ids = self.alloc_chunks(num_append_chunks)
            self.file_table[file_name].extend(append_chunk_ids)
            return append_chunk_ids

        def alloc_chunks(self, num_chunks):
            """XXXX"""
            chunk_ids = []
            for i in range(len(num_chunks)):
                chunk_id = uuid.uuid4()
                # MORE LOGIC WILL GO HERE -> about chunk robin
                chunk_ids.append(chunk_id)
                print(i)

            return chunk_ids


if __name__ == "__main__":
    t = ThreadedServer(GFSMasterService, port=config.MASTER_PORT)
    t.start()
    print("GFSMaster is Running!")
