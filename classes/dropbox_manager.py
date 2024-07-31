import sqlite3
import dropbox


class DropBox:
    
    def __init__(self, token):

        self.ACCESS_TOKEN = token
        # connect
        self.dbx = dropbox.Dropbox(self.ACCESS_TOKEN)

        # Paths
        self.dropbox_download_path = '/DataBase.db'
        self.local_download_path = 'bases/DataBase.db'

    def download_file_from_dropbox(self):
        """Download a file from Dropbox to the local system."""
        try:
            with open(self.local_download_path, "wb") as f:

                metadata, res = self.dbx.files_download(path=self.dropbox_download_path)
                f.write(res.content)
            print(f"File downloaded from {self.dropbox_download_path} to {self.local_download_path}")
            return 1
        except dropbox.exceptions.ApiError as err:
            print(f"Failed to download file from Dropbox: {err}")
            return -1

    def upload_file_to_dropbox(self):
        """Upload a file from the local system to Dropbox."""
        try:
            with open(self.dropbox_download_path, "rb") as f:
                self.dbx.files_upload(f.read(), self.dropbox_download_path, mode=dropbox.files.WriteMode("overwrite"))
            print(f"File uploaded from {self.dropbox_download_path} to {self.dropbox_download_path}")
            return 1
        except dropbox.exceptions.ApiError as err:
            print(f"Failed to upload file to Dropbox: {err}")
            return -1

    def download_dropbox(self):
        # Download the file from Dropbox
        err = self.download_file_from_dropbox()
        return err


    def upload_dropbox(self):
        # Upload the file to Dropbox
        err = self.upload_file_to_dropbox()
        return err
    
    def download_dumps(self):
        """Download a file from Dropbox to the local system."""
        try:
            with open('bases/benchling_dump.csv', "wb") as f:

                metadata, res = self.dbx.files_download(path="/benchling_dump.csv")
                f.write(res.content)
                
            return 1
        except dropbox.exceptions.ApiError as err:
            print(f"Failed to download file from Dropbox: {err}")
            return -1

    @property
    def download_path(self):
        return self.local_download_path
    
if __name__ == "__main__":
    try:
        person = DropBox()
        _ = DropBox.download_dropbox()
        print("DropBox class created")
    except:
        print("Employee class failed")