import os
import firebase_admin
from firebase_admin import credentials, storage
from werkzeug.utils import secure_filename

cred = credentials.Certificate('db/quokka-credentials.json') #alterar
firebase_admin.initialize_app(cred, {
    'storageBucket': 'quokka-3fca5.appspot.com'
})

def upload_image_to_firebase(image_path, destination_blob_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(image_path)
        blob.make_public()
        return blob.public_url
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