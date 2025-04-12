import os
import re
from supabase import create_client, Client

# Uploads image from request to supabase
# If you want to automatically name it, don't add name as argument
def upload_photo_supabase(image, image_name="default"):
    supabase = create_supabase_instance()

    # If it needs dynamic naming
    if image_name == "default":
        image_name = setup_photo_name(supabase, image)
    image_data = image.read()

    # Upload image to supabase
    try:
        # Replace the "lost-item-images" by the bucket you are uploading to
        supabase.storage.from_("lost-item-images").upload(
                file=image_data,
                path=image_name,
                file_options={"content-type": image.content_type}
            )
    except:
        return -1
    
    # Takes the working URL of the recently uploaded image for storing
    url_response = (
        supabase.storage
        .from_("lost-item-images")
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
def setup_photo_name(supabase, image):
    # Get last uploaded image name
    response = (
        supabase.storage
        .from_("lost-item-images")
        .list(
            "",
            {
                "limit": 1,
                "offset": 0,
                "sortBy": {"column": "created_at", "order": "desc"},
            }
        )
    )

    # Get the name of the last item, and find what numbers it has
    item_count = re.findall(r'\d+', response[0].get('name'))

    # Convert said count to integer
    item_count = int(item_count[0])

    # Create string name with prefix, item count + 1, and content_type
    image_name = "image_" + str(item_count + 1) + "." + image.content_type.split('/')[1]

    return image_name