import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage
from werkzeug.utils import secure_filename  
from google.api_core.exceptions import GoogleAPIError
load_dotenv()

storage_bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
if not storage_bucket_name:
    raise ValueError("FIREBASE_STORAGE_BUCKET environment variable is not set.")

cred = credentials.Certificate('screen-programing.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': storage_bucket_name
})

def upload_image_to_firebase(image_path, destination_blob_name, max_size_mb=16, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        
    try:
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"File '{image_path}' does not exist.")
        
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            raise ValueError(f"File size exceeds the maximum allowed size of {max_size_mb} MB.")
        
        file_extension = os.path.splitext(image_path)[1].lower().replace('.', '')
        if file_extension not in allowed_extensions:
            raise ValueError(f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}.")
        
        bucket = storage.bucket()
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(image_path)
        blob.make_public()
        return blob.public_url
    
    except FileNotFoundError as fnf_error:
        raise Exception(f"File error: {str(fnf_error)}")
    except ValueError as val_error:
        raise Exception(f"Validation error: {str(val_error)}")
    except GoogleAPIError as api_error:
        raise Exception(f"Google API error: {str(api_error)}")
    except Exception as e:
        raise Exception(f"Error uploading image to Firebase: {str(e)}")





def handle_image_upload(file,upload_folder='uploads'):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    if file.filename == '':
        raise ValueError("No selected file")

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    return file_path


def delete_file_from_upload(file_name, upload_folder='uploads'):
    file_path = os.path.join(upload_folder, file_name)

    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
    else:
        print(f"File {file_path} does not exist.")

def delete_image_from_firebase(image_url):
    file_name = image_url.split('/')[-1]

    bucket = storage.bucket()

    try:
        blob = bucket.blob(file_name)
        blob.delete()
    except Exception as e:
        raise Exception(f"Error deleting image from Firebase: {str(e)}")