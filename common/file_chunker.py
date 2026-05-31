#!/usr/bin/env python3
import io
import sys
import math
import os
from pathlib import Path

CHUNK_SIZE = 45 * 1024 * 1024  # 45MB, under GitHub's 50MB limit

def get_chunk_name(name, idx, num_chunks):
  return f"{name}.chunk{idx+1:02d}of{num_chunks:02d}"

def get_manifest_path(name):
  return f"{name}.chunkmanifest"

def _chunk_paths(path, num_chunks):
  return [get_manifest_path(path)] + [get_chunk_name(path, i, num_chunks) for i in range(num_chunks)]

def get_chunk_targets(path, file_size):
  num_chunks = math.ceil(file_size / CHUNK_SIZE)
  return _chunk_paths(path, num_chunks)

def chunk_file(path, targets):
  manifest_path, *chunk_paths = targets
  with open(path, 'rb') as f:
    data = f.read()
  actual_num_chunks = max(1, math.ceil(len(data) / CHUNK_SIZE))
  assert len(chunk_paths) >= actual_num_chunks, f"Allowed {len(chunk_paths)} chunks but needs at least {actual_num_chunks}, for path {path}"
  for i, chunk_path in enumerate(chunk_paths):
    with open(chunk_path, 'wb') as f:
      f.write(data[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE])
  Path(manifest_path).write_text(str(len(chunk_paths)))
  os.remove(path)

def get_existing_chunks(path):
  if os.path.isfile(path):
    return [path]
  if os.path.isfile(manifest := get_manifest_path(path)):
    num_chunks = int(Path(manifest).read_text().strip())
    return _chunk_paths(path, num_chunks)
  raise FileNotFoundError(path)

def _data_chunk_paths(path):
  manifest_path = get_manifest_path(path)
  if os.path.isfile(manifest_path):
    num_chunks = int(Path(manifest_path).read_text().strip())
    return [get_chunk_name(path, i, num_chunks) for i in range(num_chunks)]
  if os.path.isfile(path):
    return [path]
  raise FileNotFoundError(path)

def read_file_chunked(path):
  return b''.join(Path(p).read_bytes() for p in _data_chunk_paths(path))

class _ChunkedReader(io.RawIOBase):
  # presents the concatenated chunks as one read-only stream so pickle.load can
  # pull bytes on demand instead of materializing the whole file in RAM first.
  def __init__(self, paths):
    self._paths, self._idx = paths, 0
    self._f = open(self._paths[0], 'rb') if self._paths else None
  def readable(self): return True
  def readinto(self, b):
    while self._f is not None:
      n = self._f.readinto(b)
      if n: return n
      self._f.close()
      self._idx += 1
      self._f = open(self._paths[self._idx], 'rb') if self._idx < len(self._paths) else None
    return 0
  def close(self):
    if self._f is not None: self._f.close()
    self._f = None
    super().close()

def open_file_chunked(path):
  return io.BufferedReader(_ChunkedReader(_data_chunk_paths(path)))


if __name__ == "__main__":
  path = sys.argv[1]
  chunk_paths = get_chunk_targets(path, os.path.getsize(path))
  chunk_file(path, chunk_paths)
