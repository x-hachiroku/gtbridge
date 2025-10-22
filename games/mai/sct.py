import struct


class Chunk:
    MAGIC = 0x40
    NAME_LEN = 19

    def __init__(self, index_bytes, sct_data):
        self.name = index_bytes[0:Chunk.NAME_LEN].decode('cp932').rstrip('\x00')
        self.offset, self.size = struct.unpack('<II', index_bytes[Chunk.NAME_LEN:Chunk.NAME_LEN+8])
        self.uk = index_bytes[Chunk.NAME_LEN+8:]

        chunk_bytes = sct_data[ self.offset : self.offset+self.size ]
        try:
            assert chunk_bytes[0] == Chunk.MAGIC, 'Invalid chunk magic'

            self.instructions_offset, first_message_offset = struct.unpack('<II', chunk_bytes[1:9])

            message_offsets_bytes = chunk_bytes[5:first_message_offset]
            self.message_offsets = [
                struct.unpack('<I', message_offsets_bytes[i:i+4])[0] for i in range(0, len(message_offsets_bytes), 4)
            ]
            assert self.message_offsets[0] > 0, 'No messages found'

            self.encoded_messages = []
            for i, offset in enumerate(self.message_offsets):
                if offset < self.message_offsets[max(0, i-1)] or offset > self.instructions_offset:
                    break

                end = chunk_bytes.find(b'\x00', offset, self.instructions_offset)
                assert end != -1, 'Missing null terminator'
                self.encoded_messages.append(chunk_bytes[offset:end])

            self.instructions_bytes = chunk_bytes[self.instructions_offset:]

        except Exception as e:
            print('Warning:', self.name, e)
            self.message_offsets = []
            self.encoded_messages = []
            self.instructions_bytes = chunk_bytes


    def get_messages(self, encoding='cp932'):
        return [mb.decode(encoding) for mb in self.encoded_messages]


    def set_messages(self, messages, encoding='cp932'):
        self.encoded_messages = [m.encode(encoding) for m in messages]


    def _get_chunk_bytes(self):
        if not self.message_offsets:
            return self.instructions_bytes

        chunk_bytes = bytearray()
        chunk_bytes += struct.pack('<BI', Chunk.MAGIC, self.instructions_offset)

        message_bytes = b'\x00'.join(self.encoded_messages) + b'\x00'
        append = (self.message_offsets[0] + len(message_bytes) > self.instructions_offset)

        if append:
            current_message_offset = self.size
        else:
            current_message_offset = self.message_offsets[0]

        for i, message in enumerate(self.encoded_messages):
            self.message_offsets[i] = current_message_offset
            current_message_offset += len(message) + 1

        chunk_bytes += struct.pack('<'+'I'*len(self.message_offsets), *self.message_offsets)

        if append:
            chunk_bytes = chunk_bytes.ljust(self.instructions_offset, b'\x00')
            chunk_bytes += self.instructions_bytes
            chunk_bytes += message_bytes
        else:
            chunk_bytes += message_bytes
            chunk_bytes = chunk_bytes.ljust(self.instructions_offset, b'\x00')
            chunk_bytes += self.instructions_bytes

        return chunk_bytes


    def get_bytes(self, offset):
        chunk_bytes = self._get_chunk_bytes()

        index_bytes = bytearray()
        index_bytes += self.name.encode('cp932').ljust(Chunk.NAME_LEN, b'\x00')
        index_bytes += struct.pack('<II', offset, len(chunk_bytes))
        index_bytes += self.uk

        return (index_bytes, chunk_bytes)


class SCT:
    MAGIC = b'\x4D\x53\x43\x0A'
    INDEX_LEN = 35

    def __init__(self, data, first_index_offset, last_index_offset):
        self.magic = data[0:4]
        assert self.magic == SCT.MAGIC, 'Invalid sct magic'

        self.size = struct.unpack('<I', data[4:8])[0]
        self.h1 = data[8:first_index_offset]

        self.chunks = []
        for index_offset in range(first_index_offset, last_index_offset+1, SCT.INDEX_LEN):
            index_bytes = data[index_offset:index_offset+SCT.INDEX_LEN]
            self.chunks.append(Chunk(index_bytes, data))

        self.h3 = data[last_index_offset+SCT.INDEX_LEN:self.chunks[0].offset]


    def to_bytes(self):
        current_chunk_offset = self.chunks[0].offset
        chunk_indexes_bytes, chunks_bytes = bytearray(), bytearray()
        for chunk in self.chunks:
            index_bytes, chunk_bytes = chunk.get_bytes(current_chunk_offset)
            chunk_indexes_bytes += index_bytes
            chunks_bytes += chunk_bytes
            current_chunk_offset += len(chunk_bytes)

        sct_bytes = bytearray()
        sct_bytes += self.magic
        sct_bytes += b'\x00\x00\x00\x00'
        sct_bytes += self.h1
        sct_bytes += chunk_indexes_bytes
        sct_bytes += self.h3
        sct_bytes += chunks_bytes
        sct_bytes[4:8] = struct.pack('<I', len(sct_bytes))
        return sct_bytes


if __name__ == '__main__':
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument('sct', type=Path)
    parser.add_argument('first_index_offset', type=lambda x: int(x,0))
    parser.add_argument('last_index_offset', type=lambda x: int(x,0))
    args = parser.parse_args()


    sct_bytes = args.sct.read_bytes()
    sct = SCT(sct_bytes, args.first_index_offset, args.last_index_offset)

    msg_count = 0
    for chunk in sct.chunks:
        messages = chunk.get_messages()
        if messages:
            msg_count += len(messages)
            print(chunk.name, len(messages), messages[:3])
        chunk.set_messages(messages)

    assert sct_bytes == sct.to_bytes(), 'SCT reconstruction failed'

    print()
    print('SCT parsed and reconstructed successfully.')
    print(f'Parsed {msg_count} messages from {len(sct.chunks)} chunks.')
