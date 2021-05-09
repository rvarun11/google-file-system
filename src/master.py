import uuid
import signal
import pickle
import sys
import os
import rpyc
from rpyc.utils.server import ThreadedServer

from config import MASTER_PORT, CHUNK_SIZE, CHUNK_SERVERS


def int_handler(signal, frame):
    pickle.dump(
        (
            GFSMasterService.exposed_GFSMaster.file_table,
            GFSMasterService.exposed_GFSMaster.handle_table,
        ),
        open("test.img", "wb"),
    )
    sys.exit(0)


def load_fs():
    if os.path.isfile("test.img"):
        (
            GFSMasterService.exposed_GFSMaster.file_table,
            GFSMasterService.exposed_GFSMaster.handle_table,
        ) = pickle.load(open("test.img", "rb"))


class GFSMasterService(rpyc.Service):
    class exposed_GFSMaster:
        chunk_robin = 0  # for assigning chunk servers in order
        chunk_size = CHUNK_SIZE  # currently taking 8 bytes per chunk
        file_table = {}  # maps filename to list of chunk ids
        handle_table = {}  # maps chunk id to list of loc ids
        chunk_servers = CHUNK_SERVERS  # maps loc id to chunk server URL
        num_chunk_servers = len(CHUNK_SERVERS)

        def exposed_list_files(self):
            return self.file_table.keys()

        def exposed_get_chunk_size(self):
            """Returns a Chunk Size"""
            return self.__class__.chunk_size

        def exposed_check_exists(self, file_name):
            """Returns True for given File Name if its exists in file_table else False"""
            return file_name in self.__class__.file_table

        def exposed_get_chunk_ids(self, file_name):
            """Returns a List of Chunk IDs for given File Name"""
            return self.__class__.file_table[file_name]

        def exposed_get_loc_id(self, chunk_id):
            """Returns a List of Chunk Server Loc IDs for given Chunk ID"""
            return self.__class__.handle_table[chunk_id]

        def exposed_get_chunk_servers(self):
            """Returns a List of all available Chunk Servers"""
            return self.__class__.chunk_servers

        def exposed_delete_chunk(self, chunk_id):
            """Deletes Chunks for given Chunk ID"""
            del self.__class__.handle_table[chunk_id]

        def exposed_delete_file(self, file_name):
            """Deletes file for given File Name"""
            del self.__class__.file_table[file_name]
            self.print_tables()

        def exposed_alloc(self, file_name, num_chunks):
            """Returns a List of Chunk IDs for given File Name & its No. of Chunks"""
            chunk_ids = self.alloc_chunks(num_chunks)
            self.__class__.file_table[file_name] = chunk_ids

            self.print_tables()
            return chunk_ids

        def exposed_alloc_append(self, file_name, num_append_chunks):
            """XXXX"""
            append_chunk_ids = self.alloc_chunks(num_append_chunks)
            self.__class__.file_table[file_name].extend(append_chunk_ids)
            return append_chunk_ids

        def alloc_chunks(self, num_chunks):
            """Returns a List of Chunk UUIDs for given No. of Chunks
            NOTE: Each chunk_id in the handle_table is currently storing one loc_id.
            For replication, this needs to be converted to a list.
            """
            chunk_ids = []
            for _ in range(num_chunks):
                chunk_id = uuid.uuid4()
                self.__class__.handle_table[chunk_id] = self.__class__.chunk_robin
                chunk_ids.append(chunk_id)
                self.__class__.chunk_robin = (
                    self.__class__.chunk_robin + 1
                ) % self.__class__.num_chunk_servers

            return chunk_ids

        # for debugging
        def print_tables(self):
            print("\n-------------- File Table --------------")
            print(self.__class__.file_table)
            print("\n-------------- Handle Table --------------")
            print(self.__class__.handle_table)


if __name__ == "__main__":
    load_fs()
    signal.signal(signal.SIGINT, int_handler)
    print("GFSMaster is Running!")
    t = ThreadedServer(GFSMasterService, port=MASTER_PORT)
    t.start()
