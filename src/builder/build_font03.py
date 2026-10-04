from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from io import BytesIO
import json,hashlib,shutil
R=Path(__file__).resolve().parent; O=R.parent/'Castaway-Font03'; F=O/'Payload/TSData/Res/UI/Fonts';F.mkdir(parents=True,exist_ok=True)
old=R.parent/'Castaway-Thu-Rieng-Font-v0.1/Payload/TSData/Res/UI/Fonts'
required=set(range(0x20,0x250))|set(range(0x300,0x370))|set(range(0x1e00,0x1f00))|set(range(0x2000,0x2200))
viet=set(map(ord,'ăâđêôơưĂÂĐÊÔƠƯ'))|set(range(0x1ea0,0x1efa))
report=[];manifest=[]
for suffix in ['', '-Bold']:
 f=TTFont('/usr/share/fonts/truetype/dejavu/DejaVuSans'+suffix+'.ttf');opts=subset.Options();opts.hinting=False;opts.layout_features=[]
 ss=subset.Subsetter(options=opts);ss.populate(unicodes=required);ss.subset(f)
 gs=f.getGlyphSet(); replacements={}
 for n in f.getGlyphOrder():
  if f['glyf'][n].isComposite():
   rec=DecomposingRecordingPen(gs);gs[n].draw(rec);pen=TTGlyphPen(None);rec.replay(pen);replacements[n]=pen.glyph()
 for n,g in replacements.items():f['glyf'][n]=g
 for tag in ['GDEF','GPOS','GSUB','MATH','FFTM','kern','fpgm','prep','cvt ','gasp']:
  if tag in f:del f[tag]
 f['cmap'].tables=[t for t in f['cmap'].tables if t.format in (4,6)]
 family='Ron Castaway Sans';style='Bold' if suffix else 'Regular'
 for record in f['name'].names:
  values={1:family,2:style,3:family+' '+style+' v03',4:family+' '+style,6:'RonCastawaySans-'+style,16:family,17:style}
  if record.nameID in values:record.string=values[record.nameID].encode(record.getEncoding())
 buf=BytesIO();f.save(buf);ttf=buf.getvalue();again=TTFont(BytesIO(ttf),checkChecksums=2)
 assert viet<=set(again.getBestCmap());assert all(not again['glyf'][n].isComposite() for n in again.getGlyphOrder())
 wrapped=b'MXFN\x02bZ\0'+bytes(x^0x9d for x in b'\0'+ttf);wrapped+=b'\x9d'*((-len(wrapped))%10000)
 assert bytes(x^0x9d for x in wrapped[9:9+len(ttf)])==ttf
 name='RonVN-DejaVuSans'+suffix+'.mxf';(F/name).write_bytes(wrapped)
 report.append({'font':name,'glyph_count':len(again.getGlyphOrder()),'decomposed_glyphs':len(replacements),'bytes':len(wrapped),'cmap':[(t.platformID,t.platEncID,t.format) for t in again['cmap'].tables],'all_vietnamese_present':True})
(F/'FontStyle.ini').write_bytes((old/'FontStyle.ini').read_bytes().replace(b'DejaVu Sans',b'Ron Castaway Sans'))
for p in sorted(F.iterdir()):
 manifest.append({'path':'TSData/Res/UI/Fonts/'+p.name,'original':hashlib.sha256((old/p.name).read_bytes()).hexdigest(),'patched':hashlib.sha256(p.read_bytes()).hexdigest()})
(O/'manifest.json').write_text(json.dumps(manifest,indent=2));(O/'Source').mkdir(exist_ok=True)
(O/'Source/validation.json').write_text(json.dumps(report,indent=2));shutil.copy2(__file__,O/'Source/build_font03.py')
shutil.copy2('/usr/share/doc/fonts-dejavu-core/copyright',O/'Font-License.txt');print(report)
