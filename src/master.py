import uuid
import rpyc
from rpyc.utils.server import ThreadedServer


class GFSMasterService(rpyc.Service):
    class exposed_GFSMaster:
        def __init__(self):
            self.num_chunk_servers = 3
            self.chunk_robin = 0  # for assigning chunk servers in order
            self.chunk_size = 8  # currently taking 8 bytes per chunk
            self.file_table = {}  # maps filename to list of chunk ids
            self.handle_table = {}  # maps chunk id to list of loc ids

            # maps loc id to Chunk Server URL
            # Master Port: 7000,
            # Chunk Servers Port: 8000, need to changed individually if running locally, for now
            self.chunk_servers = {
                "1": "https://localhost",
                "2": "https://cloud.google.com/",
                "3": "https://aws.amazon.com/",
            }

        def exposed_check_exists(self, file_name):
            """Returns True for given File Name if its exists in file_table else False"""
            return file_name in self.file_table

        def exposed_get_chunk_ids(self, file_name):
            """Returns a List of Chunk IDs for given File Name"""
            return self.file_table[file_name]

        def exposed_get_chunk_loc(self, chunk_id):
            """Returns a List of Chunk Server Loc IDs for given Chunk ID"""
            return self.handle_table[chunk_id]

        def exposed_get_chunk_servers(self):
            """Returns a List of all available Chunk Servers"""
            return self.chunk_servers

        def exposed_update_handle_table(self, chunk_id, loc_id):
            self.handle_table[chunk_id].append(loc_id)

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
            """Returns a List of Chunk UUIDs for given No. of Chunks"""
            chunk_ids = []
            for _ in range(len(num_chunks)):
                chunk_id = uuid.uuid4()
                self.handle_table[chunk_id] = self.chunk_robin
                chunk_ids.append(chunk_id)
                self.chunk_robin = (self.chunk_robin + 1) % self.num_chunk_servers

            return chunk_ids


if __name__ == "__main__":
    t = ThreadedServer(GFSMasterService, port=7000)
    t.start()
    print("GFSMaster is Running!")
