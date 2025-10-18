import qrcode
from PIL import Image

for i in range(3):
    qr = qrcode.QRCode(version = 40)

    with open("bee-movie.txt") as file:
        qr.add_data(file.read()[1000 * i:1000 * (i + 1)])

    print(qr.version)

    qr.make(fit=True)

    image = qr.make_image(fill="black", back_color="white")
    image.save(f"qr_{i}.png")