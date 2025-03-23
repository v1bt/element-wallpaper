# 원소 배경화면 생성기
\[ [English](README.md) | 한국어 \]

일상생활에서 기억할 수 있는 주기율표 배경화면 생성기

## 실행하기
이 repo를 복사하여 실행하셔도 됩니다.
```python
import requests
import os

url = "https://dongju.molra.com/" # Or http://127.0.0.1:5500
num = "1" # hydrogen

width = 1179
height = 2556

lang = "en" # ko

res = requests.get(f"{url}/wallpaper/{num}/{width}/{height}/{lang}")

image_path = f"{num}_{width}x{height}.jpeg"
    
with open(image_path, 'wb') as f:
    f.write(res.content)

print(f"다운로드 됨: {os.path.abspath(image_path)}")
```

## 예시
[여기서 예시를 볼 수 있습니다.](https://github.com/v1bt/element-wallpaper/tree/main/examples)

<img src="https://github.com/v1bt/element-wallpaper/blob/main/examples/1_1179x2556.jpeg" width=auto height=350px> <img src="https://github.com/v1bt/element-wallpaper/blob/main/examples/92_2224x1668.jpeg" width=auto height=350px>

## 유의 사항
### 요청 방법
`/wallpaper/원소번호/너비/높이/언어`로 요청해야 합니다.

### 언어 목록
- 한국어 (ko)
- 영어 (en)

### 너비와 높이
너비와 높이는 양수여야 합니다.

### 유효한 원소 번호
유효한 원소 번호 (1~118)를 입력해야 합니다.
