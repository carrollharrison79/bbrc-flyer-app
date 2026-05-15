"""
generate_flyers.py — Dynamic PDF flyers with Street View photos
===============================================================
Requirements:
    pip install reportlab pandas openpyxl pillow requests
 
Files needed in same folder as this script:
    Marketing_List_Classified.xlsx
    9EF9F25E-9E91-4854-8E5D-03032F7EAB23.jpeg
    Company_Logo_.png
    instagram_qr.png
    facebook_qr.png
    linkedin_qr.png
 
Run:
    python generate_flyers.py
"""
 
import os, re, textwrap, io, time, requests
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
 
# ── Config ──────────────────────────────────────────────────
INPUT_FILE  = "Marketing_List__Final_.xlsx"
OUTPUT_DIR  = "flyers"
HEADSHOT    = "9EF9F25E-9E91-4854-8E5D-03032F7EAB23.jpeg"
LOGO        = "Company_Logo_.png"
IG_QR       = "instagram_qr.png"
FB_QR       = "facebook_qr.png"
LI_QR       = "linkedin_qr.png"
GOOGLE_KEY  = "AIzaSyB5kyDTIJTbI-lhiIgDaYNZoyt5hn7bxmk"
SKIP_TYPES  = {"Institutional/Government"}
 
# ── Colors ──────────────────────────────────────────────────
ROYAL_BLUE  = HexColor("#1a4fa0")
LIGHT_BLUE  = HexColor("#e8eef8")
DARK_NAVY   = HexColor("#1a2133")
GRAY_TEXT   = HexColor("#7a8aaa")
BORDER_GRAY = HexColor("#ccd4e0")
MID_BLUE    = HexColor("#8ab0d8")
BODY_GRAY   = HexColor("#444444")
BOX_BG      = HexColor("#f4f6fb")
PHOTO_BG    = HexColor("#e8eef8")
 
# ── Photo priority — most visually interesting type first ───
PHOTO_PRIORITY = [
    "Industrial/Warehouse", "Commercial Retail", "Commercial Office",
    "Self-Storage", "Multifamily Residential", "Mixed Use",
    "Marina/Recreational", "Religious", "Mining/Extraction",
    "Agricultural", "Vacant Land", "Single-Family Residential",
    "HOA/Common Area", "Utility/Infrastructure", "Unknown"
]
 
# ── Tailored messages ────────────────────────────────────────
MESSAGES = {
    "Commercial Retail":       "We represent active tenants and buyers specifically seeking retail space in the Tuscaloosa market. Demand is strong and we would welcome the opportunity to discuss how we can help you maximize the value of your holdings — whether through leasing, sale, or repositioning.",
    "Vacant Land":             "We work with developers, investors, and institutional buyers actively seeking land in Tuscaloosa County. If you have considered monetizing your land position, we have qualified buyers ready to move and would be glad to provide a confidential market evaluation.",
    "Industrial/Warehouse":    "Industrial and warehouse demand in the Tuscaloosa market is at an all-time high. We represent tenants and buyers actively looking for facilities like yours. If you are open to a conversation about leasing or a sale, we would love to connect.",
    "Multifamily Residential": "Investor demand for multifamily assets in the Tuscaloosa market remains exceptionally strong. We represent buyers prepared to move quickly and would be happy to provide a confidential valuation of your portfolio.",
    "Commercial Office":       "We have tenants and buyers actively searching for office space in Tuscaloosa. If you have considered leasing vacant suites or exploring a sale, we would welcome a confidential conversation about your options.",
    "Self-Storage":            "Self-storage continues to be one of the most sought-after asset classes among investors. We work with buyers specifically targeting storage facilities in Tuscaloosa and would be glad to discuss what your property could be worth today.",
    "Mining/Extraction":       "We specialize in sourcing land acquisitions for mining and extraction operations across Tuscaloosa County. If you are looking to expand your land footprint or add adjacent acreage, we have access to off-market opportunities and would welcome a conversation.",
    "Agricultural":            "We work with buyers and investors interested in agricultural land throughout Tuscaloosa County. If you have considered a sale, lease, or conservation easement, we would be glad to provide a confidential evaluation.",
    "Religious":               "We understand the unique stewardship responsibilities that come with owning religious property. When the time is right to explore your real estate options, we are here to help guide that process with care and discretion.",
    "HOA/Common Area":         "We assist community associations and developers in evaluating and optimizing their real estate holdings. If your association has questions about common area value or future development potential, we would welcome a conversation.",
    "Marina/Recreational":     "Recreational and waterfront properties in Alabama continue to attract strong buyer interest. We work with investors and operators in this space and would be glad to provide a confidential market assessment.",
    "Mixed Use":               "Mixed-use properties are among the most in-demand asset types in today's market. We represent buyers and tenants seeking exactly these opportunities in Tuscaloosa and would welcome the chance to discuss your property's potential.",
    "Utility/Infrastructure":  "We work with buyers and investors interested in infrastructure and utility-related real estate assets. If you have considered your options, we would be glad to have a confidential conversation.",
    "Single-Family Residential":"We work with investors and buyers actively acquiring residential properties in the Tuscaloosa market. If you have considered selling or have questions about current market value, we would be glad to provide a confidential evaluation.",
    "Unknown":                 "We are active in the Tuscaloosa commercial real estate market and work with a broad range of buyers, tenants, and investors. If you have ever considered your options for this property, we would welcome a confidential conversation.",
}
 
# ── Market trends by property type ──────────────────────────
MARKET_TRENDS = {
    "Commercial Retail":       ["Tuscaloosa avg cap rate: 6.5–7.0%", "Retail vacancy near historic lows nationally", "Grocery-anchored & essential retail outperforming"],
    "Vacant Land":             ["Industrial & residential land demand elevated", "I-20/59 corridor: active developer interest", "Tuscaloosa County parcels moving faster than 2024"],
    "Industrial/Warehouse":    ["Alabama avg asking rent: $6.50–$8.50/SF NNN", "Vacancy 7–9% statewide; sub-50K SF tighter at ~5%", "Rent growth: +2–4% YOY for well-spec'd product"],
    "Multifamily Residential": ["Alabama secondary market cap rates: 5.75–6.25%", "Value-add assets seeing 5%+ rent growth in 2025", "UA market: consistently strong student demand"],
    "Commercial Office":       ["Sun Belt office stabilizing; flight-to-quality trend", "Tuscaloosa avg cap rate: ~6.65%", "Medical & professional office outperforming class B/C"],
    "Self-Storage":            ["Self-storage: top defensive income asset in 2026", "Net-lease self-storage commanding premium pricing", "Occupancy rates remain strong in secondary markets"],
    "Mining/Extraction":       ["Land values stable with strong industrial demand", "Tuscaloosa County: active acquisition market", "I-20/59 corridor driving industrial land premiums"],
    "Agricultural":            ["Alabama agricultural land values holding steady", "Conservation easement demand increasing statewide", "Rural Tuscaloosa County parcels attracting investors"],
    "Religious":               ["Tuscaloosa avg cap rate: ~6.65% for special use", "Adaptive reuse demand increasing for large facilities", "Well-located properties attracting community interest"],
    "HOA/Common Area":         ["Tuscaloosa residential development market active", "Common area valuations tied to community growth", "New residential projects driving land demand nearby"],
    "Marina/Recreational":     ["Alabama waterfront property demand remains strong", "Lake Tuscaloosa recreational assets highly sought", "Buyer pool expanding for recreational real estate"],
    "Mixed Use":               ["Mixed-use among most in-demand asset types in 2026", "Tuscaloosa avg cap rate: 6.5–7.0%", "Strong tenant demand for walkable mixed-use product"],
    "Single-Family Residential":["Tuscaloosa investor demand for SFR portfolios active", "Value-add SFR: strong rent growth in 2025–2026", "UA-area rentals maintain low vacancy year-round"],
    "Utility/Infrastructure":  ["Infrastructure assets attracting institutional buyers", "Tuscaloosa County development driving utility demand", "Long-term lease structures command premium pricing"],
    "Unknown":                 ["Tuscaloosa CRE avg cap rate: ~6.65%", "Transaction volume improving through 2026", "Active buyer demand across all asset classes"],
}
 
# ── Recent deals ─────────────────────────────────────────────
RECENT_DEALS = [
    ("73 Acres — I-20/59 Corridor",  "Under Contract"),
    ("5500 21st Street",             "Industrial Bldg · Under Contract"),
    ("Culver Road — 1.25 Acres",     "Active"),
]
 
 
# ── Helpers ──────────────────────────────────────────────────
def safe_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')[:60]
 
def to_ir(pil_img, fmt='JPEG'):
    buf = io.BytesIO()
    pil_img.save(buf, format=fmt)
    buf.seek(0)
    return ImageReader(buf)
 
def pick_photo_address(properties):
    """Return the property address most worth photographing."""
    for ptype in PHOTO_PRIORITY:
        for row in properties:
            if row.get('Property Type') == ptype:
                addr = row.get('Property Address', '').strip()
                if addr and not re.match(r'^(hwy|highway|rd|road|county rd)', addr, re.I):
                    return addr
    # Fallback: first address with a number
    for row in properties:
        addr = row.get('Property Address', '').strip()
        if addr and re.search(r'\d', addr):
            return addr
    return None
 
def fetch_street_view(address, zip_code=''):
    """Fetch Street View image. Returns ImageReader or None."""
    full_addr = f"{address} {zip_code} Tuscaloosa AL".strip()
    encoded   = requests.utils.quote(full_addr)
 
    try:
        # Check metadata first
        meta = requests.get(
            f"https://maps.googleapis.com/maps/api/streetview/metadata"
            f"?location={encoded}&key={GOOGLE_KEY}", timeout=8
        ).json()
        if meta.get('status') != 'OK':
            return None
 
        # Try source=outdoor first for better building shots
        # then fall back to default
        for extra in ["&source=outdoor&fov=80&pitch=5", "&fov=90&pitch=0"]:
            url = (
                f"https://maps.googleapis.com/maps/api/streetview"
                f"?size=750x300&location={encoded}{extra}&key={GOOGLE_KEY}"
            )
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200 and resp.headers.get('content-type','').startswith('image'):
                img = PILImage.open(io.BytesIO(resp.content)).convert('RGB')
                # Skip if image is mostly gray (no imagery available)
                arr = list(img.getdata())
                avg_r = sum(p[0] for p in arr[:500]) / 500
                avg_g = sum(p[1] for p in arr[:500]) / 500
                avg_b = sum(p[2] for p in arr[:500]) / 500
                if abs(avg_r - avg_g) < 8 and abs(avg_g - avg_b) < 8 and avg_r > 180:
                    continue  # mostly gray = no real imagery
                return to_ir(img)
    except Exception as e:
        print(f"    Street View error for '{address}': {e}")
    return None
 
def prep_images():
    hs = lr = ig = fb = li = None
    if os.path.exists(HEADSHOT):
        img = PILImage.open(HEADSHOT)
        w, h = img.size; side = min(w, h)
        img = img.crop(((w-side)//2, 0, (w-side)//2+side, side)).resize((220, 220), PILImage.LANCZOS)
        hs = to_ir(img)
    if os.path.exists(LOGO):
        img = PILImage.open(LOGO).convert('RGBA')
        buf = io.BytesIO(); img.save(buf, format='PNG'); buf.seek(0)
        lr = ImageReader(buf)
    if os.path.exists(IG_QR):
        ig = to_ir(PILImage.open(IG_QR).convert('RGB'))
    if os.path.exists(FB_QR):
        fb = to_ir(PILImage.open(FB_QR).convert('RGB'))
    if os.path.exists(LI_QR):
        li = to_ir(PILImage.open(LI_QR).convert('RGB'))
    return hs, lr, ig, fb, li
 
 
# ── Draw flyer ───────────────────────────────────────────────
def draw_flyer(c, owner_name, owner_addr, properties, dominant_type, hs, lr, ig, fb, li, photo=None):
    W, H = landscape(letter)
    LEFT_W = 2.6 * inch
    M = 0.28 * inch
    S = 1.35  # sidebar scale
 
    # ── Sidebar ───────────────────────────────────────────
    c.setFillColor(ROYAL_BLUE)
    c.rect(0, 0, LEFT_W, H, fill=1, stroke=0)
    c.setFillColor(white)
    c.rect(0, H - 0.07*inch, LEFT_W, 0.07*inch, fill=1, stroke=0)
 
    # Headshot
    hs_sz = 1.2 * S * inch
    hs_x  = (LEFT_W - hs_sz) / 2
    hs_y  = H - 0.18*inch - hs_sz
    cx, cy = hs_x + hs_sz/2, hs_y + hs_sz/2
    c.saveState()
    p = c.beginPath(); p.circle(cx, cy, hs_sz/2)
    c.clipPath(p, stroke=0, fill=0)
    if hs: c.drawImage(hs, hs_x, hs_y, width=hs_sz, height=hs_sz, preserveAspectRatio=False)
    c.restoreState()
    c.saveState(); c.setStrokeColor(white); c.setLineWidth(3)
    c.circle(cx, cy, hs_sz/2, fill=0, stroke=1); c.restoreState()
 
    # Name / title
    name_y = hs_y - 0.22*S*inch
    c.setFillColor(white); c.setFont("Helvetica-Bold", round(12*S, 1))
    c.drawCentredString(LEFT_W/2, name_y, "Harrison Carroll")
    c.setFont("Helvetica", round(7.5*S, 1)); c.setFillColor(MID_BLUE)
    c.drawCentredString(LEFT_W/2, name_y - 0.17*S*inch, "COMMERCIAL SALESMAN")
 
    # Contact
    c.setFillColor(white); c.setFont("Helvetica", round(8.5*S, 1))
    ct_y = name_y - 0.38*S*inch
    c.drawCentredString(LEFT_W/2, ct_y,                "205-534-2628")
    c.drawCentredString(LEFT_W/2, ct_y - 0.17*S*inch, "harrison@billyboydrealty.com")
    c.setFont("Helvetica", round(7.5*S, 1))
    c.drawCentredString(LEFT_W/2, ct_y - 0.34*S*inch, "Billy Boyd Realty & Construction Inc.")
    c.setFont("Helvetica", round(7*S, 1))
    c.drawCentredString(LEFT_W/2, ct_y - 0.49*S*inch, "www.billyboydrealty.com")
    web_bot = ct_y - 0.49*S*inch
 
    # Logo at bottom
    logo_w = 1.55 * S * inch
    logo_h = logo_w * (106/477)
    logo_x = (LEFT_W - logo_w) / 2
    logo_y = 0.14 * inch
    pad_l  = 6
    if lr:
        c.setFillColor(white)
        c.roundRect(logo_x - pad_l, logo_y - pad_l,
                    logo_w + pad_l*2, logo_h + pad_l*2, 4, fill=1, stroke=0)
        c.drawImage(lr, logo_x, logo_y, width=logo_w, height=logo_h, mask='auto')
    logo_top = logo_y + logo_h + pad_l
 
    # QR codes — centered between website and logo
    qr_space = web_bot - logo_top
    qr_sz    = min(0.62 * S * inch, (qr_space - 0.3*inch) / 3)
    pad      = 3
    lbl_h    = 0.13 * inch
    row_h    = qr_sz + pad*2 + lbl_h + 0.05*inch
    qr_block_top = logo_top + (qr_space - row_h*3) / 2 + row_h*3
    qr_x    = (LEFT_W - qr_sz - pad*2) / 2
    qr_top  = qr_block_top
    for qr_img, label in [(ig, "Instagram"), (fb, "Facebook"), (li, "LinkedIn")]:
        qr_y = qr_top - qr_sz
        c.setFillColor(white)
        c.roundRect(qr_x - pad, qr_y - lbl_h - 1,
                    qr_sz + pad*2, qr_sz + pad*2 + lbl_h, 3, fill=1, stroke=0)
        if qr_img: c.drawImage(qr_img, qr_x, qr_y, width=qr_sz, height=qr_sz)
        c.setFillColor(ROYAL_BLUE); c.setFont("Helvetica-Bold", round(6.5*S, 1))
        c.drawCentredString(qr_x + qr_sz/2, qr_y - lbl_h + 2, label)
        qr_top -= row_h
 
    # ── Right side ────────────────────────────────────────
    RX = LEFT_W; RW = W - LEFT_W; MW2 = RW - 2*M
    HH = 1.2 * inch
 
    # Header band — draw from very top of page
    c.setFillColor(ROYAL_BLUE)
    c.rect(RX, H - HH, RW + 2, HH + 2, fill=1, stroke=0)  # bleed to all edges
    # White accent bar at very top
    c.setFillColor(white)
    c.rect(RX, H - 0.07*inch, RW + 2, 0.08*inch, fill=1, stroke=0)
    c.setFillColor(MID_BLUE); c.setFont("Helvetica-Bold", 8)
    c.drawString(RX+M, H - 0.28*inch, "PROPERTY OWNER")
    c.setFillColor(white); c.setFont("Helvetica-Bold", 17)
    dn = owner_name if len(owner_name) <= 44 else owner_name[:42] + "..."
    # Draw with slight character spacing
    x_pos = RX + M
    for ch in dn:
        c.drawString(x_pos, H - 0.58*inch, ch)
        x_pos += c.stringWidth(ch, "Helvetica-Bold", 17) + 0.6
    c.setFillColor(MID_BLUE); c.setFont("Helvetica", 10)
    c.drawString(RX+M, H - 0.82*inch, owner_addr[:72])
 
    # ── Dynamic layout — anchor from bottom up ────────────
    BOTTOM_M      = 0.16 * inch
    MSG_LINE_H    = 0.155 * inch
    MSG_LINES     = 4
    MSG_TOTAL_H   = 0.20*inch + MSG_LINES * MSG_LINE_H   # label + lines
 
    DEAL_ROW_H    = 0.25 * inch
    STAT_ROW_H    = 0.195 * inch
    N_STATS       = 3
    N_DEALS       = len(RECENT_DEALS)
    left_col_h    = 0.20*inch + N_STATS * STAT_ROW_H
    right_col_h   = 0.20*inch + N_DEALS * DEAL_ROW_H
    MID_CONTENT_H = max(left_col_h, right_col_h)
    BOX_PAD       = 0.10 * inch
    BOX_H         = MID_CONTENT_H + BOX_PAD * 2
 
    # Bottom up: msg → gap → boxes → gap → photo → gap → holdings
    msg_bot   = BOTTOM_M
    msg_top   = msg_bot + MSG_TOTAL_H
    box_bot   = msg_top + 0.10*inch
    box_top   = box_bot + BOX_H
    photo_bot = box_top + 0.12*inch
 
    # Holdings: dynamic height based on number of properties
    n_props   = min(len(properties), 10)
    n_rows    = max(1, -(-n_props // 2))          # ceil(n/2) rows in 2-col layout
    HOLD_LBL  = 0.20 * inch
    PROP_ROW  = 0.36 * inch
    hold_top  = H - HH - 0.18*inch               # just below header
    hold_bot  = hold_top - HOLD_LBL - n_rows * PROP_ROW
    if n_props > 10:
        hold_bot -= 0.20*inch                     # extra line for "...and N more"
 
    # Photo fills remaining space between holdings and snapshot boxes
    photo_top = hold_bot - 0.10*inch
    photo_h   = photo_top - photo_bot
    photo_w   = MW2
 
    # ── Holdings — two columns ────────────────────────────
    y = hold_top
    c.setFillColor(ROYAL_BLUE); c.setFont("Helvetica-Bold", 8)
    c.drawString(RX+M, y, "YOUR HOLDINGS — TUSCALOOSA COUNTY")
    y -= HOLD_LBL
 
    col_w  = (MW2 - 0.2*inch) / 2
    col1_x = RX + M
    col2_x = RX + M + col_w + 0.2*inch
    props_list = properties[:10]
    col1_props = props_list[0::2]
    col2_props = props_list[1::2]
    row_y = y
    for i in range(max(len(col1_props), len(col2_props))):
        for col_x, col_props in [(col1_x, col1_props), (col2_x, col2_props)]:
            if i >= len(col_props): continue
            row = col_props[i]
            bw = 1.3*inch; bh = 0.155*inch
            c.setFillColor(LIGHT_BLUE)
            c.roundRect(col_x, row_y - 0.02*inch, bw, bh, 2, fill=1, stroke=0)
            c.setFillColor(ROYAL_BLUE); c.setFont("Helvetica-Bold", 7.5)
            c.drawString(col_x + 4, row_y + 0.005*inch, row["Property Type"][:22])
            ax = col_x + bw + 0.07*inch
            max_w = col_w - bw - 0.07*inch  # available width after badge
            # Address — fit to available width at font size 10
            c.setFillColor(DARK_NAVY); c.setFont("Helvetica-Bold", 10)
            addr = row["Property Address"]
            # Estimate ~6.5 pts per char at size 10
            max_chars_addr = int(max_w / (10 * 0.55))
            addr_display = addr if len(addr) <= max_chars_addr else addr[:max_chars_addr-2]+"..."
            c.drawString(ax, row_y + 0.01*inch, addr_display)
            # Business use — smaller font, more chars
            c.setFillColor(GRAY_TEXT); c.setFont("Helvetica", 8)
            use = row["Business Use"]
            max_chars_use = int(max_w / (8 * 0.55))
            use_display = use if len(use) <= max_chars_use else use[:max_chars_use-2]+"..."
            c.drawString(ax, row_y - 0.125*inch, use_display)
        row_y -= PROP_ROW
    if len(properties) > 10:
        c.setFillColor(GRAY_TEXT); c.setFont("Helvetica-Oblique", 8)
        c.drawString(RX+M, row_y, f"...and {len(properties)-10} additional parcel(s)")
 
    # ── Property photo ────────────────────────────────────
    if photo_h > 0.3*inch:   # only draw if there's meaningful space
        if photo:
            c.drawImage(photo, RX+M, photo_bot, width=photo_w, height=photo_h,
                        preserveAspectRatio=True, anchor='c')
        else:
            c.setFillColor(PHOTO_BG)
            c.roundRect(RX+M, photo_bot, photo_w, photo_h, 5, fill=1, stroke=0)
            c.setStrokeColor(BORDER_GRAY); c.setLineWidth(0.8)
            c.roundRect(RX+M, photo_bot, photo_w, photo_h, 5, fill=0, stroke=1)
            c.setFillColor(MID_BLUE); c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(RX+M + photo_w/2, photo_bot + photo_h/2 + 0.10*inch,
                                "PROPERTY PHOTO")
            c.setFont("Helvetica", 9)
            c.drawCentredString(RX+M + photo_w/2, photo_bot + photo_h/2 - 0.08*inch,
                                "Street View image goes here")
 
    # ── Market snapshot + Recent activity ─────────────────
    col_w2 = MW2 / 2 - 0.1*inch
    trends = MARKET_TRENDS.get(dominant_type, MARKET_TRENDS["Unknown"])
    y = box_top - BOX_PAD
 
    # Shaded boxes — sized to contain all content
    c.setFillColor(BOX_BG)
    c.roundRect(RX+M - 4, box_bot, col_w2 + 8, BOX_H, 4, fill=1, stroke=0)
    c.roundRect(RX+M + col_w2 + 0.2*inch - 4, box_bot, col_w2 + 8, BOX_H, 4, fill=1, stroke=0)
 
    # Left: Market Snapshot
    c.setFillColor(ROYAL_BLUE); c.setFont("Helvetica-Bold", 8)
    c.drawString(RX+M, y, "MARKET SNAPSHOT — Q2 2026")
    ty = y - 0.20*inch
    for stat in trends[:N_STATS]:
        c.setFillColor(ROYAL_BLUE); c.setFont("Helvetica-Bold", 9)
        c.drawString(RX+M, ty, "·")
        c.setFillColor(DARK_NAVY); c.setFont("Helvetica", 9)
        c.drawString(RX+M + 0.12*inch, ty, stat)
        ty -= STAT_ROW_H
 
    # Right: Recent Activity
    rx2 = RX + M + col_w2 + 0.2*inch
    c.setFillColor(ROYAL_BLUE); c.setFont("Helvetica-Bold", 8)
    c.drawString(rx2, y, "RECENT BBRC ACTIVITY")
    dy = y - 0.20*inch
    for deal_addr, deal_status in RECENT_DEALS:
        c.setFillColor(DARK_NAVY); c.setFont("Helvetica-Bold", 9)
        c.drawString(rx2, dy, deal_addr)
        c.setFillColor(GRAY_TEXT); c.setFont("Helvetica", 8)
        c.drawString(rx2, dy - 0.12*inch, deal_status)
        dy -= DEAL_ROW_H
 
    # ── A Note From Harrison ──────────────────────────────
    c.setStrokeColor(ROYAL_BLUE); c.setLineWidth(1.5)
    c.line(RX+M, msg_top + 0.04*inch, RX+M + MW2, msg_top + 0.04*inch)
    c.setFillColor(ROYAL_BLUE); c.setFont("Helvetica-Bold", 8)
    c.drawString(RX+M, msg_top - 0.13*inch, "A NOTE FROM HARRISON")
    ly = msg_top - 0.30*inch
    msg = MESSAGES.get(dominant_type, MESSAGES["Unknown"])
    c.setFillColor(BODY_GRAY); c.setFont("Helvetica-Oblique", 9)
    chars = int(MW2 / (9 * 0.52))
    for line in textwrap.wrap(msg, width=chars)[:MSG_LINES]:
        c.drawString(RX+M, ly, line); ly -= MSG_LINE_H
 
    # Outer border
    c.setStrokeColor(BORDER_GRAY); c.setLineWidth(0.5)
    c.rect(0, 0, W, H, fill=0, stroke=1)
 
 
# ── Main ─────────────────────────────────────────────────────
def draw_mailing_panel(c, owner_name, owner_addr_line1, owner_addr_line2):
    """Draw mailing panel as second page — landscape letter."""
    W, H = landscape(letter)
    M = 0.5 * inch
 
    # Clean white background
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
 
    # Light fold guide line in the middle
    c.setStrokeColor(HexColor("#dddddd")); c.setLineWidth(0.5)
    c.setDash(4, 4)
    c.line(0, H/2, W, H/2)
    c.setDash()
 
    # ── Return address (top left) ─────────────────────────
    c.setFillColor(DARK_NAVY); c.setFont("Helvetica-Bold", 9)
    c.drawString(M, H - 0.55*inch, "Harrison Carroll")
    c.setFont("Helvetica", 9)
    c.drawString(M, H - 0.72*inch, "Billy Boyd Realty & Construction Inc.")
    c.drawString(M, H - 0.89*inch, "3811 Palisades Drive")
    c.drawString(M, H - 1.06*inch, "Tuscaloosa, AL 35405")
 
    # ── Stamp box (top right) ─────────────────────────────
    stamp_w = 1.1 * inch
    stamp_h = 0.85 * inch
    stamp_x = W - M - stamp_w
    stamp_y = H - M - stamp_h
    c.setStrokeColor(DARK_NAVY); c.setLineWidth(1)
    c.rect(stamp_x, stamp_y, stamp_w, stamp_h, fill=0, stroke=1)
    c.setFillColor(GRAY_TEXT); c.setFont("Helvetica", 7)
    c.drawCentredString(stamp_x + stamp_w/2, stamp_y + stamp_h/2 + 0.06*inch, "PLACE")
    c.drawCentredString(stamp_x + stamp_w/2, stamp_y + stamp_h/2 - 0.08*inch, "STAMP")
    c.drawCentredString(stamp_x + stamp_w/2, stamp_y + stamp_h/2 - 0.22*inch, "HERE")
 
    # ── Recipient address (center of lower half) ──────────
    addr_cx = W / 2
    addr_cy = H / 4  # center of bottom half
 
    c.setFillColor(DARK_NAVY); c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(addr_cx, addr_cy + 0.35*inch, owner_name.upper())
    c.setFont("Helvetica", 11)
    c.drawCentredString(addr_cx, addr_cy + 0.10*inch, owner_addr_line1.upper())
    if owner_addr_line2:
        c.drawCentredString(addr_cx, addr_cy - 0.15*inch, owner_addr_line2.upper())
 
    # Optional: FIRST CLASS MAIL text
    c.setFillColor(GRAY_TEXT); c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(addr_cx, addr_cy + 0.65*inch, "FIRST CLASS MAIL")
 
 
def main():
    # Load and flatten the interleaved owner/parcel row structure
    raw = pd.read_excel(INPUT_FILE, sheet_name='Parcel Details', dtype=str).fillna('')
    raw['Owner Name / Entity'] = raw['Owner Name / Entity'].replace('', None).ffill()
    raw['Owner Address']       = raw['Owner Address'].replace('', None).ffill()
    raw['Owner Zip']           = raw['Owner Zip'].replace('', None).ffill()
    df = raw[raw['Parcel ID'] != ''].copy()
 
    # Normalize column names to match rest of script
    df = df.rename(columns={
        'Owner Name / Entity': 'Owner Name 1',
        'Type':                'Property Type',
        'Use':                 'Business Use',
    })
 
    df = df[~df['Property Type'].isin(SKIP_TYPES)]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    hs, lr, ig, fb, li = prep_images()
 
    groups = list(df.groupby('Owner Name 1'))
    total  = len(groups)
    print(f"Generating {total} flyers...\n", flush=True)
 
    for i, (owner_name, group) in enumerate(groups):
        if not owner_name.strip(): continue
 
        oa    = f"{group.iloc[0]['Owner Address']}  ·  {group.iloc[0]['Owner Zip']}".strip(" ·").strip()
        props = group.to_dict('records')
        dom   = group['Property Type'].value_counts().index[0] if len(group) else "Unknown"
 
        # Pick best address to photograph
        photo_addr = pick_photo_address(props)
        photo_zip  = ""
        if photo_addr:
            # Find the zip for this address
            match = group[group['Property Address'] == photo_addr]
            if len(match): photo_zip = match.iloc[0].get('Property Zip', '')
 
        # Fetch Street View (with small delay to be polite to API)
        photo = None
        if photo_addr:
            photo = fetch_street_view(photo_addr, photo_zip)
            if photo:
                print(f"  [{i+1}/{total}] {owner_name[:40]} — photo OK", flush=True)
            else:
                print(f"  [{i+1}/{total}] {owner_name[:40]} — no photo", flush=True)
        else:
            print(f"  [{i+1}/{total}] {owner_name[:40]} — no address for photo", flush=True)
 
        fname = f"{OUTPUT_DIR}/{safe_filename(owner_name)}.pdf"
        cv = canvas.Canvas(fname, pagesize=landscape(letter))
        draw_flyer(cv, owner_name, oa, props, dom, hs, lr, ig, fb, li, photo=photo)
 
        # Page 2: mailing panel
        cv.showPage()
        owner_mailing1 = group.iloc[0]["Owner Address"].strip()
        owner_zip      = group.iloc[0]["Owner Zip"].strip()
        owner_city     = f"Tuscaloosa, AL {owner_zip}"
        draw_mailing_panel(cv, owner_name, owner_mailing1, owner_city)
        cv.save()
 
        # Polite pause — Street View allows ~10 req/sec
        time.sleep(0.15)
 
    print(f"\nDone! {total} PDFs saved to ./{OUTPUT_DIR}/")
 
 
if __name__ == "__main__":
    main()