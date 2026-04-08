from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

# Create print directory
if not os.path.exists('print'):
    os.makedirs('print')

# Constants for business card (3.5" x 2" at 300 DPI)
WIDTH = 1050
HEIGHT = 600
BLEED = 38 # 1/8" bleed
FULL_WIDTH = WIDTH + 2 * BLEED
FULL_HEIGHT = HEIGHT + 2 * BLEED

# Colors
BLACK = (21, 21, 21)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)

def draw_text(draw, text, position, font, fill, align="left"):
    draw.text(position, text, font=font, fill=fill)

try:
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
    except IOError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
except Exception as e:
    font_large = font_medium = font_small = ImageFont.load_default()

# --- FRONT OF CARD ---
front_img = Image.new('RGB', (FULL_WIDTH, FULL_HEIGHT), BLACK)
draw_front = ImageDraw.Draw(front_img)

# Layout adjustments to fit both logo and profile
try:
    logo = Image.open('logo.jpg')
    # Resize logo
    logo.thumbnail((FULL_WIDTH, FULL_HEIGHT), Image.Resampling.LANCZOS)
    logo_w, logo_h = logo.size

    # We want to shift the logo up slightly to make room
    logo_x = (FULL_WIDTH - logo_w) // 2
    logo_y = -80  # Shift up
    front_img.paste(logo, (logo_x, logo_y))
except Exception as e:
    print(f"Could not load logo: {e}")

# Draw profile picture
try:
    profile = Image.open('profile.jpg')
    profile_size = 220

    # Crop to square first
    w, h = profile.size
    min_dim = min(w, h)
    left = (w - min_dim)/2
    top = (h - min_dim)/2
    right = (w + min_dim)/2
    bottom = (h + min_dim)/2
    profile = profile.crop((left, top, right, bottom))

    profile = profile.resize((profile_size, profile_size), Image.Resampling.LANCZOS)

    # Create circular mask
    mask = Image.new('L', (profile_size, profile_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, profile_size, profile_size), fill=255)

    # Create a gold border background for profile
    border_size = profile_size + 16
    border_bg = Image.new('RGBA', (border_size, border_size), (0,0,0,0))
    draw_border = ImageDraw.Draw(border_bg)
    draw_border.ellipse((0, 0, border_size, border_size), fill=GOLD)
    draw_border.ellipse((8, 8, border_size-8, border_size-8), fill=BLACK)

    # Position
    profile_x = (FULL_WIDTH - profile_size) // 2
    profile_y = (FULL_HEIGHT // 2) - 60
    border_x = profile_x - 8
    border_y = profile_y - 8

    # Paste border then profile
    front_img.paste(border_bg, (border_x, border_y), mask=border_bg.split()[3])
    front_img.paste(profile, (profile_x, profile_y), mask=mask)
except Exception as e:
    print(f"Could not load profile picture: {e}")

# Bottom section for contact info
draw_front.rectangle([(0, FULL_HEIGHT - 220), (FULL_WIDTH, FULL_HEIGHT)], fill=(12, 12, 12))
draw_front.line([(0, FULL_HEIGHT - 220), (FULL_WIDTH, FULL_HEIGHT - 220)], fill=GOLD, width=4)

name_text = "MARY HENNEDY"
title_text = "REALTOR® | GOLDSTONE REALTY"
contact_text = "+1 (609) 500-8446  |  maryhennedy@goldstonerealty.com"

def get_text_width(text, font):
    if hasattr(font, 'getbbox'):
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0]
    return len(text) * 20

draw_front.text(((FULL_WIDTH - get_text_width(name_text, font_large)) // 2, FULL_HEIGHT - 190), name_text, font=font_large, fill=GOLD)
draw_front.text(((FULL_WIDTH - get_text_width(title_text, font_medium)) // 2, FULL_HEIGHT - 120), title_text, font=font_medium, fill=LIGHT_GRAY)
draw_front.text(((FULL_WIDTH - get_text_width(contact_text, font_small)) // 2, FULL_HEIGHT - 60), contact_text, font=font_small, fill=WHITE)

front_img.save('print/business_card_front.png')


# --- BACK OF CARD ---
back_img = Image.new('RGB', (FULL_WIDTH, FULL_HEIGHT), BLACK)
draw_back = ImageDraw.Draw(back_img)

# Try to load the gold QR code
try:
    qr = Image.open('qrcode_gold_on_black.png')
    qr_size = 420
    qr = qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    qr_x = (FULL_WIDTH - qr_size) // 2
    qr_y = (FULL_HEIGHT - qr_size) // 2 - 40
    back_img.paste(qr, (qr_x, qr_y))

    scan_text = "SCAN FOR DIGITAL CARD & CONTACT INFO"
    draw_back.text(((FULL_WIDTH - get_text_width(scan_text, font_medium)) // 2, qr_y + qr_size + 40), scan_text, font=font_medium, fill=GOLD)

except Exception as e:
    print(f"Could not load QR code: {e}")

back_img.save('print/business_card_back.png')

print("Updated print ready designs generated in print/ directory.")
