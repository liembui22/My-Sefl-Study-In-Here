#!/usr/bin/env python3
"""
render_infographic.py (v2) — Render carousel NaiGym thành ảnh PNG đúng brand,
tự kiểm lỗi chữ (tràn khung, đè nhau, chữ quá nhỏ, viết tắt khó hiểu, emoji)
và xuất theo cấu trúc thư mục reel-NN/ sẵn để đăng.

KHÔNG cần internet: font Be Vietnam Pro, Anton, Dancing Script đóng gói sẵn trong
scripts/assets/fonts/; logo tự tìm ở .claude/domains/brand/assets/ (dò ngược thư mục).

## Cách dùng nhanh

    python render_infographic.py --demo --out-dir output/            # carousel mẫu
    python render_infographic.py --config carousel.json --out-dir output/
    python render_infographic.py --config batch.json --out-dir "Reel infographic/"   # theo lô
    python render_infographic.py --config batch.json --lint-only     # chỉ soát chữ, không render

Tuỳ chọn hay dùng: --strict (lỗi QA → exit 1), --scale 2 (ảnh nét gấp đôi),
--start 81 (số reel bắt đầu; mặc định tự nối tiếp reel-NN lớn nhất đã có trong out-dir),
--no-sheet (không xuất ảnh tổng quan _tong-quan.png).

## Định dạng JSON

Một carousel:
{
  "platform": {"width": 1080, "height": 1080},     // xem references/platform-specs.md
  "title": "Đau nhức sau tập",                      // dùng cho _danh-sach.txt
  "caption": "Hook lại...\\n\\n#naigymvietnam",      // ghi ra caption.txt
  "slides": [ {...hook...}, {...value...}, {...cta...} ]
}

Theo lô: { "platform": {...}, "carousels": [ {title, caption, slides}, ... ] }
→ mỗi carousel ra một thư mục reel-NN/ gồm slide-1.png… + caption.txt.

Đánh dấu chữ trong mọi trường text:  **đậm**   [[tô vàng nhấn mạnh]]   \\n = xuống dòng

### Slide "hook"  (layout: poster | photo | split | question | chat | versus)
  {"type":"hook","layout":"photo","image":"anh/img037.jpg",
   "kicker":"BẠN CÓ TỪNG NGHĨ","headline":"Đau nhức sau tập = [[tập hiệu quả]]?",
   "subline":"Sự thật đứng sau cơn đau cơ"}
  chat:    "messages":[{"from":"member","text":"..."},{"from":"gym","text":"..."}]
  versus:  "left":"Nước dừa", "right":"Nước điện giải"

### Slide "value"  (format: checklist | comparison | radial | myth-bust | timeline | stat | grid | flow)
  checklist  : "heading", "items":[{"title","desc"}]                (≤5)
  comparison : "heading", "columns":[{"label","text"}]              (3 cột Good/Better/Best)
  radial     : "center_label", "branches":[{"icon","label","desc"}] (≤6, icon là TÊN icon, không emoji)
  myth-bust  : "myth", "truth", "mechanism"
  timeline   : "heading", "steps":[{"label":"24–72 GIỜ","title","desc"}]   (≤4)
  stat       : "kicker", "number":"20–30%", "label", "desc"
  grid       : "heading", "items":[{"icon","title","desc"}]         (4 hoặc 6 ô)
  flow       : "question", "yes":{"title","desc"}, "no":{"title","desc"}, "note"
  Mọi value slide nhận thêm "note" (dòng chú thích cuối) và "theme": dark|light|yellow.

### Slide "cta"  (layout: split | band | solid)
  {"type":"cta","layout":"split","image":"anh/img085.jpg",
   "headline":"Lớn trước, nhỏ sau.","cta_text":"Nhắn NaiGym để được xem giáo án",
   "channel":"dm_zalo","hashtags":"#naigymvietnam"}

### Slide cần ảnh chụp thật nhưng chưa có ảnh
  {"photo_brief":"PT đang chỉnh form squat cho hội viên, góc ngang hông"}

Icon có sẵn (dùng tên): check, x, alert, moon, sun, dumbbell, heart, clock, drop, fire,
brain, leaf, chat, link, arrow, star, users, scale, bolt, pause, stretch, hand, food, bed, chart
"""

import argparse
import base64
import html
import json
import math
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
FONTS_DIR = os.path.join(SCRIPT_DIR, "assets", "fonts")

# ---------- Brand (đồng bộ domains/brand/brand-identity.md) ----------
YELLOW = "#FFD10C"
ORANGE = "#F59322"
CHARCOAL = "#232323"
DEEP = "#141414"
WHITE = "#FFFFFF"
LIGHT = "#F2F0EB"      # nền sáng phụ (trắng ngà) — dịu mắt hơn trắng tinh trên feed
MUTED = "#9A9A9A"
CARD_DARK = "#2E2E2E"

THEMES = {
    "dark":   {"bg": CHARCOAL, "fg": "#F5F3EE", "sub": "#CFCBC4", "card": CARD_DARK, "card_fg": "#F5F3EE", "accent": YELLOW, "muted": MUTED},
    "deep":   {"bg": DEEP, "fg": "#F5F3EE", "sub": "#CFCBC4", "card": "#222222", "card_fg": "#F5F3EE", "accent": YELLOW, "muted": MUTED},
    "light":  {"bg": LIGHT, "fg": CHARCOAL, "sub": "#4A4843", "card": WHITE, "card_fg": CHARCOAL, "accent": ORANGE, "muted": "#6B6862"},
    "yellow": {"bg": YELLOW, "fg": CHARCOAL, "sub": "#3A3A3A", "card": CHARCOAL, "card_fg": "#F5F3EE", "accent": CHARCOAL, "muted": "#3A3A3A"},
}

# ---------- Fonts ----------
_UR = {
    "vietnamese": "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB",
    "latin-ext": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
}
_FONT_FILES = [
    ("Be Vietnam Pro", w, f"be-vietnam-pro-{s}-{w}-normal.woff2", s) for w in (400, 600, 700) for s in _UR
] + [("Anton", 400, f"anton-{s}-400-normal.woff2", s) for s in _UR] + [
    ("Dancing Script", 700, f"dancing-script-{s}-700-normal.woff2", s) for s in ("vietnamese", "latin")
]


def _b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


_FONT_CSS = None


def font_css():
    global _FONT_CSS
    if _FONT_CSS is None:
        rules, missing = [], []
        for fam, wt, fn, sub in _FONT_FILES:
            p = os.path.join(FONTS_DIR, fn)
            if not os.path.exists(p):
                missing.append(fn)
                continue
            rules.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;"
                         f"src:url(data:font/woff2;base64,{_b64(p)}) format('woff2');unicode-range:{_UR[sub]};}}")
        if missing:
            print(f"! Thiếu font: {', '.join(missing)} — chữ có thể rơi về font hệ thống", file=sys.stderr)
        _FONT_CSS = "\n".join(rules)
    return _FONT_CSS


# ---------- Logo ----------
def find_logo():
    d = SCRIPT_DIR
    for _ in range(8):
        cand = os.path.join(d, "domains", "brand", "assets", "logo-mark.png")
        if os.path.exists(cand):
            return cand
        d = os.path.dirname(d)
    return None


_LOGO = None


def logo_uri():
    global _LOGO
    if _LOGO is None:
        p = find_logo()
        _LOGO = f"data:image/png;base64,{_b64(p)}" if p else ""
    return _LOGO


# ---------- Icons (SVG nét, không dùng emoji vì emoji hiển thị khác nhau giữa máy) ----------
ICONS = {
    "check": '<path d="M5 12l5 5 9-10"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "alert": '<path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17h.01"/>',
    "moon": '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.5 1.5M17.5 17.5L19 19M5 19l1.5-1.5M17.5 6.5L19 5"/>',
    "dumbbell": '<path d="M6 7v10M18 7v10M3 10v4M21 10v4M6 12h12"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "fire": '<path d="M12 21a7 7 0 0 0 7-7c0-4-3-6-4-9-1 3-3 4-4 4 0-2-1-4-1-6C7 6 5 10 5 14a7 7 0 0 0 7 7z"/>',
    "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V5a2 2 0 0 0-3-1zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19l8-8"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "arrow": '<path d="M4 12h16M14 6l6 6-6 6"/>',
    "star": '<path d="M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8L3.5 9.2l5.9-.9z"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.5 3.4-5.5 6.5-5.5s5.7 2 6.5 5.5M16 4.5a3.5 3.5 0 0 1 0 7M18 14.8c1.9.7 3.1 2.5 3.5 5.2"/>',
    "scale": '<path d="M12 4v16M5 20h14M5 8h14M5 8l-3 6a3 3 0 0 0 6 0zM19 8l-3 6a3 3 0 0 0 6 0z"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "pause": '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>',
    "stretch": '<path d="M3 12h18M7 8l-4 4 4 4M17 8l4 4-4 4"/>',
    "hand": '<path d="M7 11V6a1.5 1.5 0 0 1 3 0v5M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V12M16 9.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-.5A6.5 6.5 0 0 1 5 14.5V12a1.5 1.5 0 0 1 2-1.4"/>',
    "food": '<path d="M4 3v8a3 3 0 0 0 6 0V3M7 3v18M17 3c-2 2-3 5-3 8h3v10"/>',
    "bed": '<path d="M3 18V7M3 13h18v5M21 13a3 3 0 0 0-3-3h-7v3M7 11.5a1.5 1.5 0 1 0 0-.01"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
}


def icon(name, size, color, stroke=2):
    body = ICONS.get(name or "", ICONS["check"])
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'style="flex-shrink:0;display:block">{body}</svg>')


# ---------- Text markup ----------
def rich(text, hl_color=YELLOW, hl_mode="color"):
    """**đậm**, [[nhấn]] , \\n xuống dòng. Escape HTML trước."""
    t = html.escape(str(text or ""))
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    if hl_mode == "bg":
        t = re.sub(r"\[\[(.+?)\]\]", rf'<span style="background:{hl_color};color:{YELLOW if hl_color == CHARCOAL else CHARCOAL};padding:0 .18em;box-decoration-break:clone;-webkit-box-decoration-break:clone">\1</span>', t)
    else:
        t = re.sub(r"\[\[(.+?)\]\]", rf'<span style="color:{hl_color}">\1</span>', t)
    return t.replace("\n", "<br>")


def plain(text):
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", str(text or ""))
    return re.sub(r"\[\[(.+?)\]\]", r"\1", t)


def fit_size(text, base, steps=((40, 1.0), (70, 0.86), (100, 0.74), (9999, 0.64))):
    n = len(plain(text))
    for limit, k in steps:
        if n <= limit:
            return int(base * k)
    return int(base * steps[-1][1])


# ---------- Images ----------
class Ctx:
    def __init__(self, w, h, base_dir):
        self.w, self.h, self.base_dir = w, h, base_dir
        self.u = w / 1080.0

    def px(self, v):
        return int(round(v * self.u))

    def img(self, path):
        if not path:
            return None
        p = path if os.path.isabs(path) else os.path.join(self.base_dir, path)
        if not os.path.exists(p):
            raise FileNotFoundError(f"Không tìm thấy ảnh: {p}")
        ext = os.path.splitext(p)[1].lower().lstrip(".")
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
        return f"data:image/{mime};base64,{_b64(p)}"


# ---------- Chrome (header) ----------
def header(c, idx, total, fg, muted):
    logo = logo_uri()
    mark = f'<img src="{logo}" style="height:{c.px(40)}px;width:auto;display:block" alt="">' if logo else ""
    return (f'<div class="hdr" style="display:flex;justify-content:space-between;align-items:center;color:{fg}">'
            f'<div style="display:flex;align-items:center;gap:{c.px(14)}px">{mark}'
            f'<div style="font-family:Anton,sans-serif;font-size:{c.px(36)}px;letter-spacing:{c.px(6)}px;line-height:1">NAIGYM</div></div>'
            f'<div style="font-size:{c.px(26)}px;font-weight:600;letter-spacing:{c.px(2)}px;color:{muted}">{idx:02d} / {total:02d}</div></div>')


def frame(c, th, inner, extra_style=""):
    return (f'<div class="slide" style="width:{c.w}px;height:{c.h}px;background:{th["bg"]};color:{th["fg"]};'
            f'position:relative;overflow:hidden;box-sizing:border-box;padding:{c.px(72)}px {c.px(80)}px;'
            f'display:flex;flex-direction:column;gap:{c.px(30)}px;{extra_style}">{inner}</div>')


def h_big(c, text, size, color, hl=YELLOW, mode="color", align="left"):
    return (f'<h1 style="margin:0;font-family:Anton,sans-serif;font-weight:400;font-size:{size}px;line-height:1.28;'
            f'text-transform:uppercase;color:{color};text-align:{align}">{rich(text, hl, mode)}</h1>')


def p_sub(c, text, color, size=30, weight=400, align="left"):
    if not text:
        return ""
    return f'<p style="margin:0;font-size:{c.px(size)}px;line-height:1.5;font-weight:{weight};color:{color};text-align:{align}">{rich(text)}</p>'


def swipe(c, color):
    return f'<div style="display:flex;justify-content:flex-end;font-size:{c.px(24)}px;font-weight:600;color:{color}">Vuốt để xem →</div>'


def note_line(c, s, th):
    n = s.get("note")
    return f'<div style="font-size:{c.px(24)}px;line-height:1.5;color:{th["sub"]}">{rich(n, th["accent"])}</div>' if n else ""


# ---------- HOOK ----------
def render_hook(s, c, idx, total):
    layout = s.get("layout", "photo" if s.get("image") else "poster")
    kicker, head, sub = s.get("kicker", ""), s.get("headline", ""), s.get("subline", "")
    size = fit_size(head, c.px(84))
    if layout in ("photo", "split") and not s.get("image"):
        layout = "poster"

    def kick(color, bg=None):
        if not kicker:
            return ""
        if bg:
            return (f'<div style="align-self:flex-start;background:{bg};color:{CHARCOAL};font-weight:700;font-size:{c.px(24)}px;'
                    f'letter-spacing:{c.px(3)}px;padding:{c.px(10)}px {c.px(22)}px;border-radius:999px">{rich(kicker)}</div>')
        return f'<div style="font-size:{c.px(24)}px;font-weight:700;letter-spacing:{c.px(3)}px;color:{color}">{rich(kicker)}</div>'

    if layout == "photo":
        th = THEMES["dark"]
        img = c.img(s["image"])
        inner = (f'<img src="{img}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{s.get("image_position","center")}">'
                 f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,20,20,.35) 0%,rgba(20,20,20,.55) 40%,rgba(20,20,20,.94) 74%,#1C1C1C 100%)"></div>'
                 f'<div style="position:relative;height:100%;display:flex;flex-direction:column;gap:{c.px(26)}px">'
                 f'{header(c, idx, total, th["fg"], "#E0DDD6")}<div style="flex-grow:1"></div>'
                 f'{kick(None, YELLOW)}{h_big(c, head, size, th["fg"])}{p_sub(c, sub, "#D6D2CB")}{swipe(c, "#B5B1AA")}</div>')
        return frame(c, th, inner)

    if layout == "split":
        th = THEMES[s.get("theme", "light")]
        img = c.img(s["image"])
        pw = int(c.w * 0.43)
        inner = (f'<div style="display:flex;width:{c.w}px;height:{c.h}px">'
                 f'<div style="flex:1;box-sizing:border-box;padding:{c.px(72)}px {c.px(48)}px {c.px(72)}px {c.px(80)}px;display:flex;flex-direction:column;gap:{c.px(26)}px">'
                 f'{header(c, idx, total, th["fg"], th["muted"])}<div style="flex-grow:1"></div>{kick(None, YELLOW)}'
                 f'{h_big(c, head, int(size*0.86), th["fg"], YELLOW, "bg")}{p_sub(c, sub, th["sub"], 26)}<div style="flex-grow:1"></div>{swipe(c, th["muted"])}</div>'
                 f'<img src="{img}" alt="" style="width:{pw}px;height:{c.h}px;object-fit:cover;object-position:{s.get("image_position","center")};display:block"></div>')
        return frame(c, th, inner, "padding:0")

    if layout == "question":
        th = THEMES[s.get("theme", "yellow")]
        inner = (f'<div data-qa-ignore="1" style="position:absolute;right:{c.px(-40)}px;top:{c.px(60)}px;font-family:Anton,sans-serif;font-size:{c.px(760)}px;line-height:1;color:rgba(35,35,35,.10)">?</div>'
                 f'{header(c, idx, total, th["fg"], th["muted"])}<div style="flex-grow:1"></div>'
                 f'<div style="position:relative;display:flex;flex-direction:column;gap:{c.px(26)}px;max-width:{c.px(820)}px">{kick(th["fg"])}{h_big(c, head, size, th["fg"], CHARCOAL, "bg" if th["bg"] == YELLOW else "color")}{p_sub(c, sub, th["sub"], 28, 600)}</div>'
                 f'<div style="flex-grow:1"></div>{swipe(c, th["fg"])}')
        return frame(c, th, inner)

    if layout == "chat":
        th = THEMES["deep"]
        bg_img = c.img(s.get("image")) if s.get("image") else None
        bubbles = ""
        for m in s.get("messages", [])[:4]:
            mine = m.get("from") == "gym"
            if mine:
                bubbles += (f'<div style="align-self:flex-end;max-width:{c.px(660)}px;background:{YELLOW};color:{CHARCOAL};border-radius:{c.px(32)}px {c.px(32)}px {c.px(8)}px {c.px(32)}px;'
                            f'padding:{c.px(24)}px {c.px(34)}px;font-family:Anton,sans-serif;font-size:{c.px(54)}px;line-height:1.28;text-transform:uppercase">{rich(m.get("text"))}</div>')
            else:
                bubbles += (f'<div style="align-self:flex-start;max-width:{c.px(780)}px;background:{LIGHT};color:{CHARCOAL};border-radius:{c.px(32)}px {c.px(32)}px {c.px(32)}px {c.px(8)}px;'
                            f'padding:{c.px(26)}px {c.px(34)}px;font-size:{c.px(34)}px;line-height:1.45;font-weight:600">{rich(m.get("text"))}</div>')
        bgl = (f'<img src="{bg_img}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1)">'
               f'<div style="position:absolute;inset:0;background:rgba(14,14,14,.84)"></div>') if bg_img else ""
        inner = (f'{bgl}<div style="position:relative;height:100%;display:flex;flex-direction:column;gap:{c.px(24)}px">'
                 f'{header(c, idx, total, th["fg"], "#B5B1AA")}<div style="flex-grow:1"></div>{kick(MUTED)}{bubbles}<div style="flex-grow:1"></div>{swipe(c, "#B5B1AA")}</div>')
        return frame(c, th, inner)

    if layout == "versus":
        left, right = s.get("left", "A"), s.get("right", "B")
        half = c.w // 2
        lsz = fit_size(left, c.px(84), ((12, 1.0), (20, 0.86), (9999, 0.72)))
        rsz = fit_size(right, c.px(84), ((12, 1.0), (20, 0.86), (9999, 0.72)))
        inner = (f'<div style="display:flex;width:{c.w}px;height:{c.h}px">'
                 f'<div style="flex:0 0 {half}px;background:{LIGHT};color:{CHARCOAL};box-sizing:border-box;padding:{c.px(72)}px {c.px(110)}px {c.px(72)}px {c.px(80)}px;display:flex;flex-direction:column;justify-content:center">'
                 f'<div style="font-size:{c.px(24)}px;font-weight:700;color:#6B6862">A</div>{h_big(c, left, lsz, CHARCOAL)}</div>'
                 f'<div style="flex:0 0 {half}px;background:{CHARCOAL};box-sizing:border-box;padding:{c.px(72)}px {c.px(80)}px {c.px(72)}px {c.px(110)}px;display:flex;flex-direction:column;justify-content:center">'
                 f'<div style="font-size:{c.px(24)}px;font-weight:700;color:{MUTED}">B</div>{h_big(c, right, rsz, YELLOW)}</div></div>'
                 f'<div style="position:absolute;top:{c.px(72)}px;left:{c.px(80)}px;right:{c.px(80)}px">{header(c, idx, total, CHARCOAL, MUTED)}</div>'
                 f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:{c.px(150)}px;height:{c.px(150)}px;border-radius:50%;background:{ORANGE};color:{WHITE};display:flex;align-items:center;justify-content:center;font-family:Anton,sans-serif;font-size:{c.px(56)}px;border:{c.px(10)}px solid {WHITE};box-sizing:border-box">VS</div>'
                 + (f'<div style="position:absolute;left:50%;bottom:{c.px(72)}px;transform:translateX(-50%);background:{ORANGE};color:{CHARCOAL};border-radius:999px;padding:{c.px(14)}px {c.px(30)}px;font-size:{c.px(28)}px;font-weight:700;white-space:nowrap">{rich(head)}</div>' if head else ""))
        return frame(c, THEMES["dark"], inner, "padding:0")

    # poster (mặc định)
    th = THEMES[s.get("theme", "dark")]
    inner = (f'{header(c, idx, total, th["fg"], th["muted"])}<div style="flex-grow:1"></div>'
             f'<div style="display:flex;flex-direction:column;gap:{c.px(26)}px">{kick(th["accent"])}{h_big(c, head, size, th["fg"], YELLOW if th["bg"] != YELLOW else CHARCOAL)}{p_sub(c, sub, th["sub"])}</div>'
             f'<div style="flex-grow:1"></div>{swipe(c, th["muted"])}')
    return frame(c, th, inner)


# ---------- VALUE ----------
def h2(c, text, th, size=54):
    if not text:
        return ""
    return (f'<h2 style="margin:0;font-family:Anton,sans-serif;font-weight:400;font-size:{fit_size(text, c.px(size), ((30,1.0),(55,0.9),(9999,0.8)))}px;'
            f'line-height:1.3;text-transform:uppercase;color:{th["fg"]}">{rich(text, YELLOW if th["bg"] != YELLOW else CHARCOAL, "bg" if th["bg"] == LIGHT else "color")}</h2>')


def v_checklist(s, c, th):
    rows = ""
    for i, it in enumerate(s.get("items", [])[:5], 1):
        desc = f'<div style="font-size:{c.px(24)}px;line-height:1.45;color:{th["sub"]};margin-top:{c.px(6)}px">{rich(it.get("desc"))}</div>' if it.get("desc") else ""
        badge = (f'<div style="flex-shrink:0;width:{c.px(56)}px;height:{c.px(56)}px;border-radius:{c.px(14)}px;background:{YELLOW};color:{CHARCOAL};'
                 f'display:flex;align-items:center;justify-content:center;font-family:Anton,sans-serif;font-size:{c.px(30)}px">{i}</div>')
        rows += (f'<div style="display:flex;gap:{c.px(24)}px;align-items:flex-start;background:{th["card"]};color:{th["card_fg"]};border-radius:{c.px(20)}px;padding:{c.px(24)}px {c.px(28)}px">'
                 f'{badge}<div><div style="font-size:{c.px(29)}px;font-weight:700;line-height:1.35">{rich(it.get("title"))}</div>{desc}</div></div>')
    return f'{h2(c, s.get("heading"), th)}<div style="flex-grow:1;display:flex;flex-direction:column;justify-content:center;gap:{c.px(16)}px">{rows}</div>'


def v_comparison(s, c, th):
    stops = [YELLOW, "#F9B24C", ORANGE]
    cols = ""
    for i, col in enumerate(s.get("columns", [])[:3]):
        cols += (f'<div style="flex:1;display:flex;flex-direction:column;border-radius:{c.px(20)}px;overflow:hidden;background:{th["card"]};color:{th["card_fg"]}">'
                 f'<div style="background:{stops[i]};color:{CHARCOAL};text-align:center;font-family:Anton,sans-serif;font-size:{c.px(40)}px;padding:{c.px(20)}px 0;text-transform:uppercase">{rich(col.get("label"))}</div>'
                 f'<div style="flex:1;padding:{c.px(26)}px;font-size:{c.px(30)}px;font-weight:600;line-height:1.45;display:flex;align-items:center;justify-content:center;text-align:center">{rich(col.get("text"))}</div></div>')
    foot = s.get("note") or "Mức nào cũng là lựa chọn hợp lệ — tùy hoàn cảnh của bạn."
    return (f'{h2(c, s.get("heading"), th)}<div style="flex-grow:1;display:flex;gap:{c.px(18)}px">{cols}</div>'
            f'<div style="font-size:{c.px(23)}px;color:{th["sub"]};text-align:center">{rich(foot)}</div>')


def v_radial(s, c, th):
    branches = s.get("branches", [])[:6]
    n = max(len(branches), 1)
    area = c.w - 2 * c.px(80)
    top_pad = c.px(140)
    ah = c.h - top_pad - c.px(72)
    cx, cy = c.w / 2, top_pad + ah / 2
    r = min(area, ah) * 0.36
    node_w = c.px(250)
    center = c.px(250)
    nodes = ""
    for i, br in enumerate(branches):
        a = 2 * math.pi * i / n - math.pi / 2
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        nodes += (f'<div style="position:absolute;left:{x - node_w/2:.0f}px;top:{y - c.px(70):.0f}px;width:{node_w}px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:{c.px(6)}px">'
                  f'<div style="width:{c.px(64)}px;height:{c.px(64)}px;border-radius:50%;background:{th["card"]};display:flex;align-items:center;justify-content:center">{icon(br.get("icon"), c.px(34), YELLOW if th["card"] != WHITE else ORANGE)}</div>'
                  f'<div style="font-size:{c.px(25)}px;font-weight:700;line-height:1.25">{rich(br.get("label"))}</div>'
                  f'<div style="font-size:{c.px(21)}px;line-height:1.35;color:{th["sub"]}">{rich(br.get("desc"))}</div></div>')
    ring = f'<div data-qa-ignore="1" style="position:absolute;left:{cx-r:.0f}px;top:{cy-r:.0f}px;width:{2*r:.0f}px;height:{2*r:.0f}px;border-radius:50%;border:{c.px(3)}px dashed {th["muted"]};opacity:.5;box-sizing:border-box"></div>'
    ctr = (f'<div style="position:absolute;left:{cx-center/2:.0f}px;top:{cy-center/2:.0f}px;width:{center}px;height:{center}px;border-radius:50%;'
           f'background:linear-gradient(135deg,{YELLOW},{ORANGE});color:{CHARCOAL};display:flex;align-items:center;justify-content:center;text-align:center;'
           f'font-family:Anton,sans-serif;font-size:{c.px(32)}px;line-height:1.2;padding:{c.px(28)}px;box-sizing:border-box;text-transform:uppercase">{rich(s.get("center_label"))}</div>')
    return ring + ctr + nodes


def v_mythbust(s, c, th):
    return (f'<div style="background:{"#FFE6D5" if th["bg"] == LIGHT else th["card"]};color:{th["card_fg"] if th["bg"] != LIGHT else CHARCOAL};border-radius:{c.px(22)}px;padding:{c.px(30)}px {c.px(34)}px;display:flex;flex-direction:column;gap:{c.px(12)}px">'
            f'<div style="display:flex;align-items:center;gap:{c.px(12)}px;font-weight:700;font-size:{c.px(24)}px;letter-spacing:{c.px(3)}px;color:{ORANGE}">{icon("x", c.px(30), ORANGE, 3)}QUAN NIỆM SAI</div>'
            f'<div style="font-size:{c.px(32)}px;font-weight:700;line-height:1.4;text-decoration:line-through;text-decoration-color:{ORANGE};text-decoration-thickness:{c.px(3)}px">{rich(s.get("myth"))}</div></div>'
            f'<div style="flex-grow:1;border-left:{c.px(10)}px solid {YELLOW};padding:{c.px(8)}px 0 {c.px(8)}px {c.px(30)}px;display:flex;flex-direction:column;justify-content:center;gap:{c.px(18)}px">'
            f'<div style="display:flex;align-items:center;gap:{c.px(12)}px;font-weight:700;font-size:{c.px(24)}px;letter-spacing:{c.px(3)}px;color:{th["accent"]}">{icon("check", c.px(30), th["accent"], 3)}SỰ THẬT</div>'
            f'<div style="font-family:Anton,sans-serif;font-size:{fit_size(s.get("truth"), c.px(52), ((50,1.0),(90,0.86),(9999,0.74)))}px;line-height:1.3;text-transform:uppercase">{rich(s.get("truth"), YELLOW, "bg" if th["bg"] == LIGHT else "color")}</div>'
            f'<div style="font-size:{c.px(25)}px;line-height:1.55;color:{th["sub"]}">{rich(s.get("mechanism"))}</div></div>')


def v_timeline(s, c, th):
    steps = s.get("steps", [])[:4]
    n = max(len(steps), 1)
    colors = [ORANGE, MUTED, th["fg"], YELLOW]
    dots = "".join(f'<div style="position:relative;width:{c.px(52)}px;height:{c.px(52)}px;border-radius:50%;background:{colors[i % 4]}"></div>' for i in range(n))
    cols = ""
    for i, st in enumerate(steps):
        cols += (f'<div style="flex:1;display:flex;flex-direction:column;gap:{c.px(10)}px">'
                 f'<div style="font-family:Anton,sans-serif;font-size:{c.px(34)}px;color:{colors[i % 4] if colors[i % 4] != th["fg"] else th["fg"]};text-transform:uppercase">{rich(st.get("label"))}</div>'
                 f'<div style="font-size:{c.px(27)}px;font-weight:700;line-height:1.35">{rich(st.get("title"))}</div>'
                 f'<div style="font-size:{c.px(23)}px;line-height:1.5;color:{th["sub"]}">{rich(st.get("desc"))}</div></div>')
    return (f'{h2(c, s.get("heading"), th)}'
            f'<div style="position:relative;display:flex;justify-content:space-between;padding-top:{c.px(10)}px">'
            f'<div data-qa-ignore="1" style="position:absolute;left:{c.px(26)}px;right:{c.px(26)}px;top:{c.px(33)}px;height:{c.px(6)}px;background:{th["muted"]}"></div>{dots}</div>'
            f'<div style="display:flex;gap:{c.px(24)}px;flex-grow:1">{cols}</div>')


def v_stat(s, c, th):
    num = s.get("number", "")
    nsz = fit_size(num, c.px(240), ((5, 1.0), (8, 0.8), (9999, 0.62)))
    return (f'<div style="flex-grow:1;display:flex;flex-direction:column;justify-content:center;gap:{c.px(14)}px">'
            f'<div style="font-size:{c.px(26)}px;font-weight:700;letter-spacing:{c.px(3)}px;color:{th["accent"]}">{rich(s.get("kicker"))}</div>'
            f'<div style="font-family:Anton,sans-serif;font-size:{nsz}px;line-height:1.05;color:{YELLOW if th["bg"] != YELLOW else CHARCOAL}">{html.escape(num)}</div>'
            f'{h_big(c, s.get("label",""), c.px(56), th["fg"])}{p_sub(c, s.get("desc"), th["sub"], 27)}</div>')


def v_grid(s, c, th):
    items = s.get("items", [])[:6]
    cols = 3 if len(items) > 4 else 2
    cells = ""
    for it in items:
        cells += (f'<div style="background:{th["card"]};color:{th["card_fg"]};border-radius:{c.px(22)}px;padding:{c.px(28)}px;display:flex;flex-direction:column;gap:{c.px(12)}px">'
                  f'{icon(it.get("icon"), c.px(48), YELLOW if th["card"] != WHITE else ORANGE)}'
                  f'<div style="font-size:{c.px(28)}px;font-weight:700;line-height:1.3">{rich(it.get("title"))}</div>'
                  f'<div style="font-size:{c.px(22)}px;line-height:1.45;opacity:.82">{rich(it.get("desc"))}</div></div>')
    return (f'{h2(c, s.get("heading"), th)}<div style="flex-grow:1;display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));'
            f'grid-auto-rows:minmax(0,1fr);gap:{c.px(18)}px">{cells}</div>')


def v_flow(s, c, th):
    def box(d, color, label):
        return (f'<div style="flex:1;border:{c.px(3)}px solid {color};border-radius:{c.px(22)}px;padding:{c.px(26)}px;display:flex;flex-direction:column;gap:{c.px(10)}px">'
                f'<div style="font-family:Anton,sans-serif;font-size:{c.px(40)}px;color:{color}">{label}</div>'
                f'<div style="font-size:{c.px(27)}px;font-weight:700;line-height:1.35">{rich(d.get("title"))}</div>'
                f'<div style="font-size:{c.px(23)}px;line-height:1.5;color:{th["sub"]}">{rich(d.get("desc"))}</div></div>')
    q = (f'<div style="align-self:center;background:{LIGHT if th["bg"] != LIGHT else WHITE};color:{CHARCOAL};border-radius:{c.px(24)}px;'
         f'padding:{c.px(26)}px {c.px(36)}px;text-align:center;font-size:{c.px(30)}px;font-weight:700;line-height:1.4;max-width:{c.px(780)}px">{rich(s.get("question"))}</div>')
    lines = (f'<svg data-qa-ignore="1" width="{c.px(840)}" height="{c.px(60)}" viewBox="0 0 840 60" style="align-self:center" aria-hidden="true">'
             f'<path d="M420 0V18H210V58M420 18H630V58" fill="none" stroke="{th["muted"]}" stroke-width="4"/></svg>')
    return (f'{h2(c, s.get("heading"), th)}{q}{lines}<div style="display:flex;gap:{c.px(22)}px">'
            f'{box(s.get("yes", {}), YELLOW if th["bg"] != YELLOW else CHARCOAL, s.get("yes_label", "CÓ"))}{box(s.get("no", {}), th["muted"], s.get("no_label", "KHÔNG"))}</div><div style="flex-grow:1"></div>')


VALUE = {"checklist": v_checklist, "comparison": v_comparison, "radial": v_radial, "myth-bust": v_mythbust,
         "timeline": v_timeline, "stat": v_stat, "grid": v_grid, "flow": v_flow}


def render_value(s, c, idx, total):
    fmt = s.get("format", "checklist")
    if fmt not in VALUE:
        raise ValueError(f"format không hợp lệ: {fmt}. Dùng: {', '.join(VALUE)}")
    default_theme = {"comparison": "light", "timeline": "light", "myth-bust": "light", "radial": "light"}.get(fmt, "dark")
    th = THEMES[s.get("theme", default_theme)]
    body = VALUE[fmt](s, c, th)
    note = note_line(c, s, th) if fmt != "comparison" else ""
    return frame(c, th, f'{header(c, idx, total, th["fg"], th["muted"])}{body}{note}')


# ---------- CTA ----------
def render_cta(s, c, idx, total):
    layout = s.get("layout", "split" if s.get("image") else "solid")
    head, cta, tags = s.get("headline", ""), s.get("cta_text", ""), s.get("hashtags", "#naigymvietnam")
    ch = s.get("channel", "dm_zalo")
    ic = "link" if ch == "link_in_bio" else "chat"
    if layout in ("split", "band") and not s.get("image"):
        layout = "solid"
    hsz = fit_size(head, c.px(58), ((40, 1.0), (70, 0.9), (9999, 0.8)))

    def btn(bg, fg):
        return (f'<div style="align-self:flex-start;display:flex;align-items:center;gap:{c.px(14)}px;background:{bg};color:{fg};border-radius:{c.px(18)}px;'
                f'padding:{c.px(20)}px {c.px(28)}px;font-size:{c.px(26)}px;font-weight:700;line-height:1.35">{icon(ic, c.px(30), fg, 2.4)}<span>{rich(cta)}</span></div>')

    if layout == "split":
        th = THEMES["dark"]
        img = c.img(s["image"])
        lw = int(c.w * 0.56)
        inner = (f'<div style="display:flex;width:{c.w}px;height:{c.h}px">'
                 f'<div style="width:{lw}px;flex-shrink:0;box-sizing:border-box;padding:{c.px(72)}px {c.px(48)}px {c.px(72)}px {c.px(80)}px;display:flex;flex-direction:column;gap:{c.px(24)}px">'
                 f'{header(c, idx, total, th["fg"], th["muted"])}<div style="flex-grow:1"></div>'
                 f'<div data-qa-ignore="1" style="font-family:Anton,sans-serif;font-size:{c.px(140)}px;line-height:.7;height:{c.px(70)}px;color:{YELLOW}">“</div>'
                 f'{h_big(c, head, hsz, th["fg"])}{p_sub(c, s.get("subline"), th["sub"], 26)}<div style="flex-grow:1"></div>{btn(YELLOW, CHARCOAL)}'
                 f'<div style="font-size:{c.px(22)}px;font-weight:700;color:{MUTED}">{html.escape(tags)}</div></div>'
                 f'<img src="{img}" alt="" style="flex:1;min-width:0;height:{c.h}px;object-fit:cover;object-position:{s.get("image_position","center")};display:block"></div>')
        return frame(c, th, inner, "padding:0")

    if layout == "band":
        th = THEMES["dark"]
        img = c.img(s["image"])
        inner = (f'<div style="display:flex;flex-direction:column;width:{c.w}px;height:{c.h}px">'
                 f'<div style="box-sizing:border-box;padding:{c.px(72)}px {c.px(80)}px {c.px(40)}px;display:flex;flex-direction:column;gap:{c.px(26)}px">'
                 f'{header(c, idx, total, th["fg"], th["muted"])}{h_big(c, head, hsz, th["fg"])}{p_sub(c, s.get("subline"), th["sub"], 26)}'
                 f'<div style="display:flex;justify-content:space-between;align-items:center;gap:{c.px(20)}px">{btn(YELLOW, CHARCOAL)}<div style="font-size:{c.px(22)}px;font-weight:700;color:{MUTED}">{html.escape(tags)}</div></div></div>'
                 f'<img src="{img}" alt="" style="flex-grow:1;min-height:0;width:100%;object-fit:cover;object-position:{s.get("image_position","center")};display:block"></div>')
        return frame(c, th, inner, "padding:0")

    th = THEMES[s.get("theme", "yellow")]
    inner = (f'{header(c, idx, total, th["fg"], th["muted"])}<div style="flex-grow:1"></div>'
             f'{h_big(c, head, hsz, th["fg"], CHARCOAL if th["bg"] == YELLOW else YELLOW, "bg" if th["bg"] == YELLOW else "color")}'
             f'{p_sub(c, s.get("subline"), th["sub"], 27, 600)}<div style="flex-grow:1"></div>'
             f'{btn(CHARCOAL if th["bg"] == YELLOW else YELLOW, YELLOW if th["bg"] == YELLOW else CHARCOAL)}'
             f'<div style="font-size:{c.px(22)}px;font-weight:700;color:{th["muted"]}">{html.escape(tags)}</div>')
    return frame(c, th, inner)


def render_photo_brief(s, c, idx, total):
    th = THEMES["light"]
    inner = (f'{header(c, idx, total, th["fg"], th["muted"])}<div style="flex-grow:1;display:flex;align-items:center;justify-content:center">'
             f'<div style="background:{WHITE};border:{c.px(4)}px dashed {ORANGE};border-radius:{c.px(20)}px;padding:{c.px(56)}px;text-align:center;max-width:{c.px(820)}px">'
             f'<div style="font-weight:700;font-size:{c.px(32)}px;color:{ORANGE};margin-bottom:{c.px(16)}px">[PHOTO BRIEF — cần ảnh chụp thật]</div>'
             f'<div style="font-size:{c.px(28)}px;line-height:1.5">{rich(s.get("photo_brief"))}</div></div></div>')
    return frame(c, th, inner)


def slide_html(s, c, idx, total):
    if "photo_brief" in s:
        body = render_photo_brief(s, c, idx, total)
    else:
        t = s.get("type")
        fn = {"hook": render_hook, "value": render_value, "cta": render_cta}.get(t)
        if not fn:
            raise ValueError(f"type không hợp lệ: {t} (hook | value | cta)")
        body = fn(s, c, idx, total)
    return (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{font_css()}'
            f'*{{box-sizing:border-box}}html,body{{margin:0;width:{c.w}px;height:{c.h}px;overflow:hidden}}'
            f"body{{font-family:'Be Vietnam Pro',sans-serif;-webkit-font-smoothing:antialiased}}"
            f'</style></head><body>{body}</body></html>')


# ---------- Soát chữ (lint) ----------
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⭕⏰-⏺]")
ABBR_RE = re.compile(r"(?<![#\w])([A-ZĐ][A-ZĐ0-9+\-]{1,7})(?![\w])")
ALLOW = {"NAIGYM", "PT", "VS", "OK", "CTA", "A", "B", "CÓ", "KHÔNG"}
GLOSSARY = {
    "RPE": "tự chấm mức gắng sức 1–10", "RIR": "số rep còn dư", "DOMS": "đau nhức cơ sau tập (24–72 giờ)",
    "TEF": "năng lượng tiêu hao để tiêu hoá thức ăn", "GI": "carb hấp thu nhanh / chậm",
    "1RM": "mức tạ tối đa nâng được 1 lần", "HIIT": "cardio cường độ cao ngắt quãng",
    "EPA": "dạng omega-3 (giải thích kèm)", "DHA": "dạng omega-3 (giải thích kèm)", "BDNF": "một loại protein nuôi dưỡng não",
    "FITT-VP": "6 yếu tố: tần suất, cường độ, thời gian, loại bài, khối lượng, tiến triển",
    "PAR-Q": "bảng hỏi sức khoẻ trước khi tập", "FMS": "bài test chuyển động", "TUT": "thời gian cơ chịu lực",
    "HLV": "huấn luyện viên", "VD": "ví dụ", "ĐH": "đại học", "BMR": "năng lượng cơ thể tiêu hao khi nghỉ",
    "TDEE": "tổng năng lượng tiêu hao mỗi ngày", "NEAT": "năng lượng tiêu hao từ vận động thường ngày",
    "KG": "kg (viết thường) hoặc 'cân nặng'", "MG": "mg (viết thường)", "BCAA": "axit amin chuỗi nhánh (giải thích kèm)",
}


def iter_texts(slide):
    for k, v in slide.items():
        if k in ("image", "image_position", "type", "layout", "format", "theme", "channel", "hashtags", "icon", "from"):
            continue
        if isinstance(v, str):
            yield k, v
        elif isinstance(v, dict):
            yield from iter_texts(v)
        elif isinstance(v, list):
            for it in v:
                if isinstance(it, dict):
                    yield from iter_texts(it)
                elif isinstance(it, str):
                    yield k, it


def lint_carousel(car, label):
    issues = []
    slides = car.get("slides", [])
    if len(slides) != 3:
        issues.append(("warn", f"{label}: có {len(slides)} slide (chuẩn NaiGym là 3: Hook / Nội dung / CTA)"))
    for i, s in enumerate(slides, 1):
        for key, txt in iter_texts(s):
            p = plain(txt)
            if EMOJI_RE.search(p):
                issues.append(("error", f"{label} slide {i} [{key}]: có emoji → thay bằng icon SVG (\"icon\": \"tên\")"))
            for ab in set(ABBR_RE.findall(p)):
                if ab in ALLOW or ab.isdigit():
                    continue
                if p.isupper() and ab not in GLOSSARY and len(p) > len(ab) + 4:
                    continue  # cả câu viết hoa, không phải viết tắt
                tip = GLOSSARY.get(ab.rstrip("+"), "viết đầy đủ bằng tiếng Việt hoặc giải thích ngay bên cạnh")
                issues.append(("warn", f"{label} slide {i} [{key}]: viết tắt \"{ab}\" có thể khó hiểu → gợi ý: {tip}"))
        if s.get("type") == "hook":
            words = len(plain(s.get("headline", "")).split())
            if words > 14:
                issues.append(("warn", f"{label} slide {i}: headline hook {words} từ (nên ≤ 12–14 từ để đọc kịp trong 3 giây)"))
        for key, txt in iter_texts(s):
            for num in re.findall(r"\d+(?:[.,]\d+)?\s?(?:%|g\b|mg\b|kg\b|giờ|phút|lần)", plain(txt)):
                issues.append(("info", f"{label} slide {i}: số liệu \"{num}\" → đảm bảo có nguồn (tài liệu NaiGym / nghiên cứu)"))
    cap = car.get("caption", "")
    if cap:
        if EMOJI_RE.search(cap):
            issues.append(("info", f"{label}: caption có emoji (được phép ở caption, nhưng giữ tiết chế)"))
        for ab in set(ABBR_RE.findall(cap)) - ALLOW:
            if ab in GLOSSARY:
                issues.append(("warn", f"{label} caption: viết tắt \"{ab}\" → {GLOSSARY[ab]}"))
        tags = re.findall(r"#\w+", cap)
        if not 3 <= len(tags) <= 6:
            issues.append(("warn", f"{label} caption: {len(tags)} hashtag (nên 3–5, ưu tiên hashtag ngách)"))
    else:
        issues.append(("warn", f"{label}: chưa có caption"))
    return issues


# ---------- QA sau render (chạy trong trình duyệt) ----------
QA_JS = r"""
(minFont) => {
  const W = document.documentElement.clientWidth, H = document.documentElement.clientHeight;
  const out = [];
  const ignored = el => el.closest('[data-qa-ignore]');
  const boxes = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.textContent.trim();
    if (!t) continue;
    const el = n.parentElement;
    if (!el || ignored(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const rects = Array.from(r.getClientRects()).filter(b => b.width > 1 && b.height > 1);
    const fs = parseFloat(cs.fontSize);
    if (fs < minFont) out.push(['warn', `chữ nhỏ ${Math.round(fs)}px (< ${minFont}px) khó đọc trên điện thoại: "${t.slice(0, 40)}"`]);
    const lh = parseFloat(cs.lineHeight) || fs * 1.2;
    for (const b0 of rects) {
      const trim = Math.max(0, (b0.height - lh) / 2);
      const b = {left: b0.left, right: b0.right, top: b0.top + trim, bottom: b0.bottom - trim};
      if (b.left < -1 || b.top < -1 || b.right > W + 1 || b.bottom > H + 1)
        out.push(['error', `chữ tràn ra ngoài khung ảnh: "${t.slice(0, 40)}"`]);
      boxes.push({b, el, t});
    }
    let p = el;
    while (p && p !== document.body) {
      const ps = getComputedStyle(p);
      if (ps.overflow === 'hidden' && (p.scrollHeight > p.clientHeight + 2 || p.scrollWidth > p.clientWidth + 2) && !ignored(p) && p.querySelector('img') === null) {
        out.push(['error', `nội dung bị cắt (khối quá chật): "${t.slice(0, 40)}"`]); break;
      }
      p = p.parentElement;
    }
  }
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], c = boxes[j];
    if (a.el === c.el || a.el.contains(c.el) || c.el.contains(a.el)) continue;
    const ix = Math.min(a.b.right, c.b.right) - Math.max(a.b.left, c.b.left);
    const iy = Math.min(a.b.bottom, c.b.bottom) - Math.max(a.b.top, c.b.top);
    if (ix > 3 && iy > 3) out.push(['error', `chữ đè lên nhau: "${a.t.slice(0, 30)}" × "${c.t.slice(0, 30)}"`]);
  }
  const seen = new Set();
  return out.filter(x => { const k = x.join('|'); if (seen.has(k)) return false; seen.add(k); return true; });
}
"""


# ---------- Xuất file ----------
def next_reel_number(out_dir):
    best = 0
    if os.path.isdir(out_dir):
        for name in os.listdir(out_dir):
            m = re.fullmatch(r"reel-(\d+)", name)
            if m:
                best = max(best, int(m.group(1)))
    return best + 1


def _file_url(p):
    p = os.path.abspath(p).replace(os.sep, "/")
    return "file://" + (p if p.startswith("/") else "/" + p)


def contact_sheet(page, items, out_path, cols=6, thumb=300):
    cells = "".join(
        f'<div style="position:relative;width:{thumb}px;height:{thumb}px"><img src="{_file_url(p)}" style="width:100%;height:100%;object-fit:contain;background:#eee;display:block">'
        f'<div style="position:absolute;left:6px;bottom:6px;background:#232323;color:#FFD10C;font:700 14px sans-serif;padding:2px 6px;border-radius:4px">{html.escape(lbl)}</div></div>'
        for lbl, p in items)
    cols = max(1, min(cols, len(items)))
    rows = math.ceil(len(items) / cols)
    W, H = cols * thumb + (cols + 1) * 6, rows * thumb + (rows + 1) * 6
    page.set_viewport_size({"width": W, "height": H})
    tmp = out_path + ".tmp.html"  # mở bằng file:// để ảnh cục bộ load được
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(f'<html><body style="margin:0;background:#fff"><div style="display:grid;grid-template-columns:repeat({cols},{thumb}px);gap:6px;padding:6px">{cells}</div></body></html>')
    try:
        page.goto(_file_url(tmp))
        page.wait_for_load_state("networkidle")
        page.screenshot(path=out_path, full_page=True)
    finally:
        os.remove(tmp)


DEMO = {
    "platform": {"width": 1080, "height": 1080},
    "title": "Đau nhức sau tập có phải tập hiệu quả?",
    "caption": "Đau nhức sau tập có phải là dấu hiệu buổi tập hiệu quả?\n\nKhông hẳn. Đau nhức cơ 24–72 giờ sau tập chủ yếu cho thấy bài tập còn lạ với cơ thể, không phải thước đo kết quả.\n\nMuốn PT xem lại form tập của bạn? Nhắn tin cho NaiGym.\n\n#naigymvietnam #tapgymdungcach #phuchoicobap",
    "slides": [
        {"type": "hook", "layout": "poster", "kicker": "BẠN CÓ TỪNG NGHĨ", "headline": "Càng đau nhức sau tập, [[càng hiệu quả]]?", "subline": "Sự thật đứng sau cơn đau cơ 24–72 giờ."},
        {"type": "value", "format": "myth-bust", "myth": "Càng đau cơ sau buổi tập, buổi tập càng hiệu quả",
         "truth": "Đau nhức chỉ cho thấy bài tập còn [[lạ]] với cơ thể", "mechanism": "Vi tổn thương sợi cơ khi hạ tạ chậm gây viêm nhẹ — đó là bước thích nghi, không phải thước đo kết quả."},
        {"type": "cta", "layout": "solid", "headline": "Tập đúng mới là [[tập hiệu quả]].", "subline": "Không cần đau mới là tiến bộ.", "cta_text": "Nhắn NaiGym để PT xem form cho bạn", "channel": "dm_zalo"},
    ],
}


def load_config(args):
    if args.demo:
        return DEMO, os.getcwd()
    if not args.config:
        sys.exit("Cần --config <file.json> hoặc --demo")
    with open(args.config, encoding="utf-8") as f:
        return json.load(f), os.path.dirname(os.path.abspath(args.config))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--out-dir", default="output")
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--scale", type=float, default=1.0, help="1 = đúng kích thước nền tảng; 2 = ảnh nét gấp đôi")
    ap.add_argument("--start", type=int, help="Số reel bắt đầu (mặc định nối tiếp reel-NN lớn nhất trong out-dir)")
    ap.add_argument("--lint-only", action="store_true", help="Chỉ soát chữ, không render")
    ap.add_argument("--strict", action="store_true", help="Có lỗi (error) thì exit 1")
    ap.add_argument("--no-sheet", action="store_true", help="Không xuất ảnh tổng quan")
    ap.add_argument("--min-font", type=int, default=20, help="Cỡ chữ tối thiểu (px ở khổ 1080) trước khi cảnh báo")
    args = ap.parse_args()

    cfg, base_dir = load_config(args)
    platform = cfg.get("platform", {"width": 1080, "height": 1080})
    carousels = cfg.get("carousels") or [cfg]
    batch = "carousels" in cfg

    all_issues = []
    for k, car in enumerate(carousels, 1):
        all_issues += lint_carousel(car, car.get("title") or f"carousel {k}")
    if args.lint_only:
        report(all_issues)
        sys.exit(1 if args.strict and any(l == "error" for l, _ in all_issues) else 0)

    os.makedirs(args.out_dir, exist_ok=True)
    start = args.start or (next_reel_number(args.out_dir) if batch else None)

    from playwright.sync_api import sync_playwright
    sheet_items, index_lines = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for k, car in enumerate(carousels):
            pf = car.get("platform", platform)
            w = args.width or pf.get("width", 1080)
            h = args.height or pf.get("height", 1080)
            c = Ctx(w, h, base_dir)
            title = car.get("title") or f"carousel {k+1}"
            if batch:
                folder = os.path.join(args.out_dir, f"reel-{start + k}")
                os.makedirs(folder, exist_ok=True)
                tag = f"reel-{start + k}"
            else:
                folder, tag = args.out_dir, "slide"
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=args.scale)
            slides = car["slides"]
            for i, s in enumerate(slides, 1):
                page.set_content(slide_html(s, c, i, len(slides)), wait_until="load")
                page.evaluate("document.fonts.ready")
                for lvl, msg in page.evaluate(QA_JS, int(args.min_font * w / 1080)):
                    all_issues.append((lvl, f"{title} slide {i}: {msg}"))
                out = os.path.join(folder, f"slide-{i}.png")
                page.screenshot(path=out)
                sheet_items.append((f"{tag if batch else 'slide'}·{i}", os.path.abspath(out)))
                print(f"✓ {out} ({w}x{h})")
            page.close()
            if car.get("caption"):
                with open(os.path.join(folder, "caption.txt"), "w", encoding="utf-8") as f:
                    f.write(plain_title(title) + "\n\n" + car["caption"].strip() + "\n")
            index_lines.append(f"{tag}: {title}" if batch else title)
        if not args.no_sheet and sheet_items:
            sp = browser.new_page()
            contact_sheet(sp, sheet_items, os.path.join(args.out_dir, "_tong-quan.png"))
            print(f"✓ {os.path.join(args.out_dir, '_tong-quan.png')} (ảnh tổng quan để rà nhanh)")
        browser.close()

    if batch:
        with open(os.path.join(args.out_dir, "_danh-sach.txt"), "a", encoding="utf-8") as f:
            f.write("\n".join(index_lines) + "\n")
    report(all_issues)
    if args.strict and any(l == "error" for l, _ in all_issues):
        sys.exit(1)


def plain_title(t):
    return plain(t).strip()


def report(issues):
    if not issues:
        print("\nQA: không phát hiện vấn đề.")
        return
    order = {"error": 0, "warn": 1, "info": 2}
    label = {"error": "LỖI", "warn": "CẢNH BÁO", "info": "GHI CHÚ"}
    print("\n=== QA ===")
    for lvl, msg in sorted(issues, key=lambda x: order[x[0]]):
        print(f"[{label[lvl]}] {msg}")
    cnt = {l: sum(1 for x, _ in issues if x == l) for l in order}
    print(f"\nTổng: {cnt['error']} lỗi · {cnt['warn']} cảnh báo · {cnt['info']} ghi chú")


if __name__ == "__main__":
    main()
