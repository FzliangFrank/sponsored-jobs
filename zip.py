import zipfile

files=['app.py','Dockerfile','requirements.txt']

with zipfile.ZipFile('dockerpack.zip','w') as archive:
    for f in files:
        archive.write(f)