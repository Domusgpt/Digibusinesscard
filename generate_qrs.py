import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from PIL import Image

# Website URL (Placeholder)
url_data = "https://your-domain.com/mary-hennedy"

# URL QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=15,
    border=2,
)
qr.add_data(url_data)
qr.make(fit=True)

# Create an elegant QR code: Black background with Gold modules
# Or transparent/white background with Black/Gold modules.
# We'll generate a few options for the user.

# Option 1: Gold on Black
img_1 = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(back_color=(21, 21, 21), front_color=(212, 175, 55))
)
img_1.save("qrcode_gold_on_black.png")

# Option 2: Black on White with rounded dots
img_2 = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(21, 21, 21))
)
img_2.save("qrcode_black_on_white.png")

# VCard QR Code
with open("mary_hennedy.vcf", "r") as f:
    vcard_data = f.read()

qr_vcard = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=2,
)
qr_vcard.add_data(vcard_data)
qr_vcard.make(fit=True)

img_vcard = qr_vcard.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(21, 21, 21))
)
img_vcard.save("qrcode_vcard_direct.png")
print("QR Codes generated successfully.")
