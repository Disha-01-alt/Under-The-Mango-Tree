import shutil

# '.' means zip the current directory (the whole project)
shutil.make_archive('website_backup', 'zip', '.')

print("ZIP file 'website_backup.zip' created successfully.")
