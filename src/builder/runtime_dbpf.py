"""DBPF 7.1/7.2 string tables; never changes keys, language order or descriptions."""
from __future__ import annotations
from dataclasses import dataclass
import struct
from dbpf import unpack
from qfs import compress

TEXT_TYPES = {0x53545223: 'STR#', 0x43545353: 'CTSS', 0x54544173: 'TTAs'}
DIR = 0xE86B1EEF

def parse_table(raw):
    if raw[64:66] != b'\xfd\xff':
        raise ValueError('Unsupported string format')
    count = struct.unpack_from('<H', raw, 66)[0]
    rows = []; pos = 68
    for _ in range(count):
        lang = raw[pos]; pos += 1
        end = raw.index(0,pos); value = raw[pos:end].decode('utf-8','surrogateescape'); pos=end+1
        end = raw.index(0,pos); desc = raw[pos:end].decode('utf-8','surrogateescape'); pos=end+1
        rows.append([lang,value,desc])
    return rows,raw[pos:]

@dataclass(frozen=True)
class Entry:
    key: tuple[int, ...]
    offset: int
    size: int

class Package:
    def __init__(self, data: bytes):
        self.data = data
        if data[:4] != b'DBPF':
            raise ValueError('Not DBPF')
        self.count, self.index, index_size = struct.unpack_from('<3I', data, 36)
        self.width = index_size // self.count if self.count else 20
        if self.width not in (20, 24) or index_size != self.count * self.width:
            raise ValueError('Unsupported DBPF index')
        if self.index + index_size > len(data):
            raise ValueError('Index outside file')
        self.entries = []
        for j in range(self.count):
            v = struct.unpack_from('<' + 'I' * (self.width // 4), data, self.index+j*self.width)
            if v[-2] + v[-1] > len(data):
                raise ValueError(('Resource outside file', v))
            self.entries.append(Entry(v[:-2], v[-2], v[-1]))
        if len({e.key for e in self.entries}) != self.count:
            raise ValueError('Duplicate resource keys')

    def raw(self, entry):
        return unpack(self.data[entry.offset:entry.offset+entry.size])

    def tables(self):
        for e in self.entries:
            if e.key[0] in TEXT_TYPES:
                raw = self.raw(e)
                yield e, raw[:64].split(b'\0')[0].decode('utf-8','surrogateescape'), parse_table(raw)[0]

    def patch(self, replacements: dict[tuple[int, ...], bytes]):
        """Append modified resources, update their index and compressed-size directory."""
        out = bytearray(self.data)
        if replacements.keys() - {e.key for e in self.entries}:
            raise ValueError('Replacement targets a missing resource')
        if any(key[0] == DIR for key in replacements):
            raise ValueError('DIR is maintained by the writer, not by callers')
        changes = dict(replacements)
        dr_width = self.width - 4
        for e in self.entries:
            if e.key[0] != DIR:
                continue
            raw = bytearray(self.raw(e))
            if len(raw) % dr_width:
                raise ValueError('Invalid DIR record width')
            changed = False
            for pos in range(0, len(raw), dr_width):
                key = struct.unpack_from('<'+'I'*(dr_width//4-1), raw, pos)
                if key in replacements:
                    struct.pack_into('<I', raw, pos+dr_width-4, len(replacements[key]))
                    changed = True
            if changed:
                changes[e.key] = bytes(raw)
        for j,e in enumerate(self.entries):
            if e.key not in changes:
                continue
            raw = changes[e.key]
            compressed = self.data[e.offset+4:e.offset+6] == b'\x10\xfb'
            packed = compress(raw) if compressed else raw
            if unpack(packed) != raw:
                raise AssertionError('QFS round trip')
            offset = len(out)
            out.extend(packed)
            struct.pack_into('<II', out, self.index+j*self.width+self.width-8, offset, len(packed))
        result = bytes(out)
        checked = Package(result)
        assert result[:96] == self.data[:96]
        for old,new in zip(self.entries,checked.entries):
            assert old.key == new.key
            if old.key in changes:
                assert checked.raw(new) == changes[old.key]
                assert (self.data[old.offset+4:old.offset+6] == b'\x10\xfb') == (result[new.offset+4:new.offset+6] == b'\x10\xfb')
            else:
                assert old == new
                assert result[new.offset:new.offset+new.size] == self.data[old.offset:old.offset+old.size]
        return result

def encode_table(raw, rows):
    assert len(rows) == struct.unpack_from('<H',raw,66)[0]
    return raw[:68] + b''.join(bytes([lang])+value.encode('utf-8','surrogateescape')+b'\0'+desc.encode('utf-8','surrogateescape')+b'\0' for lang,value,desc in rows) + parse_table(raw)[1]
