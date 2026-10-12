from pathlib import Path
from math import sin, cos, pi
import fitz

OUT=Path(__file__).resolve().parent.parent/'generated-v4';OUT.mkdir(exist_ok=True)
W,H=1280,720
NAVY='#101D30';INK='#182B41';GOLD='#D8B66D';TEAL='#087E85';MINT='#C9ECE7';PAPER='#F7F5EF';WHITE='#FFFFFF';MUTED='#687583';LINE='#DFE4E5';DARKCARD='#1B2D43';CORAL='#CB765D'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
fonts={'r':fitz.Font(fontfile=REG),'b':fitz.Font(fontfile=BOLD)}
doc=fitz.open();records=[]
URL='https://basis.pro/register/IUMS4759'
SOURCES=[
('01','サービス概要','https://docs.basis.pro/'),
('02','初回利用ガイド','https://docs.basis.pro/getting-started/first-stake-walkthrough'),
('03','ダッシュボード','https://docs.basis.pro/getting-started/dashboard'),
('04','手数料・成功報酬','https://docs.basis.pro/economics-and-rewards/performance-fee-mechanics'),
('05','解除と７日間の待機','https://docs.basis.pro/economics-and-rewards/unstaking-and-7-day-rule'),
('06','リスク開示','https://docs.basis.pro/risk-safety-and-asset-protection/risk-disclosure'),
('07','運営法人・規約','https://docs.basis.pro/legal-and-corporate/terms-of-use'),
('08','送金・ネットワーク費用','https://docs.basis.pro/getting-started/fees'),
]
def c(s):return tuple(int(s[i:i+2],16)/255 for i in (1,3,5))
def rect(p,x,y,w,h,fill,stroke=None,radius=0):
 p.draw_rect(fitz.Rect(x,y,x+w,y+h),color=c(stroke) if stroke else None,fill=c(fill) if fill else None,width=1, radius=min(radius/min(w,h),.5) if radius else None)
def line(p,x1,y1,x2,y2,col=LINE,width=1):p.draw_line((x1,y1),(x2,y2),color=c(col),width=width)
def circle(p,x,y,r,fill=None,stroke=None,width=1):p.draw_circle((x,y),r,color=c(stroke) if stroke else None,fill=c(fill) if fill else None,width=width)
def text(p,x,y,s,size=20,col=INK,font='r'):
 p.insert_text((x,y),s,fontname=font,fontsize=size,color=c(col))
 records.append(s)
def wrap(s,size,width,font='r'):
 out=[]
 for para in s.split('\n'):
  current=''
  for ch in para:
   if fonts[font].text_length(current+ch,fontsize=size)>width:
    out.append(current);current=ch
   else:current+=ch
  out.append(current)
 return out
def block(p,x,y,s,size=19,width=350,col=INK,font='r',leading=None):
 leading=leading or size*1.6
 for row in wrap(s,size,width,font):text(p,x,y,row,size,col,font);y+=leading
 return y
def tag(p,x,y,label,dark=False):
 text(p,x,y,label,12,GOLD if dark else TEAL,'b')
def page(section,dark=False):
 p=doc.new_page(width=W,height=H)
 p.insert_font(fontname='r',fontfile=REG);p.insert_font(fontname='b',fontfile=BOLD)
 rect(p,0,0,W,H,NAVY if dark else PAPER)
 rect(p,0,0,12,H,GOLD if dark else TEAL)
 tag(p,64,43,'2026  /  ASSET & LIFE',dark)
 text(p,950,43,section,12,GOLD if dark else MUTED)
 line(p,64,663,1216,663,DARKCARD if dark else LINE)
 text(p,64,689,'投資で生活CH・井出  /  THEME REVIEW 4.0',11,'#A8B6C6' if dark else MUTED)
 text(p,1178,689,f'{len(doc):02d}',13,GOLD if dark else TEAL,'b')
 return p
def title(p,kicker,heading,sub='',dark=False):
 tag(p,64,96,kicker,dark)
 text(p,64,154,heading,38,WHITE if dark else INK,'b')
 if sub:text(p,66,197,sub,18,'#B7C5D5' if dark else MUTED)
def arrow(p,x,y,length=45,col=TEAL):
 line(p,x,y,x+length,y,col,2)
 line(p,x+length,y,x+length-10,y-7,col,2);line(p,x+length,y,x+length-10,y+7,col,2)
def icon(p,kind,x,y,col=TEAL):
 if kind=='shield':
  pts=[(x,y-25),(x+25,y-15),(x+20,y+18),(x,y+33),(x-20,y+18),(x-25,y-15),(x,y-25)]
  p.draw_polyline(pts,color=c(col),width=2.5)
  line(p,x-12,y+1,x-3,y+11,col,2.5);line(p,x-3,y+11,x+14,y-10,col,2.5)
 elif kind=='wallet':
  rect(p,x-29,y-20,58,42,None,col,3);rect(p,x+3,y-7,29,18,PAPER,col,2);circle(p,x+14,y+2,2,col)
 elif kind=='calendar':
  rect(p,x-27,y-22,54,47,None,col,2);line(p,x-27,y-8,x+27,y-8,col,2)
  line(p,x-13,y-28,x-13,y-15,col,3);line(p,x+13,y-28,x+13,y-15,col,3)
  for dx in [-14,0,14]:circle(p,x+dx,y+7,2,col)
 elif kind=='growth':
  for dx,h in [(-22,20),(-3,36),(16,52)]:rect(p,x+dx,y+24-h,12,h,col)
 elif kind=='network':
  for a in range(6):
   xx=x+32*cos(a*pi/3);yy=y+32*sin(a*pi/3);line(p,x,y,xx,yy,col,1.5);circle(p,xx,yy,5,PAPER,col,2)
  circle(p,x,y,9,col)
def card(p,x,y,w,h,label,body,number='',symbol=None,dark=False):
 rect(p,x,y,w,h,DARKCARD if dark else WHITE,radius=5)
 rect(p,x,y,w,4,GOLD if dark else TEAL)
 if number:text(p,x+24,y+51,number,15,GOLD if dark else TEAL,'b')
 if symbol:icon(p,symbol,x+w-49,y+45,GOLD if dark else TEAL)
 text(p,x+24,y+104,label,26,WHITE if dark else INK,'b')
 block(p,x+24,y+148,body,18,w-48,'#C5D1DF' if dark else MUTED)
def note(p,s,x=64,y=628,width=1150,dark=False):block(p,x,y,s,12,width,'#A8B6C6' if dark else MUTED,leading=18)
def link(p,x,y,w,h,url):p.insert_link({'kind':fitz.LINK_URI,'from':fitz.Rect(x,y,x+w,y+h),'uri':url})


p=page('PERSONAL ASSET STRATEGY',True)
for r in [95,150,207]:circle(p,1010,334,r,None,'#345167',1)
for a in [.3,1.5,2.7,4,5.3]:circle(p,1010+207*cos(a),334+207*sin(a),5,GOLD)
icon(p,'shield',1010,318,GOLD)
text(p,962,409,'STRATEGY',17,GOLD,'b')
tag(p,64,126,'投資で生活CH・井出  /  2026年版',True)
text(p,60,236,'僕の資産戦略を、',60,WHITE,'b')
text(p,60,327,'この一冊に。',60,WHITE,'b')
text(p,67,411,'YouTubeでは話しきれない、その先へ。',25,'#C5D1DF')
for i,label in enumerate(['リアルな配分','注目銘柄','実際の運用']):
 x=64+i*223
 rect(p,x,489,207,78,DARKCARD,radius=4)
 text(p,x+16,538,label,24,GOLD,'b')
text(p,67,615,'資産をどう分け、何に注目し、どう運用するか。',20,'#A8B6C6')
# 02 / Actual allocation supplied by the author, not a model allocation.
p=page('01  /  MY ALLOCATION')
title(p,'僕のリアルな資産配分','現金45％。待つ余力も、戦略の一部。')
alloc=[('現金',45,TEAL,'待機資金'),('金',20,GOLD,'金価格への分散'),('PSLV',5,'#96ADB4','銀への投資'),('BTC',15,'#E2A45E','暗号資産'),('XRP',10,'#7C8CAA','暗号資産'),('ETH',5,'#426477','暗号資産')]
cx,cy,r=302,408,166
angle=-pi/2
for label,pct,col,role in alloc:
 end=angle+2*pi*pct/100
 pts=[(cx,cy)]+[(cx+r*cos(angle+(end-angle)*i/90),cy+r*sin(angle+(end-angle)*i/90)) for i in range(91)]+[(cx,cy)]
 p.draw_polyline(pts,color=c(PAPER),fill=c(col),width=2,closePath=True)
 angle=end
circle(p,cx,cy,108,PAPER)
text(p,cx-59,cy-7,'僕の配分',28,INK,'b')
text(p,cx-44,cy+34,'100%',29,TEAL,'b')
for i,(label,pct,col,role) in enumerate(alloc):
 y=249+i*55
 rect(p,570,y,646,47,WHITE,radius=3)
 circle(p,594,y+23,7,col)
 text(p,616,y+32,label,23,INK,'b')
 text(p,813,y+33,f'{pct}%',27,INK,'b')
 text(p,961,y+31,role,19,MUTED)
text(p,68,614,'僕の配分であって、全員に同じ割合を勧めるものではありません。',21,TEAL,'b')
note(p,'本人申告による現在の配分。確認日：2026年10月12日。相場や売買によって割合は変わります。',y=643)

# 03 / Publicly researched candidates; no fabricated personal conviction or holdings.
p=page('02  /  WATCHLIST IDEAS')
title(p,'動画の、その先にあるテーマ','注目銘柄の候補は「金」と「金融インフラ」。','公開情報から選んだ、比較・研究用の２候補。')
ideas=[('PAXG','金のデジタル化','金を、デジタル資産として持つ選択肢。','金価格・発行体・換金条件に注意。',GOLD,'https://www.paxos.com/paxgold'),('LINK','金融インフラ','外部データをブロックチェーンにつなぐ。','技術の採用拡大と、価格上昇は別。',TEAL,'https://docs.chain.link/getting-started/conceptual-overview')]
for i,(ticker,theme,why,risk,col,url) in enumerate(ideas):
 x=64+i*590;rect(p,x,247,562,328,WHITE,radius=5);rect(p,x,247,562,6,col)
 text(p,x+27,329,ticker,54,INK,'b')
 text(p,x+29,378,theme,26,col,'b')
 text(p,x+29,435,why,21,INK)
 text(p,x+29,488,risk,18,MUTED)
 text(p,x+29,544,'公式説明を確認する  →',16,col,'b')
 link(p,x,247,562,328,url)
note(p,'銘柄は編集上の選定案。井出氏の保有・推奨を示すものではありません。利益・値上がりは保証されません。',y=622)

# 04 / The author's actual method, described without invented returns.
p=page('03  /  MY APPROACH',True)
title(p,'僕が実際に使う運用：BASIS','値上がり以外の機会を探す。','乱高下する相場で、方向への依存を抑える運用を知る。',True)
methods=[('01','価格差などを見る','複数市場の価格差などを\n捉えることを目指す。'),('02','方向への依存を抑える','マーケットニュートラルを\n目指す、という公式設計。'),('03','同じ資産で報酬','BTCなどを同じ資産の\nstTokenに変換して運用。')]
for i,(n,h,b) in enumerate(methods):
 x=64+i*390;rect(p,x,252,370,259,DARKCARD,radius=5)
 tag(p,x+25,298,n,True);text(p,x+25,365,h,25,WHITE,'b')
 block(p,x+25,423,b,20,320,'#C5D1DF',leading=31)
text(p,65,554,'固定14 / 30 / 90 / 180日・途中解除不可・全額解除後に７日間の待機',19,GOLD,'b')
text(p,65,591,'成功報酬20%（実行コスト控除後の利益）／変換0.01%／出金0.05%／送金費用は別途',17,'#C5D1DF')
note(p,'本人申告による利用方法。仕組み・条件は公式資料の要約。元本・収益の保証なし。市場・運営・技術等のリスクあり。',y=635,dark=True)
link(p,64,611,550,39,'https://docs.basis.pro/risk-safety-and-asset-protection/risk-disclosure')
link(p,654,537,562,75,'https://docs.basis.pro/economics-and-rewards/performance-fee-mechanics')

# 05 / Clear, short next step with affiliate disclosure.
p=page('04  /  NEXT STEP',True)
tag(p,64,117,'さらに詳しく知りたい方へ',True)
text(p,61,219,'仕組みを知って、',55,WHITE,'b')
text(p,61,305,'自分で選ぶ。',55,WHITE,'b')
text(p,67,375,'費用・出金条件を確認し、自分に合うと判断したら。',22,'#C5D1DF')
rect(p,64,421,761,79,GOLD,radius=4)
text(p,92,473,'BASISの登録ページへ',29,INK,'b');arrow(p,724,461,57,INK)
link(p,64,421,761,79,URL)
rect(p,64,525,761,58,DARKCARD,radius=4)
text(p,91,564,'先に公式ドキュメントを読む  →',22,WHITE,'b')
link(p,64,525,761,58,'https://docs.basis.pro/')
circle(p,1030,354,135,None,'#345167');circle(p,1030,354,90,None,GOLD)
icon(p,'network',1030,339,GOLD);text(p,953,471,'BASIS',40,WHITE,'b')
block(p,67,617,'登録ボタンは紹介リンクです。紹介者に報酬が発生する場合があります（条件・金額は未確認）。\n公式説明の要約。運用実績・日本での必要な登録状況は独立検証していません。',12,1140,'#A8B6C6',leading=20)

vector=OUT/'basis-manual-v4.0-vector.pdf'
doc.set_metadata({'title':'僕の資産戦略を、この一冊に。｜５ページ版 v4.0','author':'投資で生活CH・井出｜レビュー版','subject':'本人申告の資産配分・銘柄候補・BASISの利用方法'})
doc.save(vector,garbage=4,deflate=True)
small=fitz.open()
for i,pg in enumerate(doc):
 px=pg.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
 dest=small.new_page(width=W,height=H)
 dest.insert_image(dest.rect,stream=px.tobytes('jpg',jpg_quality=94))
 for l in pg.get_links():
  if l.get('kind')==fitz.LINK_URI:dest.insert_link({'kind':fitz.LINK_URI,'from':l['from'],'uri':l['uri']})
 pg.get_pixmap().save(OUT/f'page-{i+1:02d}.png')
small.set_metadata(doc.metadata)
small.save(OUT/'basis-manual-v4.0.pdf',garbage=4,deflate=True)
(OUT/'text-content.txt').write_text('\n'.join(records))
print('Pages:',len(doc),'Bytes:',(OUT/'basis-manual-v4.0.pdf').stat().st_size)
