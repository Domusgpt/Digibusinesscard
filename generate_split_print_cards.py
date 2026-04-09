from PIL import Image, ImageDraw, ImageFont
import os

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
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except Exception as e:
    font_large = font_medium = font_small = ImageFont.load_default()

def get_text_width(text, font):
    if hasattr(font, 'getbbox'):
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0]
    return len(text) * 20

# --- SPLIT FRONT OF CARD ---
front_img = Image.new('RGB', (FULL_WIDTH, FULL_HEIGHT), BLACK)
draw_front = ImageDraw.Draw(front_img)

half_width = FULL_WIDTH // 2

# LEFT HALF: Top portion Profile, Bottom portion Contact Info

# Top Left: Profile picture
profile_height = int(FULL_HEIGHT * 0.6)
try:
    profile = Image.open('profile.jpg')
    w, h = profile.size
    target_ratio = half_width / profile_height
    img_ratio = w / h

    if img_ratio > target_ratio:
        new_w = h * target_ratio
        left = (w - new_w) / 2
        right = (w + new_w) / 2
        profile = profile.crop((left, 0, right, h))
    else:
        new_h = w / target_ratio
        top = (h - new_h) / 2
        bottom = (h + new_h) / 2
        profile = profile.crop((0, top, w, bottom))

    profile = profile.resize((half_width, profile_height), Image.Resampling.LANCZOS)
    front_img.paste(profile, (0, 0))
except Exception as e:
    print(f"Could not load profile picture: {e}")

# Bottom Left: Contact Info
name_text = "MARY HENNEDY"
title_text = "REALTOR® | GOLDSTONE REALTY"

phone_text = "P: +1 (609) 500-8446"
email_text = "E: maryhennedy@goldstonerealty.com"
web_text = "W: goldstonerealty.com"

y_offset = profile_height + 15
draw_front.text(((half_width - get_text_width(name_text, font_large)) // 2, y_offset), name_text, font=font_large, fill=GOLD)
y_offset += 40
draw_front.text(((half_width - get_text_width(title_text, font_medium)) // 2, y_offset), title_text, font=font_medium, fill=LIGHT_GRAY)

y_offset += 40
# Contact info left-aligned within a block on the left half
contact_block_x = 20
draw_front.text((contact_block_x, y_offset), phone_text, font=font_small, fill=WHITE)
y_offset += 30
draw_front.text((contact_block_x, y_offset), email_text, font=font_small, fill=WHITE)
y_offset += 30
draw_front.text((contact_block_x, y_offset), web_text, font=font_small, fill=WHITE)

# Gold separator line down the middle
draw_front.line([(half_width, 0), (half_width, FULL_HEIGHT)], fill=GOLD, width=4)

# RIGHT HALF: Logo Center
try:
    logo = Image.open('logo.jpg')
    # Let's crop the logo slightly if it has a lot of black margin, or just resize
    logo_target_w = half_width - 80
    logo.thumbnail((logo_target_w, FULL_HEIGHT - 80), Image.Resampling.LANCZOS)
    logo_w, logo_h = logo.size

    logo_x = half_width + (half_width - logo_w) // 2
    logo_y = (FULL_HEIGHT - logo_h) // 2
    front_img.paste(logo, (logo_x, logo_y))
except Exception as e:
    print(f"Could not load logo: {e}")

front_img.save('print/Mary_Hennedy_Business_Card_Front_Split.png', dpi=(300, 300))
front_img.save('print/Mary_Hennedy_Business_Card_Front_Split.pdf', resolution=300.0)

print("Split design front generated.")
