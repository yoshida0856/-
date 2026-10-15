"""Build the approved five-page manual and its registration links.

Run: python manuals/source/build_v5.py --output output/pdf/basis-manual-v5.0.pdf
Dependencies: PyMuPDF, Pillow. Artwork and official brand assets are retained.
"""
from pathlib import Path
from io import BytesIO
import argparse
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parent
W, H = 1672, 941
LINKS = [
    ((72, 679, 535, 768), 'https://campaign.coincheck.com/invitation?code=RzLuJLQ'),
    ((619, 679, 1060, 768), 'https://promote.mexc.com/a/VlM5ZfOs'),
    ((1140, 679, 1603, 768), 'https://basis.pro/register/IUMS4759'),
]
LOGOS = [
    ('coincheck', (380, 397, 437, 454)),
    ('mexc', (838, 400, 914, 456)),
    ('basis', (1367, 391, 1425, 458)),
]

def build(output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    for index in range(1, 6):
        image_path = ROOT / 'v5-images' / f'page-{index:02}.png'
        with Image.open(image_path) as im:
            assert im.size == (W, H), (image_path, im.size)
            stream = BytesIO()
            im.convert('RGB').save(stream, format='JPEG', quality=95, subsampling=0, optimize=True)
        page = doc.new_page(width=W, height=H)
        page.insert_image(page.rect, stream=stream.getvalue())
        if index == 5:
            for name, box in LOGOS:
                page.insert_image(fitz.Rect(box), filename=str(ROOT / 'brand-assets' / f'{name}-symbol.png'))
            for box, url in LINKS:
                page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(box), 'uri': url})
    doc.set_metadata({
        'title': '僕の資産戦略を、この一冊に。',
        'author': '投資で生活CH・井出',
        'subject': '資産配分・注目銘柄・BASISの運用と始め方',
        'creator': 'Five-page illustrated manual v5.0',
    })
    doc.set_toc([(1, title, n) for n, title in enumerate([
        '表紙', '僕のリアルな資産配分', '裏の注目銘柄',
        'BASISの運用方法と条件', '始め方・登録ページ',
    ], 1)])
    doc.save(output, garbage=4, deflate=True)
    doc.close()
    with fitz.open(output) as checked:
        assert checked.page_count == 5
        assert all(p.rect == fitz.Rect(0, 0, W, H) for p in checked)
        found = [link['uri'] for p in checked for link in p.get_links()]
        assert sorted(found) == sorted(url for _, url in LINKS)
        assert not checked.is_encrypted
        for p in checked:
            assert p.get_pixmap(matrix=fitz.Matrix(.1, .1)).width > 0
    assert output.stat().st_size < 40_000_000
    print(f'{output}: 5 pages, {output.stat().st_size:,} bytes, 3 registration links')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(ROOT.parent / 'basis-manual-v5.0.pdf'))
    build(parser.parse_args().output)
