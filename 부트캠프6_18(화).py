# -*- coding: utf-8 -*-
"""부트캠프6/18(화)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cIPYRrEjsjQjvm8wZnp2Q1hLi58WWvRQ
"""

!pip install opencv-python-headless
!pip install dlib

import imutils
print(imutils.__version__)

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = '/mnt/data/image.jpg'  # Sample image path, replace with your image path
image = cv2.imread(image_path)

# Check if the image is loaded correctly
if image is None:
    raise ValueError("Image not loaded. Please check the path.")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load pre-trained face detector and eye detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(30, 30))

# Apply mosaic effect to the eyes
for (x, y, w, h) in faces:
    face_roi_gray = gray[y:y+h, x:x+w]
    face_roi_color = image[y:y+h, x:x+w]

    # Detect eyes in the face region
    eyes = eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10))

    # Apply mosaic effect to each eye
    for (ex, ey, ew, eh) in eyes:
        eye_roi = face_roi_color[ey:ey+eh, ex:ex+ew]
        eye_roi = cv2.resize(eye_roi, (ew//10, eh//10), interpolation=cv2.INTER_NEAREST)
        eye_roi = cv2.resize(eye_roi, (ew, eh), interpolation=cv2.INTER_NEAREST)
        face_roi_color[ey:ey+eh, ex:ex+ew] = eye_roi

    # Overlay the mask on the face
    mask_path = '/mnt/data/mask.png'  # Replace with the actual path of the mask image
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)

    # Check if the mask is loaded correctly
    if mask is None:
        raise ValueError("Mask image not loaded. Please check the path.")

    # Check if mask has alpha channel
    has_alpha = mask.shape[2] == 4

    # Resize the mask to fit the face width
    mask_width = int(w * 0.8)  # Adjust mask width as needed
    mask_height = int(mask.shape[0] * (mask_width / mask.shape[1]))

    # Calculate mask position on the face (bottom 1/3 of the face)
    mask_y = y + int(h * 0.67)  # Bottom 1/3 of the face
    mask_x = x + w // 2 - mask_width // 2  # Center the mask horizontally

    # Ensure the mask fits within the face boundaries
    if mask_x < 0:
        mask_x = 0
    if mask_x + mask_width > image.shape[1]:
        mask_x = image.shape[1] - mask_width
    if mask_y + mask_height > image.shape[0]:
        mask_y = image.shape[0] - mask_height

    # Resize mask to fit the face if necessary
    resized_mask = cv2.resize(mask, (mask_width, mask_height), interpolation=cv2.INTER_AREA)

    # Overlay the mask on the face
    for i in range(mask_height):
        for j in range(mask_width):
            if has_alpha:
                if resized_mask[i, j][3] != 0:  # Check the alpha channel
                    image[mask_y + i, mask_x + j] = resized_mask[i, j][:3]
            else:
                image[mask_y + i, mask_x + j] = resized_mask[i, j]

# Display the final image with the mask applied
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

import qrcode

# 생성할 QR 코드의 데이터 (여기서는 네이버 URL을 예시로 함)
data = "https://www.naver.com"

# QR 코드 생성
qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

# QR 코드 이미지 생성
img = qr.make_image(fill_color="black", back_color="white")

# 이미지를 파일로 저장
img.save("/content/qrcode.png")

# 저장된 이미지 파일의 경로 출력
print("QR 코드 이미지가 저장된 경로:", "/content/qrcode.png")

from IPython.display import Image

# 저장된 QR 코드 이미지 파일의 경로
qr_code_path = "/content/qrcode.png"

# 이미지를 Colab에서 보여주기
Image(qr_code_path)

from tkinter.constants import TRUE
import pandas as pd
import numpy as np
df = pd.DataFrame(
    {"임영웅" : [100, 50, 91, 30],
     "홍길동" : [100, 92, 60, 50],
     "인순이" : [100, 80, 47, 45]},
     index=pd.MultiIndex.from_tuples(
         [("냉장고", "삼성"), ("냉장고", "LG"), ("TV", "삼성"), ("TV", "LG")],
         names=["제품명", "제조사"])
)
df["평균가격"]=(df["임영웅"]+df["홍길동"]+df["인순이"])/3

df.iloc[0:]
# df.describe()
# df.apply(np.sqrt)

"""1. 열이름과 시간표 데이터를 리스트로 작성합니다"""

import pandas as pd

# 데이터 생성
columns = ["과목번호", "과목명", "강의실", "시간수"]
data = [
    ["C1", "AI", "R1", 3],
    ["C2", "빅데이터", "R2", 2],
    ["C3", "경영학", "R3", 3],
    ["C4", "디자인", "R4", 4],
    ["C5", "건축", "R2", 2],
    ["C6", "예술", "R3", 1]
]

"""2)시간표 데이터를 데이터프레임 객체 df로 변환하여 csv파일로 저장합니다."""

# 데이터프레임 생성
df = pd.DataFrame(data, columns=columns)
df

"""3. Timetable.csv파일을 데이터 프레임 객체 df2로 읽고 열을 추가합니다."""

#경로지정하고 csv형식으로 파일 저장
df.to_csv("/content/Timetable.csv")

#파일 불러오기
df2 = pd.read_csv('/content/Timetable.csv')

#열 추가
df2["교수"] = ["임영웅", "이순신", "삼순이", "홍천재", "짬퐁이", "윤석열"]
df2 = df2.drop(columns=["Unnamed: 0"])
df2

"""4.강의실을 기준으로 그룹화하여 최대 시간 수를 구합니다."""

#최댓값 가져오기
max = df2.groupby("강의실")["시간수"].max()
#출력
max