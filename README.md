# Element Wallpaper Generator
\[ English | [한국어](README_ko.md) \]

```python
import requests
import os

url = "https://dongju.molra.com/" # Or http://127.0.0.1:5500
num = "1" # hydrogen

width = 1179
height = 2556

lang = "en"

res = requests.get(f"{url}/wallpaper/{num}/{width}/{height}/{lang}")

image_path = f"wallpaper_{num}_{width}x{height}.jpeg"
    
with open(image_path, 'wb') as f:
    f.write(res.content)

print(f"Downloaded at: {os.path.abspath(image_path)}")
```
You can just copy and run this repo.
