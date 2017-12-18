from boto.s3.key import Key
from zutils.file_util import FileUtil


class S3Util:

    @staticmethod
    def _files(keys):
        return (key for key in keys if not key.name.endswith('/'))

    @staticmethod
    def _folders(keys):
        return (key for key in keys if key.name.endswith('/'))

    @staticmethod
    def download(s3_connection, bucket_name, s3_url, local_filename):
        '''
        Downloads the file from s3 to the local machine

        :param bucket_name: S3 Bucket Name
        :type bucket_name: string
        :param s3_url: URL of the file to be downloaded
        :type s3_url: string
        :param local_filename: Local filename where
            the contents have to be saved
        :type local_filename: string
        '''
        return S3Util.download_file(s3_connection, bucket_name,
                                    s3_url, local_filename)

    @staticmethod
    def download_file(s3_connection, bucket_name, s3_url, local_filename):
        '''
        Downloads the file from s3 to the local machine

        :param bucket_name: S3 Bucket Name
        :type bucket_name: string
        :param s3_url: URL of the file to be downloaded
        :type s3_url: string
        :param local_filename: Local filename where
            the contents have to be saved
        :type local_filename: string
        '''
        bucket = s3_connection.get_bucket(bucket_name)
        key = bucket.get_key(s3_url)
        if key is None:
            return False

        FileUtil.check_and_create_dir(local_filename)
        # saves locally from s3
        key.get_contents_to_filename(local_filename)
        return True

    @staticmethod
    def download_folder(s3_connection, bucket_name, s3_url, local_folder):
        '''
        Downloads the files in the S3 Url locally and
        returns a tuple of (list of files, status)

        :param bucket_name: S3 Bucket Name
        :type bucket_name: string
        :param s3_url: URL of the S3 folder
        :type s3_url: string
        :param local_folder: Local folder
        :type local_folder: string
        '''
        files = []
        try:
            bucket = s3_connection.get_bucket(bucket_name)
            rs = bucket.list(s3_url)
            for key in S3Util._files(rs):
                # saves locally from s3
                filename = local_folder + "/" + key.name
                FileUtil.check_and_create_dir(filename)
                key.get_contents_to_filename(filename)
                files.append(filename)
            return files, True
        except:
            return files, False

    @staticmethod
    def get_sub_folders(s3_connection, bucket_name, s3_url):
        '''
        Returns the immediate sub folders for the given folder.
        It does not recursively traverse subfolders

        :param bucket_name: S3 Bucket Name
        :type bucket_name: string
        :param s3_url: S3 URL of the folder
        :type s3_url: string
        '''
        folders = []
        try:
            bucket = s3_connection.get_bucket(bucket_name)
            rs = bucket.list(s3_url, "/")
            for key in S3Util._folders(rs):
                folders.append(key.name)
            return folders, True
        except:
            return folders, False

    @staticmethod
    def upload_file(s3_connection, bucket_name, s3_url, local_filename):
        '''
        Upload file to amazon S3

        :param bucket_name: Bucket where the file has to be uploaded
        :type bucket_name: string
        :param s3_url: S3 URL
        :type s3_url: string
        :param local_filename: Local file which has to be uploaded
        :type local_filename: strings
        '''
        try:
            bucket = s3_connection.get_bucket(bucket_name)
            key = Key(bucket)
            key.key = s3_url
            key.set_contents_from_filename(local_filename)
            return True
        except:
            return False

    @staticmethod
    def read_file(s3_connection, bucket_name, s3_url):
        '''
        Read json file from s3 and returns content

        :param bucket_name: S3 Bucket Name
        :type bucket_name: string
        :param s3_url: URL of the file to be read
        :type s3_url: string
        '''
        bucket = s3_connection.get_bucket(bucket_name)
        key = bucket.get_key(s3_url)
        if key is None:
            return None

        try:
            data = key.get_contents_as_string()
            return data
        except:
            return None

    @staticmethod
    def get_key(s3_connection, bucket_name, s3_url):
        bucket = s3_connection.get_bucket(bucket_name)
        key = bucket.get_key(s3_url)
        return key

    @staticmethod
    def check_file_exists_in_s3(s3_connection, bucket_name, s3_url):
        key = S3Util.get_key(s3_connection, bucket_name, s3_url)
        if key is None:
            return False
        return True

    @staticmethod
    def delete_file(s3_connection, bucket_name, s3_url):
        '''
        Delete file from amazon S3

        :param bucket_name: Bucket name
        :type bucket_name: string
        :param s3_url: S3 URL
        :type s3_url: string
        '''

        bucket = s3_connection.get_bucket(bucket_name)
        key = bucket.get_key(s3_url)
        if key is None:
            return None

        try:
            key.delete()
            return True
        except:
            return False

    @staticmethod
    def copy_file(s3_connection, bucket_name, s3_source_url, s3_target_url):
        '''
        Copy file from one location to another and delete previous file

        :param bucket_name: Bucket name
        :type bucket_name: string
        :param s3_source_url: S3 source path from where file has been copied
        :type s3_source_url: string
        :param s3_target_url: S3 target path where file should be copied
        type s3_target_url : string
        '''

        bucket = s3_connection.get_bucket(bucket_name)
        source_key = bucket.get_key(s3_source_url)
        if source_key is None:
            return None

        try:
            target_key = source_key.copy(bucket.name, s3_target_url)
            if target_key.exists:
                source_key.delete()
                return True
        except:
            return False

    @staticmethod
    def save_file_from_string(s3_connection, bucket_name, s3_url, content):
        '''
        Save file to amazon S3

        :param bucket_name: Bucket where the file has to be uploaded
        :type bucket_name: string
        :param s3_url: S3 URL
        :type s3_url: string
        :param content: Content of file
        :type content: string
        '''

        try:
            bucket = s3_connection.get_bucket(bucket_name)
            key = bucket.get_key(s3_url)
            key.set_contents_from_string(content)
            key.set_acl('public-read')
            return True
        except:
            return False
