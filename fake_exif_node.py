import os
import datetime
import numpy as np
from PIL import Image
import folder_paths

def convert_to_degrees(value):
    """Helper function to convert GPS coordinates to degrees/minutes/seconds for EXIF"""
    d = int(value)
    m = int((value - d) * 60)
    s = (value - d - (m / 60.0)) * 3600.0
    
    # Exif rational representation: (numerator, denominator)
    return ((d, 1), (m, 1), (int(s * 1000000), 1000000))

class SaveImageWithFakeEXIF:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ),
                     "filename_prefix": ("STRING", {"default": "IMG"}),
                     "format": (["jpg", "png"], {"default": "jpg"}),
                     "camera_make": ("STRING", {"default": "Apple"}),
                     "camera_model": ("STRING", {"default": "iPhone 16 Pro Max"}),
                     "latitude": ("FLOAT", {"default": 48.8566, "min": -90.0, "max": 90.0, "step": 0.0001}),
                     "longitude": ("FLOAT", {"default": 2.3522, "min": -180.0, "max": 180.0, "step": 0.0001}),
                     }
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def save_images(self, images, filename_prefix="IMG", format="jpg", camera_make="Apple", camera_model="iPhone 16 Pro Max", latitude=48.8566, longitude=2.3522):
        import piexif
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        
        for batch_number, image in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # Create EXIF data
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
            # Make & Model
            exif_dict["0th"][piexif.ImageIFD.Make] = camera_make.encode('utf-8')
            exif_dict["0th"][piexif.ImageIFD.Model] = camera_model.encode('utf-8')
            
            # Date Time (Fully Automatic)
            dt = datetime.datetime.now()
            dt_formatted = dt.strftime("%Y:%m:%d %H:%M:%S")
            
            exif_dict["0th"][piexif.ImageIFD.DateTime] = dt_formatted.encode('utf-8')
            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = dt_formatted.encode('utf-8')
            exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = dt_formatted.encode('utf-8')
            
            # GPS
            gps_lat = convert_to_degrees(abs(latitude))
            gps_lat_ref = b'N' if latitude >= 0 else b'S'
            gps_lon = convert_to_degrees(abs(longitude))
            gps_lon_ref = b'E' if longitude >= 0 else b'W'
            
            exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = gps_lat_ref
            exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = gps_lat
            exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = gps_lon_ref
            exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = gps_lon
            
            # Optional: Add realistic software version to look authentic
            exif_dict["0th"][piexif.ImageIFD.Software] = b"17.4.1" 
            
            exif_bytes = piexif.dump(exif_dict)
            # Construction du nom de fichier avec Date et Heure
            dt_filename = dt.strftime("%Y%m%d_%H%M%S")
            file = f"{filename}_{dt_filename}_{counter:05}.{format}"
            output_file_path = os.path.join(full_output_folder, file)
            
            save_format = format.upper()
            if save_format == "JPG":
                save_format = "JPEG"
                
            img.save(output_file_path, format=save_format, exif=exif_bytes)
            
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return { "ui": { "images": results } }

NODE_CLASS_MAPPINGS = {
    "SaveImageWithFakeEXIF": SaveImageWithFakeEXIF
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageWithFakeEXIF": "Save Image (Fake EXIF)"
}
