from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


"""
private
https://jack-public2023.s3.amazonaws.com/private/products/2024/03/16/apple.jpeg?AWSAccessKeyId=AKIA3X52F2LXRN3TJZGH&Signature=ww4oSbqbfjGVQTefulbgzAQ94Q0%3D&Expires=1710561208
https://jack-public2023.s3.amazonaws.com/private/products/2024/03/16/apple.jpeg?AWSAccessKeyId=AKIA3X52F2LXRN3TJZGH&Signature=hXwtDUlitoLs9RN7VdPtIWX4Vfk%3D&Expires=1710561560
https://jack-public2023.s3.amazonaws.com/private/products/2024/03/16/iphone-15-pro-finish-select-202309-6-7inch-bluetitanium.jpeg?AWSAccessKeyId=AKIA3X52F2LXRN3TJZGH&Signature=a2iDB6NYa%2FVvfCbII%2Ft0BRRA0Mg%3D&Expires=1710561560

public
https://jack-public2023.s3.amazonaws.com/media/products/2024/03/16/apple.jpeg



"""
