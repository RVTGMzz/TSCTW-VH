import ctypes as C,ctypes.util,struct,collections
from pathlib import Path
root=Path('/workspace/scratch/bad8e6f7b1d4')
a=C.CDLL(ctypes.util.find_library('archive'))
a.archive_read_new.restype=C.c_void_p
for name,args,ret in [('archive_read_support_format_all',[C.c_void_p],C.c_int),('archive_read_support_filter_all',[C.c_void_p],C.c_int),('archive_read_open_filename',[C.c_void_p,C.c_char_p,C.c_size_t],C.c_int),('archive_read_next_header',[C.c_void_p,C.POINTER(C.c_void_p)],C.c_int),('archive_entry_pathname',[C.c_void_p],C.c_char_p),('archive_entry_size',[C.c_void_p],C.c_longlong),('archive_read_data',[C.c_void_p,C.c_void_p,C.c_size_t],C.c_longlong),('archive_read_free',[C.c_void_p],C.c_int)]:
 f=getattr(a,name);f.argtypes=args;f.restype=ret
ar=a.archive_read_new();a.archive_read_support_format_all(ar);a.archive_read_support_filter_all(ar)
assert a.archive_read_open_filename(ar,str(root/'upload/Fonts.rar').encode(),10240)==0
ent=C.c_void_p(); dest=root/'castaway-vn/work/fonts';dest.mkdir(exist_ok=True)
while a.archive_read_next_header(ar,C.byref(ent))==0:
 name=a.archive_entry_pathname(ent).decode();size=a.archive_entry_size(ent);print(name,size)
 if size==0:continue
 p=dest/name
 assert p.resolve().is_relative_to(dest.resolve());p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('wb') as f:
  buf=C.create_string_buffer(65536)
  while True:
   n=a.archive_read_data(ar,buf,len(buf))
   if n==0:break
   assert n>0
   f.write(buf.raw[:n])
a.archive_read_free(ar)
b=(root/'upload/ui.package').read_bytes();n,o,s=struct.unpack_from('<3I',b,36)
for typ in [0,0xa2e3d533,0xe86b1eef]:
 entries=[struct.unpack_from('<5I',b,o+i*20) for i in range(n) if struct.unpack_from('<I',b,o+i*20)[0]==typ]
 for e in entries[:3]:print('ENTRY',tuple(hex(x) for x in e),repr(b[e[-2]:e[-2]+200]))
