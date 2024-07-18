'''import firebase_admin
from firebase_admin import credentials, storage


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


def delete_image_from_firebase(image_url):
    file_name = image_url.split('/')[-1]

    bucket = storage.bucket()

    try:
        blob = bucket.blob(file_name)
        blob.delete()
    except Exception as e:
        raise Exception(f"Error deleting image from Firebase: {str(e)}")'''