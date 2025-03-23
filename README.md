# Element Wallpaper Generator
\[ English | [한국어](README_ko.md) \]

Element wallpaper generator that can be memorized in everyday life

## Run
You can just copy and run this repo.
```python
import requests
import os

url = "https://dongju.molra.com/" # Or http://127.0.0.1:5500
num = "1" # hydrogen

width = 1179
height = 2556

lang = "en"

res = requests.get(f"{url}/wallpaper/{num}/{width}/{height}/{lang}")

image_path = f"{num}_{width}x{height}.jpeg"
    
with open(image_path, 'wb') as f:
    f.write(res.content)

print(f"Downloaded at: {os.path.abspath(image_path)}")
```

## Examples
[You can see an example here.](https://github.com/v1bt/element-wallpaper/tree/main/examples)

<img src="https://github.com/v1bt/element-wallpaper/blob/main/examples/1_1179x2556.jpeg" width=auto height=350px> <img src="https://github.com/v1bt/element-wallpaper/blob/main/examples/92_2224x1668.jpeg" width=auto height=350px>

## Notes
### How to Request
You should request it with `/wallpaper/Atomic number/Width/Height/Language`

### Language List
- Korean (ko)
- English (en)

### Width and Height
Width and height must be positive.

### Valid element number
You must enter a valid element number (1-118).
