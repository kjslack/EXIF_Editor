from PIL import Image
import piexif
import Tkinter
import tkFileDialog
import copy
import os
from PIL import Image, ImageTk


# Most images will be big, so they need to be scaled to a smaller size.
# The desired_size is the maximum height or width the image should be.
def ScaleImage(image_for_display, desired_size):
    width, height = image_for_display.size
    largest_dimension = max(width,height)
    scaling_factor = float(desired_size) / float(largest_dimension)
    revised_width = int(width*scaling_factor)
    revised_height = int(height*scaling_factor)
    image_for_display = image_for_display.resize((revised_width,revised_height), Image.ANTIALIAS)
    return image_for_display


# Displays the image in a separate window
def DisplayImage(image):
    window = Tkinter.Tk()
    window.minsize(width=image.size[0],height=image.size[1])
    render = ImageTk.PhotoImage(image)
    image_label = Tkinter.Label(image=render)
    image_label.image = render
    image_label.place(x=0, y=0)
    return window


# Opens a gui from which you can select the picture directory you want
def SelectDirectory():
    window = Tkinter.Tk()
    directory_path = tkFileDialog.askdirectory(title = 'Select the Directory to Load Images From')
    window.destroy()
    return directory_path


# Returns a list of the filenames and paths to all the jpg and png images in the directory
def FilesInDirectory(directory_path):
    fileList = []
    # Get all files and subfolders in the directory
    directory_contents = os.listdir(directory_path)

    # Get the filename and path of only the jpg and png image files
    for directory_item in directory_contents:
        if os.path.isfile(directory_path + '/' + directory_item):
            filename, extension = os.path.splitext(directory_item)
            # Only add image type files (.jpg & .png)
            # if the file extension is uppercase, temporarily make it lowercase for the comparison
            if extension.lower() == '.jpg' or extension.lower() == '.png':
                fileList.append(directory_path + '/' +directory_item)
    return fileList


def SetTags():
    pass


# Saves and closes the image
def FinishProcessingImage(exif_bytes):
    image.save("Revised Test Image.jpg", "jpeg", exif=exif_bytes)
    image.close()


if( __name__ == "__main__"):
    directory = SelectDirectory()
    list_of_files = FilesInDirectory(directory)

    for image_file in list_of_files:
        filename = image_file
        #filename = "Test_Image.jpg"

        image = Image.open(filename)

        # Don't mess with the size or formatting of the original image, so work on a copy
        image_for_display = copy.copy(image)

        image_for_display = ScaleImage(image_for_display, 600)
        window = DisplayImage(image_for_display)
        #window.mainloop()  # needed to get the window to work when run from PyCharm

        exif_dict = piexif.load(image.info["exif"])

        description = raw_input("Image Description = ")
        exif_dict['0th'][270] = description

        # Set User Comment Exif Tag 37510
        exif_dict['Exif'][37510] = description

        #SetTags(exif_dict)

        # Converts the revised exif data which is text to a binaryish format for writing back to the image.
        exif_bytes = piexif.dump(exif_dict)

        FinishProcessingImage(exif_bytes)