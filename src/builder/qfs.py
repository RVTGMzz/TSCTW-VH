import struct
from collections import defaultdict,deque

def compress(raw):
 out=bytearray();hist=defaultdict(lambda:deque(maxlen=48));p=0;start=0
 def add(i):
  if i+3<=len(raw):hist[raw[i:i+3]].append(i)
 def flush(end):
  nonlocal start
  while end-start>=4:
   n=min(112,((end-start)//4)*4);out.append(0xe0+(n-4)//4);out.extend(raw[start:start+n]);start+=n
 while p<len(raw):
  best=0;dist=0
  if p+3<=len(raw):
   for prev in reversed(hist.get(raw[p:p+3],())):
    d=p-prev
    if d>131072:continue
    n=3;limit=min(1028,len(raw)-p)
    while n<limit and raw[prev+n]==raw[p+n]:n+=1
    if (n>=5 or (n>=4 and d<=16384) or (n>=3 and d<=1024)) and n>best:best=n;dist=d
    if best==limit:break
  if best:
   flush(p);lit=p-start;d=dist-1;n=best
   if n<=10 and dist<=1024:out.extend(((d>>8)<<5 | (n-3)<<2 | lit,d&255))
   elif n<=67 and dist<=16384:out.extend((0x80|(n-4),(lit<<6)|(d>>8),d&255))
   else:out.extend((0xc0|((d>>16)<<4)|(((n-5)>>8)<<2)|lit,(d>>8)&255,d&255,(n-5)&255))
   out.extend(raw[start:p])
   for i in range(p,p+n):add(i)
   p+=n;start=p
  else:add(p);p+=1
 flush(p);out.append(0xfc+p-start);out.extend(raw[start:p])
 return struct.pack('<I',len(out)+9)+b'\x10\xfb'+len(raw).to_bytes(3,'big')+out
