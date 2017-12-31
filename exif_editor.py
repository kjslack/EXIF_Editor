from PIL import Image
import piexif

filename = "Test_Image.jpg"

image = Image.open(filename)
exif_dict = piexif.load(image.info["exif"])

print exif_dict

exif_dict["0th"]["270"] = "Revised Test Image Description"
exif_bytes = piexif.dump(exif_dict)

image.save("Revised Test Image.jpg", "jpeg", exif = exif_bytes)