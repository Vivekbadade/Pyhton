import qrcode

def qrcode_generator(data, name):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{name}.png")

data= input("Enter the data to be encoded in the QR code: ").strip()
name = input("Enter the name of the QR code image file (without extension): ").strip()

qrcode_generator(data, name)
