from pathlib import Path
import struct,json,hashlib,shutil
from dbpf import entries,unpack,strings
R=Path(__file__).resolve().parent
O=R.parent/'Castaway-Text-v05';P=O/'Payload';P.mkdir(parents=True,exist_ok=True)
translations={
'On':'Bật','Off':'Tắt','Low':'Thấp','Medium':'Vừa','High':'Cao',
'Quit':'Thoát','Save':'Lưu','Default Settings':'Mặc định','Enabled':'Bật','Disabled':'Tắt',
'Apply Changes':'Áp dụng','Back':'Trở lại','Main Menu':'Menu chính',
'Graphics/Performance Options':'Đồ họa','Color':'Màu sắc','Sim Detail':'Chi tiết Sim',
'Graphic Effects':'Hiệu ứng','Texture Detail':'Bề mặt','Sim/Object Detail':'Chi tiết',
'Reflections':'Phản chiếu','Screen Size':'Độ phân giải','Lighting':'Ánh sáng',
'Shadows':'Bóng đổ','Refresh Rate':'Tần số quét','UI Transparency':'Độ trong',
'Smooth Edges':'Khử răng cưa','Audio Options':'Âm thanh','Volume':'Âm lượng',
'Sound Effects':'Hiệu ứng','Ambient':'Môi trường','Performance':'Hiệu năng',
'Voices':'Giọng nói','Music':'Nhạc','Audio Quality':'Chất lượng','Mute':'Tắt tiếng',
'Play':'Phát','Stop':'Dừng','Speakers':'Loa',
'OK':'Đồng ý','Cancel':'Hủy','Yes':'Có','No':'Không','Retry':'Thử lại',
'Next':'Tiếp','Close':'Đóng','Exit':'Thoát',
}
base=dict(l.split('\t',1) for l in (R/'translations.tsv').read_text().splitlines() if l)
base.update(translations);translations=base
translations.update({'Audio Options':'Âm thanh','Game Options':'Trò chơi','Save & Quit':'Lưu và thoát','Quit without Saving':'Không lưu',"Don't Quit":'Chơi tiếp','Do you want to save before quitting? Any unsaved changes will be lost.':'Lưu trước khi thoát? Các thay đổi chưa lưu sẽ mất.'})
translations.update({'Catalogs Display Custom Content':'Hiện đồ tùy chỉnh','Display Custom Content Dialog at Startup':'Bảng đồ tùy chỉnh','Display Custom Content Dialog':'Bảng đồ tùy chỉnh','Edge Scrolling':'Cuộn mép','Sim While Minimized':'Chạy khi thu nhỏ','House-Specific Options':'Hộ gia đình','Lot View Options':'Hiển thị khu đất','View Distance':'Tầm nhìn','Fade Distance':'Độ mờ xa','Camera Rotation':'Xoay máy quay','Sims 1 Style':'Kiểu Sims 1','Free Will':'Tự hành động','Extra Large':'Rất lớn','Small':'Nhỏ','Large':'Lớn','Neighborhood Camera Drift':'Lướt máy quay','Snapshot Picture Quality':'Chất lượng ảnh','Maximum Video Recording Time':'Thời lượng quay','Picture In Picture Window':'Cửa sổ phụ','Live Picture in Picture':'Cửa sổ trực tiếp','Picture in Picture':'Cửa sổ phụ','Check For Updates Automatically':'Tự cập nhật','Do not connect to the Web':'Tắt kết nối mạng','Auto Centering':'Tự căn giữa'})
# Limit changes to specific, observed UI tables. Leave long game-settings labels English.
translations.update(json.loads((R/'extra05.json').read_text()))
allowed={'Options.package':set(range(128,135)),'UIText.package':{82,84,85,138,142,153,750,755},'Live.package':{130,134,136,137,138,153},'Neighborhood.package':{130,132,203,220},'Tutorial.package':set(range(1,6))}
from qfs import compress as qfs_literal
manifest=[];report=[]
master=translations.copy()
for name,ids in allowed.items():
 translations=master.copy()
 if name=='Neighborhood.package':translations['Play']='Chơi'
 b=(R/'text/Text'/name).read_bytes();new=bytearray(b);es=entries(b);indexoff=struct.unpack_from('<I',b,40)[0];changed={};changes=[]
 for n,(t,g,i,o,s) in enumerate(es):
  if t!=0x53545223 or i not in ids:continue
  raw=unpack(b[o:o+s]);rows=strings(raw);updates=0
  for row in rows:
   if row[0] in (1,2) and row[1] in translations:
    en=row[1];row[1]=translations[en];updates+=1;changes.append({'instance':i,'language':row[0],'en':en,'vi':row[1]})
  if not updates:continue
  result=raw[:68]+b''.join(bytes([l])+v.encode('utf-8','surrogateescape')+b'\0'+d.encode('utf-8','surrogateescape')+b'\0' for l,v,d in rows)
  compressed=b[o+4:o+6]==b'\x10\xfb'
  packed=qfs_literal(result) if compressed else result
  assert unpack(packed)==result
  newoff=len(new);new.extend(packed);struct.pack_into('<II',new,indexoff+n*20+12,newoff,len(packed))
  changed[(t,g,i)]=len(result)
 # Update only the decompressed length fields of changed compressed resources.
 for t,g,i,o,s in es:
  if t!=0xe86b1eef:continue
  assert s%16==0
  for j in range(o,o+s,16):
   key=struct.unpack_from('<3I',b,j)
   if key in changed:struct.pack_into('<I',new,j+12,changed[key])
 # Independent structural comparisons against original.
 assert new[:96]==b[:96]
 newes=entries(new);assert len(newes)==len(es)
 for e,e2 in zip(es,newes):
  t,g,i,o,s=e;_,_,_,o2,s2=e2;key=(t,g,i);assert e[:3]==e2[:3]
  if t==0xe86b1eef:
   assert e==e2
   for j in range(o,o+s,16):
    keydir=struct.unpack_from('<3I',b,j);assert new[j:j+12]==b[j:j+12]
    assert struct.unpack_from('<I',new,j+12)[0]==changed.get(keydir,struct.unpack_from('<I',b,j+12)[0])
  elif key not in changed:assert e==e2 and new[o:o+s]==b[o:o+s]
  else:
   oldraw,newraw=unpack(b[o:o+s]),unpack(new[o2:o2+s2]);assert oldraw[:68]==newraw[:68]
   assert unpack(new[o2:o2+s2])==newraw
   if b[o+4:o+6]==b'\x10\xfb':assert s2<len(newraw),(name,i,s2,len(newraw))
   assert (b[o+4:o+6]==b'\x10\xfb')==(new[o2+4:o2+6]==b'\x10\xfb')
   oldrows,newrows=strings(oldraw),strings(newraw);assert len(oldrows)==len(newrows)
   for oldrow,newrow in zip(oldrows,newrows):
    l,v,d=oldrow
    import re
    assert re.findall(r'%(?:\d+\$)?[-+0 #]*\d*(?:\.\d+)?[hlL]*[sdifouxXeEgGc]',v)==re.findall(r'%(?:\d+\$)?[-+0 #]*\d*(?:\.\d+)?[hlL]*[sdifouxXeEgGc]',newrow[1])
    if len(v.split('|'))>=5:assert v.split('|')[2:]==newrow[1].split('|')[2:]
    assert newrow==[l,translations.get(v,v) if l in (1,2) else v,d]
 dest=P/'TSData/Res/Text'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(new)
 manifest.append({'path':dest.relative_to(P).as_posix(),'original':hashlib.sha256((R.parent/'Castaway-Text-v04/Payload/TSData/Res/Text'/name).read_bytes() if name in ('Options.package','UIText.package') else b).hexdigest(),'patched':hashlib.sha256(new).hexdigest()})
 report.append({'file':name,'changes':changes,'changed_resources':len(changed)})
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
S=O/'Source';S.mkdir(exist_ok=True)
for f in ['build_v05.py','dbpf.py','qfs.py','translations.tsv','extra05.json','extra05.tsv','long05.py']:shutil.copy2(R/f,S/f)
(S/'translations.json').write_text(json.dumps(translations,ensure_ascii=False,indent=2))
(S/'validation.json').write_text(json.dumps({'checks':'Original header/index order/resource IDs retained; untouched resource bytes identical; original compression type retained; QFS round-trip; compression directory sizes verified; string order/count/descriptions and other languages preserved. Windows runtime not tested.','files':report},ensure_ascii=False,indent=2))
print('PASS',[(x['file'],len(x['changes']),x['changed_resources']) for x in report])
print('Unique translations',len(set(c['en'] for x in report for c in x['changes'])))
