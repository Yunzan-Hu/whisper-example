# build image:
cd build
docker build . -t <your/repo/and/tag>

# deploy on kubernetes
change the image address in file kubernetes/deployment.yaml, and then apply it on DCE5

# test it
cd example
python3 client.py
(make sure the audio file path is correct)
