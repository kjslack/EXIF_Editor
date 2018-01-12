from PIL import Image
import piexif

filename = "Test_Image.jpg"

image = Image.open(filename)
exif_dict = piexif.load(image.info["exif"])

print exif_dict

description = raw_input("Image Description = ")
exif_dict['0th'][270] = description
exif_bytes = piexif.dump(exif_dict)

# Set User Comment Exif Tag 37510
exif_dict['Exif'][37510] = description

image.save("Revised Test Image.jpg", "jpeg", exif = exif_bytes)

image.close()