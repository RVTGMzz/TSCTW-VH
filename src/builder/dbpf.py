import struct

def unpack(b):
 if b[4:6]!=b'\x10\xfb':return b
 size=int.from_bytes(b[6:9],'big'); p=9; out=bytearray()
 while p<len(b):
  c=b[p];p+=1
  if c<0x80:
   d=b[p];p+=1;lit=c&3;count=((c&0x1c)>>2)+3;dist=((c&0x60)<<3)+d+1
  elif c<0xc0:
   d,e=b[p:p+2];p+=2;lit=d>>6;count=(c&0x3f)+4;dist=((d&0x3f)<<8)+e+1
  elif c<0xe0:
   d,e,f=b[p:p+3];p+=3;lit=c&3;count=((c&0xc)<<6)+f+5;dist=((c&0x10)<<12)+(d<<8)+e+1
  elif c<0xfc:
   lit=((c&0x1f)<<2)+4;out.extend(b[p:p+lit]);p+=lit;continue
  else:
   lit=c&3;out.extend(b[p:p+lit]);p+=lit;break
  out.extend(b[p:p+lit]);p+=lit
  assert dist<=len(out)
  for _ in range(count):out.append(out[-dist])
 assert len(out)==size,(len(out),size)
 return bytes(out)

def entries(b):
 n,o,s=struct.unpack_from('<3I',b,36);assert s==n*20
 return [struct.unpack_from('<5I',b,o+i*20) for i in range(n)]

def strings(b):
 assert b[64:66]==b'\xfd\xff',b[:70]
 n=struct.unpack_from('<H',b,66)[0];p=68;r=[]
 for i in range(n):
  lang=b[p];p+=1;q=b.index(0,p);v=b[p:q].decode('utf-8',errors='surrogateescape');p=q+1;q=b.index(0,p);d=b[p:q].decode('utf-8',errors='surrogateescape');p=q+1;r.append([lang,v,d])
 assert p==len(b),(p,len(b))
 return r
if __name__=='__main__':
 from pathlib import Path
 import json,collections
 allrows=[]
 for f in Path('castaway-vn/work/text/Text').glob('*.package'):
  b=f.read_bytes()
  for t,g,i,o,s in entries(b):
   if t!=0x53545223:continue
   raw=unpack(b[o:o+s]); rows=strings(raw)
   for lang,v,d in rows:
    if lang==1:allrows.append(dict(file=f.name,id=i,text=v,description=d))
 Path('castaway-vn/work/english.json').write_text(json.dumps(allrows,ensure_ascii=True,indent=2))
 print(collections.Counter(r['file'] for r in allrows))
 for r in allrows:
  if r['file']=='Options.package' or (r['file']=='UIText.package' and len(r['text'])<45):print(r['file'],r['id'],repr(r['text']))
