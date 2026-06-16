from pathlib import Path
import hashlib

from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
OUT = PUBLIC / "ediz-yilmaz-portfolio.pdf"
CACHE = ROOT / ".tmp" / "portfolio-pdf-assets"
SITE_URL = "https://edyx0.github.io/"

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 38

INK = colors.HexColor("#0e0c0a")
CHAR = colors.HexColor("#1a1714")
RULE = colors.HexColor("#3a342c")
PAPER = colors.HexColor("#f5efe3")
PAPER_2 = colors.HexColor("#dcd4c2")
PAPER_3 = colors.HexColor("#a39786")
MUTED = colors.HexColor("#847b6e")
RUST = colors.HexColor("#ff5722")
MOSS = colors.HexColor("#a9c200")


def register_fonts():
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("PortfolioSans", str(font_dir / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("PortfolioSans-Bold", str(font_dir / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("PortfolioSerif", str(font_dir / "Georgia.ttf")))
    pdfmetrics.registerFont(TTFont("PortfolioSerif-Italic", str(font_dir / "Georgia Italic.ttf")))


def hex_color(value):
    return colors.HexColor(value)


def wrap_lines(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text(c, text, x, y, width, font="PortfolioSans", size=10, leading=14, color=PAPER_2, max_lines=None):
    c.setFont(font, size)
    c.setFillColor(color)
    lines = wrap_lines(text, font, size, width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and pdfmetrics.stringWidth(lines[-1] + "...", font, size) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "..."
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_label(c, text, x, y, color=RUST):
    c.setFont("PortfolioSans-Bold", 8)
    c.setFillColor(color)
    c.drawString(x, y, text.upper())


def draw_link(c, label, url, x, y, font="PortfolioSans-Bold", size=10, color=PAPER):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, label)
    w = pdfmetrics.stringWidth(label, font, size)
    c.setStrokeColor(RUST)
    c.setLineWidth(0.6)
    c.line(x, y - 2, x + w, y - 2)
    c.linkURL(url, (x, y - 3, x + w, y + size + 2), relative=0)
    return x + w


def draw_button(c, label, url, x, y, w, h, fill=RUST):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 6, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont("PortfolioSans-Bold", 10)
    text_w = pdfmetrics.stringWidth(label, "PortfolioSans-Bold", 10)
    c.drawString(x + (w - text_w) / 2, y + h / 2 - 3, label)
    c.linkURL(url, (x, y, x + w, y + h), relative=0)


def draw_chip(c, text, x, y, accent=RUST):
    font = "PortfolioSans-Bold"
    size = 8
    c.setFont(font, size)
    w = chip_width(text)
    c.setFillColor(colors.Color(accent.red, accent.green, accent.blue, alpha=0.16))
    c.roundRect(x, y, w, 18, 5, stroke=0, fill=1)
    c.setFillColor(PAPER_2)
    c.drawCentredString(x + w / 2, y + 6.3, text)
    return x + w + 7


def chip_width(text):
    return pdfmetrics.stringWidth(text, "PortfolioSans-Bold", 8) + 18


def draw_centered_chips(c, items, x, y, width, accent=RUST, gap=7, row_gap=24):
    rows = []
    current = []
    current_w = 0
    for item in items:
        item_w = chip_width(item)
        next_w = item_w if not current else current_w + gap + item_w
        if current and next_w > width:
            rows.append((current, current_w))
            current = [item]
            current_w = item_w
        else:
            current.append(item)
            current_w = next_w
    if current:
        rows.append((current, current_w))

    cy = y
    for row, row_w in rows:
        cx = x + (width - row_w) / 2
        for item in row:
            cx = draw_chip(c, item, cx, cy, accent)
        cy -= row_gap


def draw_image_cover(c, path, x, y, w, h):
    img_path = prepared_image(path, w, h, "cover")
    if not img_path:
        return
    c.drawImage(ImageReader(str(img_path)), x, y, w, h, mask="auto")


def draw_image_contain(c, path, x, y, w, h):
    img_path = prepared_image(path, w, h, "contain")
    if not img_path:
        return
    with Image.open(img_path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    sw, sh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(img_path)), x + (w - sw) / 2, y + (h - sh) / 2, sw, sh, mask="auto")


def draw_rounded_icon(c, path, x, y, size, radius=12):
    img_path = prepared_rounded_icon(path, size, radius)
    if not img_path:
        return
    c.drawImage(ImageReader(str(img_path)), x, y, size, size, mask="auto")


def prepared_rounded_icon(path, size_pt, radius_pt):
    source = PUBLIC / path.lstrip("/")
    if not source.exists():
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"{path}:{size_pt:.1f}:{radius_pt:.1f}:rounded-icon".encode()).hexdigest()[:14]
    out = CACHE / f"{key}.png"
    if out.exists():
        return out

    target = max(96, int(size_pt * 2))
    radius = int(radius_pt * 2)
    with Image.open(source) as im:
        im = im.convert("RGBA")
        im.thumbnail((target, target), Image.Resampling.LANCZOS)
        square = Image.new("RGBA", (target, target), (0, 0, 0, 0))
        square.alpha_composite(im, ((target - im.width) // 2, (target - im.height) // 2))
        mask = Image.new("L", (target, target), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, target, target), radius=radius, fill=255)
        square.putalpha(mask)
        square.save(out, "PNG", optimize=True)
    return out


def prepared_image(path, w_pt, h_pt, mode):
    source = PUBLIC / path.lstrip("/")
    if not source.exists():
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"{path}:{w_pt:.1f}:{h_pt:.1f}:{mode}".encode()).hexdigest()[:14]
    out = CACHE / f"{key}.jpg"
    if out.exists():
        return out

    target_w = max(80, int(w_pt * 2))
    target_h = max(80, int(h_pt * 2))
    with Image.open(source) as im:
        im = im.convert("RGB")
        if mode == "cover":
            src_ratio = im.width / im.height
            target_ratio = target_w / target_h
            if src_ratio > target_ratio:
                new_w = int(im.height * target_ratio)
                left = (im.width - new_w) // 2
                im = im.crop((left, 0, left + new_w, im.height))
            else:
                new_h = int(im.width / target_ratio)
                top = (im.height - new_h) // 2
                im = im.crop((0, top, im.width, top + new_h))
            im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        else:
            im.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        im.save(out, "JPEG", quality=58, optimize=True, progressive=True)
    return out


def page_bg(c, page_num, label):
    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(MARGIN, PAGE_H - 28, PAGE_W - MARGIN, PAGE_H - 28)
    c.line(MARGIN, 30, PAGE_W - MARGIN, 30)
    c.setFont("PortfolioSans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, PAGE_H - 21, "EDİZ YILMAZ / PORTFOLIO")
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 21, f"{page_num:02d} / {label}")
    draw_link(c, SITE_URL.replace("https://", "").rstrip("/"), SITE_URL, MARGIN, 15, size=8, color=PAPER_3)


APPS = [
    {
        "name": "Tabu Ekstra",
        "subtitle": "Words of 2026",
        "accent": "#9d4edd",
        "icon": "/icons/tabu-ekstra.png",
        "url": "https://apps.apple.com/app/tabu-ekstra-2026-kelimeleri/id6757464030",
        "summary": "A modern Taboo-style iOS game with 2026 word lists, offline play, and fast rounds for friends, families, and campus groups.",
        "stats": ["#18 TR Card Games", "7,000+ users", "12.23% conversion"],
        "tech": ["SwiftUI", "StoreKit 2", "RevenueCat", "AdMob", "PlayFab"],
        "shots": ["/screenshots/tabu-ekstra/1.jpg", "/screenshots/tabu-ekstra/2.jpg", "/screenshots/tabu-ekstra/3.jpg"],
    },
    {
        "name": "Imposter",
        "subtitle": "Spy at the Party",
        "accent": "#d4a356",
        "icon": "/icons/imposter.png",
        "url": "https://apps.apple.com/app/imposter-spy-at-the-party/id6761042851",
        "summary": "A single-device social deduction game built around secret words, imposter roles, clue giving, and voting.",
        "stats": ["Released May 2026", "3-8 players", "EN/TR localization"],
        "tech": ["SwiftUI", "StoreKit 2", "RevenueCat", "AdMob", "ATT"],
        "shots": ["/screenshots/imposter/1.jpg", "/screenshots/imposter/2.jpg", "/screenshots/imposter/3.jpg"],
    },
    {
        "name": "Holy Shift",
        "subtitle": "Cyber Reflex Game",
        "accent": "#ff10b4",
        "icon": "/icons/holy-shift.png",
        "url": "https://apps.apple.com/app/holy-shift-cyber-reflex-game/id6755365901",
        "summary": "A hyper-casual arcade reflex game built around color matching, neon cyberpunk visuals, and high-score chasing.",
        "stats": ["Original game mechanic", "6+ skins", "Unity/C#"],
        "tech": ["Unity 2022 LTS", "C#", "Custom shaders", "AdMob", "Firebase"],
        "shots": ["/screenshots/holy-shift/1.jpg", "/screenshots/holy-shift/2.jpg", "/screenshots/holy-shift/3.jpg"],
    },
]


def cover_page(c):
    page_bg(c, 1, "Overview")
    x = MARGIN
    y = PAGE_H - 82
    draw_label(c, "Computer Engineering / iOS / Games / AI", x, y)
    c.setFillColor(PAPER)
    c.setFont("PortfolioSerif", 48)
    c.drawString(x, y - 54, "Ediz Yılmaz")
    c.setFont("PortfolioSerif-Italic", 31)
    c.setFillColor(PAPER_3)
    c.drawString(x, y - 92, "Partial developer & full-time CS student.")
    body = (
        "Istanbul merkezli bilgisayar mühendisliği öğrencisi ve indie iOS geliştiricisiyim. "
        "SwiftUI parti oyunları, Unity arcade deneyimleri, App Store yayınlama süreçleri, "
        "LLM pipeline'ları, ürün tasarımı ve büyüme taraflarını uçtan uca sahipleniyorum."
    )
    draw_text(c, body, x, y - 132, 410, size=12, leading=17, color=PAPER_2)
    draw_button(c, "Website'i aç", SITE_URL, x, y - 223, 126, 30)
    draw_link(c, "github.com/Edyx0", "https://github.com/Edyx0", x + 150, y - 214, size=10, color=PAPER_2)
    draw_link(c, "linkedin.com/in/edizylm", "https://linkedin.com/in/edizylm/", x + 270, y - 214, size=10, color=PAPER_2)

    stats = [("3", "App Store app"), ("7K+", "Tabu Ekstra users"), ("3.88", "Yeditepe CE GPA"), ("#18", "TR Card Games")]
    sx, sy = x, 112
    for value, label in stats:
        c.setFillColor(CHAR)
        c.roundRect(sx, sy, 105, 62, 8, stroke=0, fill=1)
        c.setFillColor(RUST)
        c.setFont("PortfolioSerif", 25)
        c.drawString(sx + 14, sy + 30, value)
        c.setFillColor(PAPER_3)
        c.setFont("PortfolioSans-Bold", 8)
        c.drawString(sx + 14, sy + 14, label)
        sx += 117

    # Visual stack: product screenshots carry the website/app identity.
    base_x = 555
    draw_image_cover(c, "/tabu-ekstra/summer-words.jpg", base_x, 285, 230, 130)
    for i, (shot, yy) in enumerate([
        ("/screenshots/tabu-ekstra/1.jpg", 74),
        ("/screenshots/imposter/1.jpg", 110),
        ("/screenshots/holy-shift/1.jpg", 146),
    ]):
        xx = 510 + i * 87
        c.setFillColor(CHAR)
        c.roundRect(xx - 5, yy - 5, 82, 184, 13, stroke=0, fill=1)
        draw_image_cover(c, shot, xx, yy, 72, 174)


def apps_page(c):
    page_bg(c, 1, "Project Portfolio")
    draw_label(c, "Project Portfolio", MARGIN, PAGE_H - 72)
    c.setFillColor(PAPER)
    c.setFont("PortfolioSerif", 34)
    c.drawString(MARGIN, PAGE_H - 112, "Ediz Yılmaz projects")
    draw_text(
        c,
        "A compact, project-focused snapshot of released App Store apps, game projects, and the product/engineering decisions behind them.",
        MARGIN,
        PAGE_H - 140,
        520,
        size=11,
        leading=15,
    )

    link_x, link_y, link_w, link_h = PAGE_W - MARGIN - 230, PAGE_H - 123, 230, 58
    c.setFillColor(CHAR)
    c.roundRect(link_x, link_y, link_w, link_h, 9, stroke=0, fill=1)
    draw_label(c, "Detailed portfolio", link_x + 16, link_y + 36, RUST)
    c.setFont("PortfolioSans-Bold", 16)
    c.setFillColor(PAPER)
    c.drawString(link_x + 16, link_y + 15, "edyx0.github.io")
    c.linkURL(SITE_URL, (link_x, link_y, link_x + link_w, link_y + link_h), relative=0)

    card_w = (PAGE_W - MARGIN * 2 - 26) / 3
    x = MARGIN
    for app in APPS:
        accent = hex_color(app["accent"])
        y = 70
        c.setFillColor(CHAR)
        c.roundRect(x, y, card_w, 330, 10, stroke=0, fill=1)
        c.setFillColor(accent)
        c.rect(x, y + 326, card_w, 4, stroke=0, fill=1)
        draw_rounded_icon(c, app["icon"], x + 18, y + 258, 54, 12)
        c.setFillColor(PAPER)
        c.setFont("PortfolioSans-Bold", 16)
        c.drawString(x + 84, y + 292, app["name"])
        c.setFillColor(PAPER_3)
        c.setFont("PortfolioSans", 9)
        c.drawString(x + 84, y + 276, app["subtitle"])
        draw_text(c, app["summary"], x + 18, y + 238, card_w - 36, size=9.5, leading=13, color=PAPER_2, max_lines=4)

        yy = y + 168
        for stat in app["stats"]:
            c.setFillColor(colors.Color(accent.red, accent.green, accent.blue, alpha=0.18))
            c.roundRect(x + 18, yy, card_w - 36, 22, 5, stroke=0, fill=1)
            c.setFillColor(PAPER_2)
            c.setFont("PortfolioSans-Bold", 8.5)
            c.drawCentredString(x + card_w / 2, yy + 7.7, stat)
            yy -= 29

        draw_centered_chips(c, app["tech"], x + 18, y + 70, card_w - 36, accent)
        draw_link(c, "App Store", app["url"], x + 18, y + 18, size=9, color=PAPER)
        x += card_w + 13


def case_page(c):
    page_bg(c, 2, "Product Snapshots")
    draw_label(c, "02 / Product Snapshots", MARGIN, PAGE_H - 72)
    c.setFillColor(PAPER)
    c.setFont("PortfolioSerif", 33)
    c.drawString(MARGIN, PAGE_H - 112, "Ürün ekranları ve kararlar")

    top_y = 250
    x = MARGIN
    c.setFillColor(CHAR)
    c.roundRect(x, top_y, 358, 150, 10, stroke=0, fill=1)
    draw_label(c, "Featured", x + 18, top_y + 124, hex_color("#9d4edd"))
    c.setFillColor(PAPER)
    c.setFont("PortfolioSans-Bold", 20)
    c.drawString(x + 18, top_y + 96, "Tabu Ekstra")
    draw_text(
        c,
        "Free baseline + Ekstra Plus kelime setleri, RevenueCat ile entitlement sync, AdMob rewarded/interstitial dengesi ve PlayFab ile hafif içerik/analytics yönetimi.",
        x + 18,
        top_y + 70,
        312,
        size=9.8,
        leading=13.5,
        color=PAPER_2,
    )
    draw_image_cover(c, "/tabu-ekstra/summer-words.jpg", x + 384, top_y, 390, 150)

    phone_y = 54
    phone_w, phone_h = 76, 164
    px = MARGIN
    for app in APPS:
        accent = hex_color(app["accent"])
        c.setFillColor(PAPER)
        c.setFont("PortfolioSans-Bold", 12)
        c.drawString(px, phone_y + phone_h + 18, app["name"])
        for shot in app["shots"][:2]:
            c.setFillColor(CHAR)
            c.roundRect(px - 4, phone_y - 4, phone_w + 8, phone_h + 8, 13, stroke=0, fill=1)
            draw_image_cover(c, shot, px, phone_y, phone_w, phone_h)
            px += phone_w + 10
        c.setFillColor(accent)
        c.rect(px - 2, phone_y, 3, phone_h, stroke=0, fill=1)
        px += 22


def other_page(c):
    page_bg(c, 3, "Other Projects / Links")
    draw_label(c, "03 / Other Projects", MARGIN, PAGE_H - 72)
    c.setFillColor(PAPER)
    c.setFont("PortfolioSerif", 33)
    c.drawString(MARGIN, PAGE_H - 112, "Diğer projeler ve bağlantılar")

    left_x, right_x = MARGIN, 462
    draw_image_cover(c, "/other-projects/ayasofya/cover.png", left_x, 240, 365, 150)
    c.setFillColor(PAPER)
    c.setFont("PortfolioSans-Bold", 16)
    c.drawString(left_x, 215, "Ayasofya — Kutsal Bilgelik Taşı")
    c.setFillColor(RUST)
    c.setFont("PortfolioSans-Bold", 9)
    c.drawString(left_x, 198, "2021 / Unity / C# / BGM Gamejam 2nd Place")
    draw_text(
        c,
        "SEUK ekibiyle geliştirilen 2D pixel-art parkour. Level design ve programming taraflarını üstlendim; ilk game jam ve ilk Unity shipment deneyimim.",
        left_x,
        174,
        360,
        size=10,
        leading=14,
    )
    draw_link(c, "itch.io project", "https://edizy.itch.io/ayasofya-kutsal-bilgelik-tasi", left_x, 102, size=9, color=PAPER)

    c.setFillColor(CHAR)
    c.roundRect(right_x, 240, 320, 150, 10, stroke=0, fill=1)
    draw_image_contain(c, "/kickle/logo.jpg", right_x + 18, 300, 58, 58)
    c.setFillColor(PAPER)
    c.setFont("PortfolioSans-Bold", 16)
    c.drawString(right_x + 92, 333, "Kickle")
    c.setFillColor(PAPER_3)
    c.setFont("PortfolioSans", 9)
    c.drawString(right_x + 92, 316, "iOS / SwiftUI / work in progress")
    draw_image_contain(c, "/kickle/worldcup.png", right_x + 18, 254, 130, 44)
    draw_text(c, "World Cup dönemine yetiştirilmesi planlanan futbol trivia uygulaması; SwiftUI ve Liquid Glass denemeleri için alan açıyor.", right_x + 160, 292, 136, size=9, leading=12, max_lines=5)

    draw_label(c, "Core toolkit", right_x, 205, MOSS)
    chips = ["Swift", "SwiftUI", "Unity", "C#", "Python", "LLMs", "StoreKit 2", "RevenueCat", "AdMob", "Firebase", "PlayFab", "Figma", "Procreate", "Apple Search Ads"]
    cx, cy = right_x, 178
    for chip in chips:
        nx = draw_chip(c, chip, cx, cy, RUST)
        if nx > PAGE_W - MARGIN - 20:
            cy -= 24
            cx = right_x
            nx = draw_chip(c, chip, cx, cy, RUST)
        cx = nx

    draw_label(c, "Links", left_x, 78, RUST)
    draw_text(
        c,
        "Website: edyx0.github.io  /  GitHub: github.com/Edyx0  /  LinkedIn: linkedin.com/in/edizylm  /  Email: edizyilmaz@icloud.com",
        left_x,
        56,
        PAGE_W - MARGIN * 2,
        size=11,
        leading=15,
        color=PAPER_2,
    )


def contact_page(c):
    page_bg(c, 5, "Contact")
    x = MARGIN
    draw_label(c, "04 / Contact", x, PAGE_H - 72)
    c.setFillColor(PAPER)
    c.setFont("PortfolioSerif", 39)
    c.drawString(x, PAGE_H - 118, "Bağlantılar")
    draw_text(
        c,
        "Bu PDF sitenin kısa portfolyo özeti olarak hazırlandı. Güncel uygulamalar, detay sayfaları, gizlilik politikaları ve iletişim bilgileri için ana website üzerinden ilerleyebilirsiniz.",
        x,
        PAGE_H - 150,
        540,
        size=12,
        leading=17,
    )

    links = [
        ("Website", SITE_URL, "edyx0.github.io"),
        ("Email", "mailto:edizyilmaz@icloud.com", "edizyilmaz@icloud.com"),
        ("LinkedIn", "https://linkedin.com/in/edizylm/", "linkedin.com/in/edizylm"),
        ("GitHub", "https://github.com/Edyx0", "github.com/Edyx0"),
    ]
    y = 270
    for label, url, display in links:
        c.setFillColor(CHAR)
        c.roundRect(x, y, 480, 42, 8, stroke=0, fill=1)
        c.setFillColor(RUST)
        c.setFont("PortfolioSans-Bold", 9)
        c.drawString(x + 16, y + 24, label.upper())
        draw_link(c, display, url, x + 110, y + 20, size=11, color=PAPER)
        y -= 55

    draw_button(c, "Portfolio sitesine git", SITE_URL, x, 56, 160, 32)
    c.setFillColor(PAPER_3)
    c.setFont("PortfolioSans", 8)
    c.drawRightString(PAGE_W - MARGIN, 56, "Generated from Edyx0.github.io source content")


def build_pdf():
    register_fonts()
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("Ediz Yılmaz Portfolio")
    c.setAuthor("Ediz Yılmaz")
    c.setSubject("Website portfolio summary with project links")
    for page in [apps_page]:
        page(c)
        c.showPage()
    c.save()


if __name__ == "__main__":
    build_pdf()
    print(OUT)
