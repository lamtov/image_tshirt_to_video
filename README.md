## Download Anaconda Window: 
https://repo.anaconda.com/archive/Anaconda3-2020.11-Windows-x86_64.exe
## Open Anaconda Prompt For Setup #loi
```sh
conda create -n python_image_to_tshirt_video  python=3.8

conda activate python_image_to_tshirt_video
conda install   -y -c conda-forge opencv
conda install -y -c anaconda tk
conda install -y -c anaconda pillow
conda install -y -c conda-forge pyinstaller
```
## Open Anaconda Prompt For Run # loi
```sh
git clone https://github.com/lamtov/image_tshirt_to_video.git
cd image_tshirt_to_video
conda activate python_image_to_tshirt_video
python main.py
```

## Build window 
```sh
conda create -n minimal_example python=3.7 pyinstaller
conda activate minimal_example
pip install opencv-python
conda install -y -c anaconda tk
conda install -y -c anaconda pillow
```
pyinstaller  --onefile  --add-binary C:/Users/Lam/Documents/TOVANLAM_MMO/Python_PSD/main/opencv_videoio_ffmpeg451_64.dll;.   -F C:/Users/Lam/Documents/TOVANLAM_MMO/Python_PSD/main/tshirt_video_generator.py  -p C:/Users/Lam/.conda/envs/minimal_example/python.exe 

# File chay o trong thu muc dist, phai copy thu muc dataset dat canh de lay font tu dataset/font
