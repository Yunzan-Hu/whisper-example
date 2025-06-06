# build image:
docker build -f build/Dockerfile -t <your/repo/and/tag>  
镜像内预先下载了5个大小的faster-whisper模型，分别是tiny、base、small、medium及large-v3，如果不想预置这么多模型，请自行修改Dockerfile

# deploy on kubernetes
change the image address in file kubernetes/deployment.yaml, and then apply it on DCE5  
可以通过环境变量“WHISPER_MODEL_SIZE”的值来修改启动的模型大小  

# test it
cd example  
python3 client.py  
(make sure the audio file path is correct)  
