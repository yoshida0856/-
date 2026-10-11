from pathlib import Path
from math import sin, cos, pi
import fitz

OUT=Path(__file__).resolve().parent.parent/'generated-v2';OUT.mkdir(exist_ok=True)
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
 text(p,64,689,'投資で生活CH・井出  /  REVIEW EDITION 2.0',11,'#A8B6C6' if dark else MUTED)
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

# 01 / Opening: strong title, abstract sculptural geometry, quiet brand.
p=page('SURVIVAL STRATEGY',True)
for xx in range(735,1270,42):
 for yy in range(95,610,42):circle(p,xx,yy,1.1,'#2A3C50')
circle(p,992,334,208,None,'#345167',1)
circle(p,992,334,168,None,'#5C6570',1)
circle(p,992,334,127,None,GOLD,2)
for a in [0.1,1.2,2.1,3.7,5.1]:circle(p,992+208*cos(a),334+208*sin(a),5,GOLD)
for i in range(7):
 pts=[(790+j*6,430+i*15+15*sin(j/9+i*.35)) for j in range(68)]
 p.draw_polyline(pts,color=c('#2F6170' if i%2 else '#4E7C80'),width=1.5)
icon(p,'shield',992,323,GOLD)
text(p,927,402,'PREPARE',19,GOLD,'b')
tag(p,64,140,'2026年版  /  資産防衛と運用の実践ガイド',True)
text(p,61,228,'資産を守る。',61,WHITE,'b')
text(p,61,311,'選択肢を広げる。',61,WHITE,'b')
block(p,66,380,'インフレに備える。資金を分ける。\n新しい運用の仕組みを、自分の基準で選ぶ。',22,650,'#BAC8D7',leading=36)
rect(p,64,496,558,68,DARKCARD,radius=3)
text(p,86,538,'生活の備え  →  資産の選び方  →  BASIS',20,GOLD,'b')
text(p,66,601,'最後の生存戦略マニュアル  /  改訂レビュー版',17,'#A8B6C6')

# 02 / Reader promise and page navigation.
p=page('READING MAP')
title(p,'この一冊で整理すること','３つの問いが、あなたの判断軸になる。','読み終えたときに、次の一歩を自分で選べるように。')
cards=[('01','いくら、残す？','毎月の生活費と、近い将来の支出。\n使う時期から必要資金を見積もる。','wallet'),('02','何に、分ける？','現預金・金・株式などの役割。\n利益と損失の両方から考える。','shield'),('03','どう、運用する？','BASISの仕組み・費用・出金条件。\n理解してから利用を検討する。','network')]
for i,(n,h,b,ico) in enumerate(cards):card(p,64+i*390,247,370,284,h,b,n,ico)
rect(p,64,555,1152,48,INK,radius=3)
text(p,87,586,'03–05  資産防衛の土台     /     06–10  運用とBASIS     /     11–13  行動・登録・確認先',17,WHITE)

# 03 / Inflation infographic.
p=page('01  /  PURCHASING POWER')
title(p,'守るのは「残高」だけではない','同じ100万円でも、買える量は変わる。','物価が上がると、現金の購買力は低下する。だから役割を分けて持つ。')
rect(p,64,245,740,332,WHITE,radius=5)
text(p,92,284,'物価が毎年３％上昇する場合の例',18,MUTED)
for idx,(label,value,col) in enumerate([('現在',100,TEAL),('５年後',86.3,GOLD)]):
 yy=329+idx*110;text(p,94,yy+28,label,22,INK,'b')
 rect(p,231,yy,510*value/100,55,col,radius=3)
 text(p,246,yy+37,f'{value:g}万円分',29,WHITE if idx==0 else INK,'b')
note(p,'仮定：税引後利息ゼロ。100万円 ÷（1.03の５乗）≈86.3万円。将来予測ではありません。',92,541,685)
text(p,854,280,'現金には、現金の役割。',23,INK,'b')
block(p,854,323,'日々の支払いと緊急時の備え。\nすぐ使える資金を残したうえで、\n長期資金の置き場所を考える。',20,350)
line(p,854,431,1190,431,GOLD,3)
block(p,854,470,'預金の保護対象・限度額は、\n金融機関と商品ごとに確認。\n「銀行なら全部同じ」と考えない。',18,355,MUTED)

# 04 / Three separate pots.
p=page('02  /  MONEY BUCKETS')
title(p,'投資を始める前に','お金を３つに分ける。判断がぶれなくなる。','使う時期が違えば、適した置き場所も違います。')
buckets=[('01','生活資金','日々の支払い・緊急時の備え','すぐ使えることを優先。\n生活費３〜６か月分を\n検討の出発点に。','wallet',TEAL),('02','予定資金','住居・教育・納税など','使う日と金額を決める。\n近い支払いに必要なお金を\n値動きの大きい投資に回さない。','calendar',GOLD),('03','長期資金','当面使わない余裕資金','値下がりを受け入れられる\n期間と金額を確認して、\n分散・運用を検討する。','growth',INK)]
for i,(n,h,sub,b,ico,col) in enumerate(buckets):
 x=64+i*390;rect(p,x,244,370,335,WHITE,radius=6);rect(p,x,244,370,7,col)
 tag(p,x+25,281,n);icon(p,ico,x+310,301,col)
 text(p,x+25,352,h,32,INK,'b');text(p,x+25,389,sub,17,MUTED)
 block(p,x+25,440,b,19,320)
note(p,'必要な備えは、収入の安定性・家族構成・支出で変わります。高金利の借入がある場合は返済も優先して検討。')

# 05 / Asset role comparison, concise reader-facing copy.
p=page('03  /  ASSET ROLES')
title(p,'「最強の資産」を探す前に','役割と弱点を、一緒に見る。','万人共通の黄金比率ではなく、自分の家計に合う組み合わせを。')
data=[('現預金','使える資金を確保','インフレ・保護範囲・金融機関の障害','wallet'),('株式・債券','成長や利息の機会','価格変動・金利変動・信用リスク','growth'),('金・銀','資産の性質を分散','価格・為替・売買差額・保管費用','shield'),('暗号資産','新しい技術への参加','大幅下落・不正アクセス・送金ミス','network')]
for i,(h,role,risk,ico) in enumerate(data):
 x=64+(i%2)*590;y=241+(i//2)*177
 rect(p,x,y,562,157,WHITE,radius=4);icon(p,ico,x+51,y+60,TEAL)
 text(p,x+104,y+49,h,26,INK,'b');text(p,x+104,y+87,role,20,TEAL,'b')
 block(p,x+104,y+123,risk,15,428,MUTED,leading=22)
note(p,'買う前に「いつ使うか」「いくら減っても困らないか」「換金条件を説明できるか」を確認。')

# 06 / Transition to structural strategies, hypothetical example clearly marked.
p=page('04  /  HOW RETURNS ARE PURSUED',True)
title(p,'運用を理解する、もう一つの視点','値上がりだけに頼らない仕組みを知る。','裁定取引は、価格差などの機会を捉える方法。利益の保証ではありません。',True)
for x,label,price in [(64,'市場 A','100,000'),(478,'市場 B','100,200')]:
 rect(p,x,262,353,190,DARKCARD,radius=5);text(p,x+27,308,label,22,GOLD,'b')
 text(p,x+27,380,price,51,WHITE,'b');text(p,x+283,379,'円',20,'#A8B6C6')
arrow(p,425,358,44,GOLD)
text(p,65,502,'価格差 200円  −  仮の費用 120円  ＝  80円',29,WHITE,'b')
note(p,'仕組みを説明するための仮定。約定・送金・価格変動・取引先の問題で損失になることもあります。',65,545,805,True)
rect(p,867,262,349,303,'#223850',radius=5)
text(p,893,313,'BASISの公式説明',22,GOLD,'b')
block(p,893,357,'価格差・資金調達率の差などを\n活用し、相場方向への依存を\n抑える運用を目指す。\n\n実際の成果は、市場環境と\n取引の実行結果に左右される。',18,297,'#D5DEEA',leading=28)
note(p,'出典：公式概要・リスク開示［01・06］。サービス提供者の説明を要約。実際の収益性の独立検証ではありません。',dark=True)

# 07 / Platform asset flow, no copied interface or fake dashboard.
p=page('05  /  INTRODUCING BASIS')
title(p,'BASISを知る','４つの対応資産、２つのウォレット。','公式ドキュメントに基づく、資金の流れの概要。')
assets=[('BTC','#D5A755'),('ETH','#7D8FA8'),('SOL','#628D88'),('PAXG','#BA974A')]
for i,(symbol,col) in enumerate(assets):
 x=120+i*165;circle(p,x,289,39,col);text(p,x-25 if len(symbol)==3 else x-33,298,symbol,22,WHITE,'b')
text(p,847,271,'BASIS',54,INK,'b')
block(p,849,313,'資産の数量を基準に、\n同じ資産のstTokenへ変換。',20,350)
rect(p,64,378,495,190,WHITE,radius=5);tag(p,90,420,'FUNDING WALLET')
text(p,90,463,'入金・保有・出金',28,INK,'b');text(p,90,507,'BTC / ETH / SOL / PAXG',23,TEAL,'b')
arrow(p,580,467,103,TEAL);text(p,584,427,'同じ資産で',14,MUTED);text(p,589,501,'数量 1 : 1',16,TEAL,'b')
rect(p,721,378,495,190,INK,radius=5);tag(p,748,420,'STAKING WALLET',True)
text(p,748,463,'ステーク・報酬の管理',28,WHITE,'b');text(p,748,507,'stBTC / stETH / stSOL / stPAXG',20,GOLD,'b')
note(p,'数量1：1は、円・ドル換算の価値や元本の保証ではありません。USDTは内部表示用で、入出金対象外。［01・02・06］')

# 08 / Five steps as a readable journey.
p=page('06  /  YOUR FIRST STAKE')
title(p,'利用の流れを先に把握する','登録から出金まで、５つのステップ。','入金前に「出口」まで確認しておく。')
stages=[('01','登録','メールの認証コードで\nログイン。'),('02','入金','BTCは専用アドレス。\n他の対応資産は\n接続ウォレットから。'),('03','変換','同じ資産のstTokenへ。\n数量１：１の変換。'),('04','運用','プール・期間を選択。\n残高と状態、推定の\n報酬を確認する。'),('05','解除・出金','期間後に全額解除。\n７日間待機して変換。\n入出金用ウォレットで\n出金する。')]
for i,(n,h,b) in enumerate(stages):
 x=64+i*234;rect(p,x,257,216,290,WHITE,radius=5)
 circle(p,x+44,307,25,TEAL if i<4 else INK);text(p,x+31,314,n,18,WHITE,'b')
 text(p,x+21,379,h,24,INK,'b');block(p,x+21,423,b,16,175,leading=27)
 if i<4:arrow(p,x+218,353,13,GOLD)
rect(p,64,572,1152,43,MINT,radius=3);text(p,83,601,'対応資産・ネットワーク・送金先を必ず照合。秘密鍵やシードフレーズを他人へ渡さない。',17,TEAL,'b')
note(p,'公式初回利用ガイドの要約［02］。実際の画面・対応条件は利用時に確認してください。',y=642)

# 09 / Terms, fees and waiting periods large and unambiguous.
p=page('07  /  TERMS BEFORE RETURNS',True)
title(p,'利回りを見る前に、条件を見る','ロック期間 ＋ ７日間の待機。','固定プールは途中解除不可。全ポジション単位で解除されます。',True)
for i,n in enumerate([14,30,90,180]):
 x=64+i*205;rect(p,x,260,186,131,DARKCARD,radius=5)
 text(p,x+24,319,str(n),47,WHITE,'b');text(p,x+122 if n<100 else x+143,320,'日',19,GOLD)
 text(p,x+24,365,'選択する固定期間',14,'#B7C5D5')
rect(p,904,260,312,131,'#3B3B37',radius=5);text(p,928,320,'＋７日',44,GOLD,'b');text(p,930,365,'解除後の必須待機期間',17,WHITE)
line(p,64,424,1216,424,'#3A4C60')
fees=[('入金','0%'),('変換','0.01%'),('出金','0.05%'),('成功報酬','20%')]
for i,(h,n) in enumerate(fees):
 x=64+i*292;tag(p,x,468,h,True);text(p,x,520,n,36,WHITE,'b')
block(p,64,561,'成功報酬は、実行コスト控除後の利益に対して報酬分配前に差し引かれると公式資料に記載。\nネットワーク費用は別途。推定報酬率は変動し、将来の利益を保証しません。',17,1140,'#C5D1DF',leading=26)
note(p,'期間・手数料・待機条件の出典［02・04・05・08］。条件は変更されるため利用時に再確認。',y=636,dark=True)

# 10 / Risk illustration that readers can immediately interpret.
p=page('08  /  KNOW THE DIFFERENCE')
title(p,'数量と価値は、別のもの','コインが増えても、評価額は下がり得る。','「マーケットニュートラル」は「リスクゼロ」という意味ではありません。')
rect(p,64,249,688,319,WHITE,radius=5)
text(p,91,291,'仕組みを理解するための仮の例',16,MUTED)
text(p,95,365,'数量',20,INK,'b');text(p,225,365,'1 BTC  →  1.05 BTC',31,TEAL,'b')
text(p,95,423,'価格',20,INK,'b');text(p,225,423,'100万円  →  70万円',31,INK,'b')
line(p,91,451,720,451,LINE)
text(p,95,512,'評価額',20,INK,'b');text(p,225,517,'100万円  →  73.5万円',34,CORAL,'b')
for i,(h,b) in enumerate([('市場リスク','資産価格・為替の変動'),('運営・技術リスク','取引先の破綻、障害、不正アクセス'),('換金リスク','固定期間・待機期間・追加処理')]):
 y=269+i*105;circle(p,813,y+4,18,INK);text(p,807,y+10,str(i+1),17,WHITE,'b')
 text(p,850,y+9,h,23,INK,'b');text(p,850,y+44,b,17,MUTED)
note(p,'この数量増加率・価格は仮定であり、BASISの予測や実績ではありません。元本・収益・即時換金は保証されません。［06・07］')

# 11 / Action checklist, less wall of text, clear next decision.
p=page('09  /  YOUR NEXT STEP')
title(p,'今日、始める準備','先に整える。納得してから進む。','登録と資金投入は別の判断。焦らず、順番を守る。')
items=[('生活の備え','生活費・予定支出・借入を確認。投資に回せる資金を分けた。'),('仕組みの理解','費用・ロック期間・７日間の待機・損失要因を説明できる。'),('利用条件の確認','居住地の利用条件、必要な登録、税務上の取扱いを確認した。'),('操作の安全性','資産・ネットワーク・送金先・メール認証の安全を確認した。')]
for i,(h,b) in enumerate(items):
 y=245+i*85;rect(p,64,y,795,72,WHITE,radius=3);rect(p,86,y+24,24,24,None,TEAL,1)
 text(p,127,y+30,h,20,INK,'b');text(p,127,y+57,b,15,MUTED)
rect(p,900,245,316,327,INK,radius=5);icon(p,'shield',1058,308,GOLD)
text(p,927,385,'チェックできない項目は、',20,WHITE,'b');text(p,927,420,'先に解消する。',28,GOLD,'b')
block(p,929,467,'不明点を残したまま、\n生活資金を入れない。\n必要なら独立した専門家へ。',18,264,'#C5D1DF',leading=30)
note(p,'本資料は一般的な学習・紹介資料です。個別の投資助言ではありません。')

# 12 / Purposeful CTA with generous breathing room, affiliate context at point of action.
p=page('10  /  EXPLORE BASIS',True)
tag(p,64,105,'次の一歩は、情報を確かめること。',True)
text(p,61,197,'自分の資産を、',54,WHITE,'b');text(p,61,272,'自分の基準で選ぶ。',54,WHITE,'b')
block(p,67,332,'BASISの公式資料で、仕組み・費用・出金条件を確認。\n理解し、自分の目的に合うと判断したら、登録ページへ。',22,765,'#C5D1DF',leading=37)
rect(p,64,452,699,81,GOLD,radius=4);text(p,93,505,'BASISの登録ページへ',28,INK,'b');arrow(p,665,493,60,INK)
link(p,64,452,699,81,URL)
text(p,67,569,URL,18,'#C5D1DF');link(p,64,545,700,34,URL)
block(p,67,601,'紹介リンクです。登録・利用により紹介者に報酬が発生する場合があります。\n報酬の有無・条件・金額は未確認です。',12,785,'#A8B6C6',leading=20)
for r in [90,135,180]:circle(p,1032,325,r,None,'#345167',1)
icon(p,'network',1032,321,GOLD)
text(p,943,477,'BASIS',45,WHITE,'b');text(p,918,520,'UNDERSTAND FIRST',15,GOLD,'b')

# 13 / Sources and review scope: references separate from promotional flow.
p=page('REFERENCE  /  VERIFIED READING')
title(p,'確認先と資料の位置づけ','根拠を確認できる資料であること。','BASIS公式ドキュメント閲覧日：2026年10月11日')
for i,(n,label,url) in enumerate(SOURCES):
 x=64+(i%2)*590;y=251+(i//2)*74
 rect(p,x,y,562,60,WHITE,radius=3);tag(p,x+17,y+26,n)
 text(p,x+58,y+26,label,18,INK,'b');text(p,x+58,y+48,'公式ドキュメントを開く  →',12,TEAL)
 link(p,x,y,562,60,url)
block(p,64,579,'公式資料の記載を要約したもので、運用実績・資産保管・認証・日本での必要な登録状況を独立検証したものではありません。\n運営主体は公式資料上、BASIS DIGITAL INFRASTRUCTURE LTD（セーシェル）。条件は利用時に必ず再確認してください。',13,1152,MUTED,leading=21)
note(p,'原資料「2026年：最後の生存戦略マニュアル」を再構成した改訂レビュー版。内容・デザインとも修正可能。',y=638)

vector=OUT/'basis-manual-v2.0-vector.pdf'
doc.set_metadata({'title':'2026年版 資産防衛と運用の実践ガイド｜改訂案 v2.0','author':'投資で生活CH・井出｜改訂レビュー版','subject':'実用ガイドとBASIS紹介・公式資料を要約'})
doc.save(vector,garbage=4,deflate=True)

# Screen-ready PDF: preserve the exact design without font-subsetting risks.
small=fitz.open()
for i,pg in enumerate(doc):
 px=pg.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
 dest=small.new_page(width=W,height=H)
 dest.insert_image(dest.rect,stream=px.tobytes('jpg',jpg_quality=94))
 for l in pg.get_links():
  if l.get('kind')==fitz.LINK_URI:dest.insert_link({'kind':fitz.LINK_URI,'from':l['from'],'uri':l['uri']})
 pg.get_pixmap(matrix=fitz.Matrix(1,1)).save(OUT/f'page-{i+1:02d}.png')
small.set_metadata(doc.metadata)
small.save(OUT/'basis-manual-v2.0.pdf',garbage=4,deflate=True)
(OUT/'text-content.txt').write_text('\n'.join(records),encoding='utf-8')
print('Designed pages:',len(doc),'PDF bytes:',(OUT/'basis-manual-v2.0.pdf').stat().st_size)
