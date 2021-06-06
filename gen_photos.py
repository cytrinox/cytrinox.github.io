import os
#from PIL import Image, ExifTags
#from PIL.ExifTags import TAGS
import pyexiv2
import datetime
from shutil import copyfile

OUTPUT_MD = "/home/cytrinox/blogs/chaospixel/_posts"
OUTPUT_IMG = "/home/cytrinox/blogs/chaospixel/images/artwork"


directory = "/storage/main/photos/collections/artwork#blog/"


def try_except(success):
    try:
        return success()
    except Exception:
        return None


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".asm") or filename.endswith(".jpg"):
        path = os.path.join(directory, filename)
        imgdest = os.path.join(OUTPUT_IMG, filename)
        print(path)
        metadata = pyexiv2.ImageMetadata(path)
        metadata.read()
        #print(metadata.exif_keys)
        FocalLength = try_except(lambda: metadata['Exif.Photo.FocalLength'].value)
        FNumber = try_except(lambda: float(metadata['Exif.Photo.FNumber'].value))
        ExposureTime = try_except(lambda: metadata['Exif.Photo.ExposureTime'].value)
        ISOSpeedRatings = try_except(lambda: metadata['Exif.Photo.ISOSpeedRatings'].value)
        #CameraOwnerName = metadata['Exif.Photo.CameraOwnerName'].value
        LensModel = try_except(lambda: metadata['Exif.Photo.LensModel'].value)
        #print("focal: {}, ex: {}, f: {}, iso: {}, cp: {}, lens: {}".format(FocalLength, ExposureTime, FNumber, ISOSpeedRatings, CameraOwnerName, LensModel))
        #print(metadata.iptc_keys)
        title = metadata['Iptc.Application2.ObjectName'].value[0]
        desc = ""
        try:
            desc = metadata['Iptc.Application2.Caption'].value[0]
        except:
            pass
        mdfile = "{}-artworkphoto-{}.md".format(datetime.datetime.now().date().isoformat(), title.lower().replace(' ', '-'))
        mdfile = os.path.join(OUTPUT_MD, mdfile)
        if os.path.isfile(imgdest):
            print("File {} already exists".format(imgdest))
            continue
        with open(mdfile, 'w') as f:
            f.write("\n".join(["---", "layout: artwork", 'title: "{}"'.format(title), 'image: "/images/artwork/{}"'.format(filename), 'tags: [photography, landscapes, featured]', 'category: "photography"', '---', '', desc]))
            f.write("\n\n*Copyright:* Daniel Vogelbacher")
            f.write("\n\n\n")
            f.write("#### Capture settings\n\n")
            if LensModel:
                f.write("\n".join(['|**Lens**|{}|\n'.format(LensModel)]))
            if FNumber:
                f.write("\n".join(['|**Aperture**|f/{}|\n'.format(FNumber)]))
            if ExposureTime:
                f.write("\n".join(['|**Exposure**|{} sec|\n'.format(ExposureTime)]))
            if ISOSpeedRatings:
                f.write("\n".join(['|**ISO Speed**|ISO {}|\n'.format(ISOSpeedRatings)]))
            if FocalLength:
                f.write("\n".join(['|**Focal length**|{}mm|\n'.format(FocalLength)]))

        copyfile(path, imgdest)
        #print(title)
        #print(desc)
        continue
    else:
        continue
