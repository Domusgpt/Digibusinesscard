from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os
import qrcode

if not os.path.exists('print'):
    os.makedirs('print')

WIDTH = 1050
HEIGHT = 600
BLEED = 38
FULL_WIDTH = WIDTH + 2 * BLEED
FULL_HEIGHT = HEIGHT + 2 * BLEED

BLACK = (21, 21, 21)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)

try:
    font_xl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except Exception as e:
    font_xl = font_large = font_medium = font_small = ImageFont.load_default()

def get_text_width(text, font):
    if hasattr(font, 'getbbox'):
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0]
    return len(text) * 20

# --- SPLIT FRONT OF CARD ---
front_img = Image.new('RGB', (FULL_WIDTH, FULL_HEIGHT), BLACK)
draw_front = ImageDraw.Draw(front_img)

half_width = FULL_WIDTH // 2

# BACKGROUND TEXTURE/GRADIENT (Simulated via overlay)
bg_overlay = Image.new('RGB', (FULL_WIDTH, FULL_HEIGHT), (15, 15, 15))
front_img.paste(bg_overlay, (0, 0))

# RIGHT HALF: Logo Center (Do this first so it sits behind the middle border)
try:
    logo = Image.open('logo.jpg').convert('RGBA')
    logo_target_w = half_width - 120
    logo.thumbnail((logo_target_w, FULL_HEIGHT - 120), Image.Resampling.LANCZOS)
    logo_w, logo_h = logo.size

    logo_x = half_width + (half_width - logo_w) // 2
    logo_y = (FULL_HEIGHT - logo_h) // 2
    front_img.paste(logo, (logo_x, logo_y), mask=logo)
except Exception as e:
    # Fallback to pure RGB if RGBA fails
    try:
        logo = Image.open('logo.jpg')
        logo_target_w = half_width - 120
        logo.thumbnail((logo_target_w, FULL_HEIGHT - 120), Image.Resampling.LANCZOS)
        logo_w, logo_h = logo.size
        logo_x = half_width + (half_width - logo_w) // 2
        logo_y = (FULL_HEIGHT - logo_h) // 2
        front_img.paste(logo, (logo_x, logo_y))
    except Exception as e2:
        print(f"Could not load logo: {e2}")

# LEFT HALF: Profile, Contact Info, and QR Code

# Create a circular mask for the profile picture
circle_size = 280
profile_x = (half_width - circle_size) // 2
profile_y = 60

mask = Image.new('L', (circle_size, circle_size), 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.ellipse((0, 0, circle_size, circle_size), fill=255)

# Add gold border around profile
draw_front.ellipse((profile_x - 6, profile_y - 6, profile_x + circle_size + 6, profile_y + circle_size + 6), fill=GOLD)
draw_front.ellipse((profile_x - 2, profile_y - 2, profile_x + circle_size + 2, profile_y + circle_size + 2), fill=BLACK)

try:
    profile = Image.open('profile.jpg')
    w, h = profile.size
    # crop to square
    min_dim = min(w, h)
    left = (w - min_dim)/2
    top = (h - min_dim)/2
    profile = profile.crop((left, top, left+min_dim, top+min_dim))
    profile = profile.resize((circle_size, circle_size), Image.Resampling.LANCZOS)

    # Apply circular mask
    output_profile = ImageOps.fit(profile, mask.size, centering=(0.5, 0.5))
    output_profile.putalpha(mask)

    front_img.paste(output_profile, (profile_x, profile_y), mask=output_profile)
except Exception as e:
    print(f"Could not load profile picture: {e}")

# Text info below profile
name_text = "MARY HENNEDY"
title_text = "REALTOR® | GOLDSTONE REALTY"

y_offset = profile_y + circle_size + 30
draw_front.text(((half_width - get_text_width(name_text, font_xl)) // 2, y_offset), name_text, font=font_xl, fill=GOLD)
y_offset += 65
draw_front.text(((half_width - get_text_width(title_text, font_medium)) // 2, y_offset), title_text, font=font_medium, fill=LIGHT_GRAY)

# Contact block + QR code side-by-side
y_offset += 50
contact_block_x = 40

# Add QR code
qr_size = 110
try:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data("https://domusgpt.github.io/Digibusinesscard/") # Replace with actual URL when hosted
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)

    # Create gold border for QR
    qr_x = half_width - qr_size - 40
    qr_y = y_offset

    draw_front.rectangle([qr_x - 4, qr_y - 4, qr_x + qr_size + 4, qr_y + qr_size + 4], fill=GOLD)
    front_img.paste(qr_img, (qr_x, qr_y))

    # Adjust contact text block width to avoid hitting QR
    max_text_width = qr_x - contact_block_x - 20
except Exception as e:
    print(f"Could not generate QR: {e}")

phone_text = "P: +1 (609) 500-8446"
email_text = "E: maryhennedy@goldstonerealty.com"
web_text = "W: goldstonerealty.com"

text_y = y_offset + 10
draw_front.text((contact_block_x, text_y), phone_text, font=font_small, fill=WHITE)
text_y += 35
draw_front.text((contact_block_x, text_y), email_text, font=font_small, fill=WHITE)
text_y += 35
draw_front.text((contact_block_x, text_y), web_text, font=font_small, fill=WHITE)


# Gold separator line down the middle with subtle styling
draw_front.line([(half_width, 50), (half_width, FULL_HEIGHT - 50)], fill=GOLD, width=3)
# Small gold accents top and bottom of middle line
draw_front.ellipse((half_width - 6, 40, half_width + 6, 52), fill=GOLD)
draw_front.ellipse((half_width - 6, FULL_HEIGHT - 52, half_width + 6, FULL_HEIGHT - 40), fill=GOLD)

# Final full card gold border (inside the bleed area)
border_margin = BLEED + 10
draw_front.rectangle(
    [border_margin, border_margin, FULL_WIDTH - border_margin, FULL_HEIGHT - border_margin],
    outline=GOLD,
    width=2
)

front_img.save('print/Mary_Hennedy_Business_Card_Front_Split.png', dpi=(300, 300))
front_img.save('print/Mary_Hennedy_Business_Card_Front_Split.pdf', resolution=300.0)

print("Split design front generated with premium styling and QR code.")
