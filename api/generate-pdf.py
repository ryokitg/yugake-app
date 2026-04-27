from http.server import BaseHTTPRequestHandler
import json
ベース64をインポート
import io
from datetime import datetime

reportlab.lib.pagesizes から A4 をインポート
reportlab.pdfgen から canvas をインポート
reportlab.lib.units から mm をインポート
reportlab.pdfbaseからpdfmetricsをインポート
reportlab.pdfbase.cidfonts から UnicodeCIDFont をインポート

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

W、H = A4
海軍 = (0.06, 0.12, 0.27)
navyL = (0.12, 0.22, 0.43)
金 = (0.70, 0.57, 0.24)
白 = (1, 1, 1)
光 = (0.94, 0.95, 0.98)
暗い = (0.08, 0.10, 0.16)
灰色 = (0.40, 0.43, 0.51)

def header(c, title, sub=''):
    c.setFillColorRGB(*navy)
    c.rect(0, H-18*mm, W, 18*mm, fill=1, stroke=0)
    c.setFillColorRGB(*gold)
    c.rect(0, H-19.2*mm, W, 1.2*mm, fill=1, stroke=0)
    c.setFillColorRGB(*white)
    c.setFont('HeiseiKakuGo-W5', 13)
    c.drawString(14*mm, H-11*mm, title)
    サブの場合:
        c.setFillColorRGB(*gold)
        c.setFont('HeiseiKakuGo-W5', 7.5)
        c.drawRightString(W-14*mm, H-11*mm, sub)

def footer(c, left, right=''):
    c.setFillColorRGB(*navy)
    c.rect(0, 0, W, 11*mm, fill=1, stroke=0)
    c.setFillColorRGB(*gold)
    c.setFont('HeiseiKakuGo-W5', 7)
    c.drawString(14*mm, 4*mm, left)
    正しい場合：
        c.setFillColorRGB(0.67, 0.71, 0.80)
        c.drawRightString(W-14*mm, 4*mm, right)

def section(c, y, title):
    c.setFillColorRGB(*navy)
    c.rect(14*mm, y-1*mm, 3*mm, 7*mm, fill=1, stroke=0)
    c.setFillColorRGB(*navy)
    c.setFont('HeiseiKakuGo-W5', 10)
    c.drawString(20*mm, y+3.5*mm, title)
    c.setStrokeColorRGB(0.78, 0.80, 0.85)
    c.setLineWidth(0.3)
    c.line(14*mm, y-3*mm, W-14*mm, y-3*mm)

def generate_pdf(data, annotated_img_bytes=None):
    buf = io.BytesIO()
    c = Canvas.Canvas(buf, pagesize=A4)

    ref = data.get('ref', 'YGK-000000')
    name = data.get('name', '—')

    # ===== PAGE1: æ¸зå®šå†™çœŸã šã‚¸ã‚¸ =====
    header(c, 'æ¸¬å®šçµ æžœå†™çœŸ', ref + ' ' + name)

    annotated_img_bytes の場合:
        試す：
            img_buf = io.BytesIO(annotated_img_bytes)
            # å†™çœŸã‚’A4ã «ã £ã ±ã «ã «è¡
            img_y = 22*mm
            img_h = H - 40*mm
            img_w = W - 28*mm
            c.drawImage(img_buf, 14*mm, img_y, img_w, img_h, preserveAspectRatio=True, anchor='c')
        except Exception as e:
            c.setFillColorRGB(*light)
            c.roundRect(14*mm, 22*mm, W-28*mm, H-44*mm, 2*mm, fill=1, stroke=0)
            c.setFillColorRGB(*gray)
            c.setFont('HeiseiKakuGo-W5', 9)
            c.drawCentredString(W/2, H/2, 'å†™çœŸã ®èèngeã ¿è¾¼ã ¿ã «å¤±æ•—ã —ã ¾ã —ã Ÿ')
    それ以外：
        c.setFillColorRGB(*light)
        c.roundRect(14*mm, 22*mm, W-28*mm, H-44*mm, 2*mm, fill=1, stroke=0)
        c.setFillColorRGB(*gray)
        c.setFont('HeiseiKakuGo-W5', 9)
        c.drawCentredString(W/2, H/2, 'å†™çœŸæœènge'®å½±')

    footer(c, 'å¤§æ´ã‚¤“å…· - æ¸зå®šçµ æžœå†™çœŸ', 'å —ä»˜ç•ã Ÿã ·: ' + ref)
    c.showPage()

    # ===== PAGE2: è ·äººç”ã‚«ã «ã «ã † =====
    header(c, 'å¾¡æ‰‹åž‹ æ¸зå®šã‚«ã‚«ã‚¤ã‚¤ã‚¤ã‚¤ã‚”ã‚¹ã‚¤', 'å¤§æ´‹å¼“å…·')

    #å —ä»˜æƒ…å ±ã‚œã‚¹ã‚«ã‚¹
    c.setFillColorRGB(*light)
    c.roundRect(14*mm, H-40*mm, W-28*mm, 18*mm, 2*mm, fill=1, stroke=0)
    c.setStrokeColorRGB(*navyL)
    c.setLineWidth(0.5)
    c.roundRect(14*mm, H-40*mm, W-28*mm, 18*mm, 2*mm, fill=0, stroke=1)

    lbl、val、x について [
        ('å —ä»˜ç•ƈå ·', ref, 16*mm),
        ('å —æ³¨æ—¥', data.get('date', datetime.now().strftime('%Y/%m/%d')), 72*mm),
        ('å¼“æ‰‹', data.get('bowhand', 'â€—'), 132*mm),
        ('å¼ã ®ç¨®é¡ž', data.get('string', 'â€”'), 163*mm),
    ]:
        c.setFillColorRGB(*グレー); c.setFont('平成角碁-W5', 6.5)
        c.drawString(x, H-28*mm, lbl)
        c.setFillColorRGB(*dark); c.setFont('平成角碁-W5', 11)
        c.drawString(x, H-37*mm, val)

    # ã Šå®¢æ§˜æƒ…å ±
    セクション(c、H-48*mm、'ã Šå®¢æ§˜æƒ…å ±')
    cw = (W-28*mm)/3
    情報 = [
        [('æ‰€å±ž', data.get('所属','â€”')), ('ã Šå å® ', 名前), ('æ€§åˆ¥ã‚»å¹´é½¢', data.get('性別','â€”')+' / '+data.get('年齢','â€”')+'æ³')],
        [('èº«é•·', data.get('height','â€—')+'cm'), ('ä½“é‡ ', data.get('weight','â€—')+'kg'), ('å¼“åŠ›', data.get('strength','â€—')+'kg')],
    ]
    y2 = H-61*mm
    for row in info:
        for i, (lbl, val) in enumerate(row):
            x = 14*mm + i*cw
            c.setFillColorRGB(*グレー); c.setFont('平成角碁-W5', 6.5)
            c.drawString(x+1*mm, y2+5*mm, lbl)
            c.setFillColorRGB(*dark); c.setFont('平成角碁-W5', 10)
            c.drawString(x+1*mm, y2, val)
            c.setStrokeColorRGB(0.82, 0.84, 0.88); c.setLineWidth(0.2)
            c.line(x, y2-2*mm, x+cw-2*mm, y2-2*mm)
        y2 -= 14*mm

    # æ¸¬å®šå€¤
    section(c, y2+2*mm, 'æ¸¬å®šå€¤')
    c.setStrokeColorRGB(*gold); c.setLineWidth(0.5)
    c.line(14*mm, y2-1*mm, W-14*mm, y2-1*mm)

    グループ = [
        ('æā‡ã ®é•·ã •', [
            ('ä¸æŒ‡', data.get('f_middle','â€—')), ('è–¬æŒ‡', data.get('f_ring','â€—')),
            ('äººå·®ã —æā‡', data.get('f_index','â€”')), ('èŠšæŠš‡', data.get('f_thumb','â€”')),
        ]),
        ('æā‡ã ®å¤ã ã •', [
            ('ä¸æŠā‡ çзДäºāé–¢ç￣€', data.get('t_middle','â€”')), ('è–зæŠš‡ çзДäºāé–¢ç￣€', data.get('t_ring','â€”')),
            ('äº˜å·®ã —æŠ¢‡ çзьäºŠãé–¢ç￣€', data.get('t_index','â€”')), ('è¢ç¢çā‡ é–¢ç￣€', data.get('t_thumb','â€”')),
        ]),
        ('æ‰‹å…¨ä½“', [
            ('æŠ¹ã ®å¹…', data.get('h_width','â€”')), ('æŠ¹ã ®å'¨å›²', data.get('h_around','â€”')),
            ('æŠ¹ã ®å¹³ã ®é•·ã •', data.get('h_length','â€”')), ('æŠ¤ã ã ®å¤¹ã •', data.get('h_wrist','â€”')),
        ]),
    ]
    y4 = y2-10*mm
    gi、(gname、items) の列挙(groups)について：
        x = 14*mm + gi*cw
        c.setFillColorRGB(*navyL); c.rect(x, y4, cw-2*mm, 6.5*mm, fill=1, stroke=0)
        c.setFillColorRGB(*白); c.setFont('平成角碁-W5', 7.5)
        c.drawString(x+2*mm, y4+2*mm, gname)
        ji、(lbl、val) について、enumerate(items) で以下を実行します。
            yy = y4-(ji+1)*12*mm
            c.setFillColorRGB(*グレー); c.setFont('平成角碁-W5', 6.5)
            c.drawString(x+2*mm, yy+5*mm, lbl)
            c.setFillColorRGB(*dark); c.setFont('平成角碁-W5', 13)
            v = str(val)+' cm' if val and val != 'â€—' else 'â€—'
            c.drawString(x+2*mm, yy, v)
            c.setStrokeColorRGB(0.82, 0.85, 0.90); c.setLineWidth(0.2)
            c.line(x, yy-2*mm, x+cw-3*mm, yy-2*mm)

    # ä»•ä¸Šã 'äºˆå®šæ—¥
    y5 = y4-55*mm
    c.setFillColorRGB(*light)
    c.roundRect(14*mm, y5-2*mm, W-28*mm, 16*mm, 2*mm, fill=1, stroke=0)
    c.setFillColorRGB(*グレー); c.setFont('平成角碁-W5', 7)
    c.drawString(17*mm, y5+9*mm, 'ä»•ä¸Šã 'äºˆå®šæ—¥')
    c.setFillColorRGB(*dark); c.setFont('平成角碁-W5', 11)
    c.drawString(17*mm, y5+2*mm, 'ã€€ã€€ã€€å¹´ã€€ã€€æœˆã€€ã€€æ—¥')

    # কারিকিনিত
    y6 = y5-20*mm
    セクション(c, y6, 'å‚™è€ƒã «ç``¹è¨˜äº‹é …')
    c.setFillColorRGB(*light)
    c.roundRect(14*mm, y6-14*mm, W-28*mm, 12*mm, 2*mm, fill=1, stroke=0)
    c.setFillColorRGB(0.24, 0.25, 0.32); c.setFont('平成角碁-W5', 8.5)
    c.drawString(17*mm, y6-7*mm, data.get('note', 'ã ªã —'))

    footer(c, 'å¤§æ´ã‚¤ã “å…· - å¾¡æ‰‹åž‹æ¸¸å®šã‚«ã‚«ã‚¹ã‚¹ã‚¤ã‚¤ã‚¤ã‚¤ã‚¤ã‚¤', 'å —ä»˜ç•ã‚¤ã Ÿ: '+ref)
    c.showPage()

    # ===== PAGE3: ã Šå®¢æ§˜æŽ§ã ˆ =====
    header(c, 'å¾¡æ‰ã ã žã ã ¸ãå®šæŽ§ã ˆ', 'å¤§æ´‹å¼“å…·')

    c.setFillColorRGB(*light)
    c.roundRect(14*mm, H-40*mm, W-28*mm, 18*mm, 2*mm, fill=1, stroke=0)
    c.setFillColorRGB(0.24, 0.25, 0.32); c.setFont('平成角碁-W5', 8.5)
    c.drawString(18*mm, H-27*mm, 'ã “ã ®å˜ã «ã ã ¾ã ™ã€‚')
    c.drawString(18*mm, H-34*mm, 'ä»¥ä¸‹ã ®æ¸зå®šã «ã‚¿ã‚’å —ã 'ä»˜ã 'ã ¾ã —ã Ÿã€‚ä»•ä¸Šã ã ã‚Šã ¾ã §ã —ã °ã‚Šã ã Šå¾…ã ¡ ã ã •ã «ã€‚')

    c.setFillColorRGB(*ネイビー); c.setFont('平成角碁-W5', 8)
    c.drawString(14*mm, H-48*mm, 'å —ä»˜ç•ªå ·')
    c.setFillColorRGB(*navyL); c.setFont('平成角碁-W5', 20)
    c.drawString(14*mm, H-60*mm, ref)
    c.setFillColorRGB(*グレー); c.setFont('平成角碁-W5', 7.5)
    c.drawString(14*mm, H-66*mm, 'å —ä»˜æ—¥: '+data.get('date', datetime.now().strftime('%Y/%m/%d')))
    c.setStrokeColorRGB(0.78, 0.80, 0.85); c.setLineWidth(0.4)
    c.line(14*mm, H-70*mm, W-14*mm, H-70*mm)

    c.setFillColorRGB(*dark); c.setFont('平成角碁-W5', 9)
    c.drawString(14*mm, H-78*mm, 'ã Šå å‰ : '+name)
    c.drawString(14*mm, H-87*mm, 'æ‰€å±ž: '+data.get('belong','â€—'))
    c.drawString(14*mm, H-96*mm, 'å¼“æ‰‹: '+data.get('bowhand','â€—')+'ã€€å¼¦: '+data.get('string','â€—'))
    c.line(14*mm, H-100*mm, W-14*mm, H-100*mm)

    # ç°¡æ˜“æ¸зå®šå€¤
    c.setFillColorRGB(*ネイビー); c.setFont('平成角碁-W5', 9)
    c.drawString(14*mm, H-108*mm, 'æ¸¬å®šå€¤')
    シンプル = [
        ('ä¸æŒ‡ã ®é•·ã •', data.get('f_middle','â€—'), 'è–¬æŒ‡ã ®é•·ã •', data.get('f_ring','â€—')),
        ('äººå·®ã —æŠ¿‡ã ®é•·ã •', data.get('f_index','â€”'), 'è¿è¿ã‚®ã ®é•·ã •', data.get('f_thumb','â€”')),
        ('æŠ¹ã ®å¹…', data.get('h_width','â€”'), 'æŠ¹ã ®å¹³ã ®é•·ã •', data.get('h_length','â€”')),
        ('æ‰‹ã ®å'¨å›²', data.get('h_around','â€—'), 'æ‰‹é¦–ã ®å¤ªã •', data.get('h_wrist','â€—')),
    ]
    y7 = H-120*mm
    l1、v1、l2、v2 をシンプルに表すと次のようになります。
        c.setFillColorRGB(*グレー); c.setFont('平成角碁-W5', 6.5)
        c.drawString(14*mm, y7+4*mm, l1); c.drawString(W/2, y7+4*mm, l2)
        c.setFillColorRGB(*dark); c.setFont('平成角碁-W5', 11)
        v1s = str(v1)+' cm' if v1 and v1!='â€—' else 'â€—'
        v2s = str(v2)+' cm' if v2 and v2!='â€—' else 'â€—'
        c.drawString(14*mm, y7, v1s); c.drawString(W/2, y7, v2s)
        c.setStrokeColorRGB(0.82, 0.85, 0.90); c.setLineWidth(0.2)
        c.line(14*mm, y7-2*mm, W-14*mm, y7-2*mm)
        y7 -= 13*mm

    # ä»•ä¸Šã 'ä˝œå®šæŠ€
    c.setFillColorRGB(*light)
    c.roundRect(14*mm, y7-8*mm, W-28*mm, 18*mm, 2*mm, fill=1, stroke=0)
    c.setFillColorRGB(*グレー); c.setFont('平成角碁-W5', 7)
    c.drawString(17*mm, y7+5*mm, 'ä»•ä¸Šã 'äºˆå®šæ—¥')
    c.setFillColorRGB(*dark); c.setFont('平成角碁-W5', 12)
    c.drawString(17*mm, y7-2*mm, 'ã€€ã€€ã€€å¹´ã€€ã€€æœˆã€€ã€€æ—¥ã€€é ã ')

    c.setFillColorRGB(*navy); c.rect(0, 0, W, 13*mm, fill=1, stroke=0)
    c.setFillColorRGB(*ゴールド); c.setFont('平成角碁-W5', 8)
    c.drawString(14*mm, 8*mm, 'å¤§æ´‹å¼“å…·')
    c.setFillColorRGB(0.67, 0.71, 0.80); c.setFont('平成角碁-W5', 6)
    c.drawString(14*mm, 3*mm, 'ã€'006-0022 å ã€ æµ·é “æœå¹Šã ¸ã‚æŠœå¹ã‚¸ã æŠ¸ã ®ã‚¤ã‚¤ã‚¤ã‚¤ã‚¿ (011)681-8420')

    c.showPage()
    c.保存()
    buf.seek(0)
    return buf.read()


クラスハンドラー(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        試す：
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))

            data = body.get('data', {})
            img_b64 = body.get('image', None)

            img_bytes = なし
            img_b64の場合：
                # data:image/jpeg;base64,... ã ®å½¢å¼ ã «å¯¾å¿œ
                if ',' in img_b64:
                    img_b64 = img_b64.split(',')[1]
                img_bytes = base64.b64decode(img_b64)

            pdf_bytes = generate_pdf(data, img_bytes)
            pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'pdf': pdf_b64}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
