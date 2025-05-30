from django.core.files.uploadedfile import UploadedFile
from supabase import Client


def upload_file_to_supabase(supabase: Client, bucket_name: str, file: UploadedFile, path: str) -> str:
    """
    Faylni Supabase storage ga yuklaydi.
    :param supabase: Supabase Client obyekti
    :param bucket_name: bucket nomi (masalan 'media')
    :param file: Django UploadedFile obyekti
    :param path: Faylni bucket ichidagi yo'li (masalan 'audio/song.mp3')
    :return: Yuklangan fayl URL'i
    """
    file_data = file.read()
    response = supabase.storage.from_(bucket_name).upload(path, file_data)
    if response.get("error"):
        raise Exception(f"Upload error: {response['error']['message']}")

    # Fayl URL sini olish uchun
    url = supabase.storage.from_(bucket_name).get_public_url(path)
    return url
