import os
import re
from supabase import create_client, Client
import shortuuid

"""
upload_photo_supabase parameters

image           = the image we are trying to upload
image_name      = could be blank, which will activate automatic naming. if argument is given,
                  then won't resort to automatic
bucket          = which bucket to upload the photo, default is lost-item-images.

return value is the url of the image which can be used for creating or editing records.

"""
def upload_photo_supabase(image, bucket="lost-item-images"):

    supabase = create_supabase_instance()

    # Provide unique image name using uuid
    image_name = setup_photo_name(supabase, image, bucket)

    image_data = image.read()

    # Upload image to supabase
    try:
        # Replace the "lost-item-images" by the bucket you are uploading to
        supabase.storage.from_(bucket).upload(
                file=image_data,
                path=image_name,
                file_options={"content-type": image.content_type}
            )
    except:
        return False
    
    # Takes the working URL of the recently uploaded image for storing
    url_response = (
        supabase.storage
        .from_(bucket)
        .get_public_url(image_name)
    )

    # Returns the url of the photo
    return url_response


# Creates a supabase connection
def create_supabase_instance():

    url: str = os.environ.get('SUPABASE_URL')
    key: str = os.environ.get('SUPABASE_KEY')

    supabase: Client = create_client(url, key)

    # Returns supabase object for your needs
    return supabase


# If there is a need for automatic naming, call the function
def setup_photo_name(supabase, image, bucket):

    return shortuuid.uuid() + '.' + image.content_type.split('/')[1]


# Delete photo from Supabase
def delete_photo_supabase(photo_url, bucket="lost-item-images"):
    print(bucket)
    # Create Supabase instance
    supabase = create_supabase_instance()

    # Extract the name of the file with its type for deletion
    photo_url = re.search(r'[\w-]+\.(jpg|jpeg|png|gif|bmp|webp)', photo_url, re.IGNORECASE)
    image_name = ""

    # If there is a match to the pattern, store it to a new variable
    if photo_url:
        image_name = photo_url.group()
        print(image_name)
    else:
        print("ERROR FINDING PHOTO NAME")
        return False
    
    # Delete image from supabase
    response = (
        supabase.storage
        .from_(bucket)
        .remove([image_name])
    )

    return True