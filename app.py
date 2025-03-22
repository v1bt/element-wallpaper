from PIL import Image, ImageDraw, ImageFont
import json
from flask import Flask, send_file, jsonify
from io import BytesIO

app = Flask(__name__)

KO = {
    'H': '수소', 'He': '헬륨', 'Li': '리튬', 'Be': '베릴륨', 'B': '붕소', 'C': '탄소',
    'N': '질소', 'O': '산소', 'F': '플루오린', 'Ne': '네온', 'Na': '나트륨', 'Mg': '마그네슘',
    'Al': '알루미늄', 'Si': '규소', 'P': '인', 'S': '황', 'Cl': '염소', 'Ar': '아르곤',
    'K': '칼륨', 'Ca': '칼슘', 'Sc': '스칸듐', 'Ti': '티타늄', 'V': '바나듐', 'Cr': '크롬',
    'Mn': '망간', 'Fe': '철', 'Co': '코발트', 'Ni': '니켈', 'Cu': '구리', 'Zn': '아연',
    'Ga': '갈륨', 'Ge': '저마늄', 'As': '비소', 'Se': '셀레늄', 'Br': '브로민', 'Kr': '크립톤',
    'Rb': '루비듐', 'Sr': '스트론튬', 'Y': '이트륨', 'Zr': '지르코늄', 'Nb': '니오븀', 'Mo': '몰리브데넘',
    'Tc': '테크네튬', 'Ru': '루테늄', 'Rh': '로듐', 'Pd': '팔라듐', 'Ag': '은', 'Cd': '카드뮴',
    'In': '인듐', 'Sn': '주석', 'Sb': '안티모니', 'Te': '텔루륨', 'I': '아이오딘', 'Xe': '제논',
    'Cs': '세슘', 'Ba': '바륨', 'La': '란타넘', 'Ce': '세륨', 'Pr': '프라세오디뮴', 'Nd': '네오디뮴',
    'Pm': '프로메튬', 'Sm': '사마륨', 'Eu': '유로퓸', 'Gd': '가돌리늄', 'Tb': '터븀', 'Dy': '디스프로슘',
    'Ho': '홀뮴', 'Er': '에르븀', 'Tm': '툴륨', 'Yb': '이터븀', 'Lu': '루테튬', 'Hf': '하프늄',
    'Ta': '탄탈럼', 'W': '텅스텐', 'Re': '레늄', 'Os': '오스뮴', 'Ir': '이리듐', 'Pt': '백금',
    'Au': '금', 'Hg': '수은', 'Tl': '탈륨', 'Pb': '납', 'Bi': '비스무트', 'Po': '폴로늄',
    'At': '아스타틴', 'Rn': '라돈', 'Fr': '프랑슘', 'Ra': '라듐', 'Ac': '악티늄', 'Th': '토륨',
    'Pa': '프로트악티늄', 'U': '우라늄', 'Np': '넵투늄', 'Pu': '플루토늄', 'Am': '아메리슘', 'Cm': '퀴륨',
    'Bk': '버클륨', 'Cf': '캘리포늄', 'Es': '아인슈타이늄', 'Fm': '페르뮴', 'Md': '멘델레븀', 'No': '노벨륨',
    'Lr': '로렌슘', 'Rf': '러더포듐', 'Db': '두브늄', 'Sg': '시보귬', 'Bh': '보륨', 'Hs': '하슘',
    'Mt': '마이트너륨', 'Ds': '다름슈타튬', 'Rg': '뢴트게늄', 'Cn': '코페르니슘', 'Nh': '니호늄', 'Fl': '플레로븀',
    'Mc': '모스코븀', 'Lv': '리버모륨', 'Ts': '테네신', 'Og': '오가네손'
}

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_element_color(atomic_number, symbol):
    if symbol in ['H', 'C', 'N', 'O', 'P', 'S', 'Se']:
        return hex_to_rgb('8ced8c')
    elif symbol in ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']:
        return hex_to_rgb('eace5d')
    elif symbol in ['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra']:
        return hex_to_rgb('f1f165')
    elif ((21 <= atomic_number <= 30) or (39 <= atomic_number <= 48) or 
          (72 <= atomic_number <= 80) or (104 <= atomic_number <= 108)):
        return hex_to_rgb('fac5b7')
    elif 89 <= atomic_number <= 103:
        return hex_to_rgb('f5ccda')
    elif 57 <= atomic_number <= 71:
        return hex_to_rgb('e8d19c')
    elif symbol in ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn', 'Og']:
        return hex_to_rgb('e5bde5')
    elif symbol in ['B', 'Si', 'Ge', 'As', 'Sb', 'Te']:
        return hex_to_rgb('acdfec')
    elif symbol in ['Al', 'Ga', 'In', 'Sn', 'Tl', 'Pb', 'Bi', 'Po', 'At']:
        return hex_to_rgb('acdfec')
    elif 109 <= atomic_number <= 118:
        return hex_to_rgb('eeeeee')
    return (255, 255, 255)

with open('elements/data.json', 'r', encoding='utf-8') as file:
    elements_data = json.load(file)

@app.route('/')
def index():
    return "원소 이미지 생성 서버입니다. '/g/원소번호/너비/높이/언어' 형식으로 요청하세요."

@app.route('/g/<int:atomic_number>/<int:width>/<int:height>/<string:lang>/')
def generate_element_image_with_lang(atomic_number, width, height, lang):
    if atomic_number < 1 or atomic_number > 118:
        return "유효한 원소 번호(1-118)를 입력하세요.", 400
    
    if width <= 0 or height <= 0:
        return "너비와 높이는 양수여야 합니다.", 400
    
    if lang not in ['ko', 'en']:
        return "지원하는 언어는 'ko'(한국어)와 'en'(영어)입니다.", 400
    
    element = next((el for el in elements_data if el['atomicNumber'] == atomic_number), None)
    if not element:
        return f"원소 번호 {atomic_number}에 대한 데이터를 찾을 수 없습니다.", 404
    
    img = create_element_image(element, width, height, lang)
    
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/jpeg')

def create_element_image(element, width, height, lang='ko'):
    atomic_number = element['atomicNumber']
    symbol = element['symbol']
    mass = str(element['atomicMass'])
    
    if lang == 'ko':
        name = KO.get(symbol, symbol)
    else:
        name = element.get('name', symbol)

    aspect_ratio = width / height
    is_landscape = aspect_ratio > 1.0

    img = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_path = 'fonts/pretendard.ttf'

    min_dimension = min(width, height)

    if is_landscape:
        font_huge_size = int(height * 0.35)
        font_large_size = int(height * 0.08)
        font_medium_size = int(height * 0.055)
        font_small_size = int(height * 0.03)
    else:
        font_huge_size = int(height * 0.379)
        font_large_size = int(height * 0.064)
        font_medium_size = int(height * 0.043)
        font_small_size = int(height * 0.021)

    font_huge = ImageFont.truetype('fonts/Pretendard-ExtraBold.ttf', font_huge_size)
    font_large = ImageFont.truetype('fonts/Pretendard-SemiBold.ttf', font_large_size)
    font_medium = ImageFont.truetype(font_path, font_medium_size)
    font_small = ImageFont.truetype(font_path, font_small_size)

    background_color = get_element_color(atomic_number, symbol)
    draw.rectangle([(0, 0), (width, height)], fill=background_color)

    number_color = (0, 0, 0, 50)
    img_temp = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw_temp = ImageDraw.Draw(img_temp)

    atomic_str = str(atomic_number)
    total_width = sum(font_huge.getbbox(char)[2] for char in atomic_str)

    letter_spacing = int(-0.05 * min_dimension) if is_landscape else int(-0.12 * min_dimension)
    total_width_with_spacing = total_width + letter_spacing * (len(atomic_str) - 1)
    start_x = width / 2 - total_width_with_spacing / 2
    
    current_x = start_x
    vertical_offset = int(height * 0.02) if is_landscape else int(height * 0.043)
    
    for char in atomic_str:
        char_width = font_huge.getbbox(char)[2]
        draw_temp.text((current_x + char_width/2, height/2 - vertical_offset), char, 
                      font=font_huge, fill=number_color, anchor='mm')
        current_x += char_width + letter_spacing

    img_rgba = img.convert('RGBA')
    img_rgba.alpha_composite(img_temp)
    img = img_rgba.convert('RGB')
    draw = ImageDraw.Draw(img)

    if is_landscape:
        symbol_offset = int(height * 0.1)
        name_offset = int(height * 0.16)
        mass_offset = int(height * 0.2)
    else:
        symbol_offset = int(height * 0.128)
        name_offset = int(height * 0.192) 
        mass_offset = int(height * 0.235)
    
    draw.text((width/2, height/2 + symbol_offset), symbol, font=font_large, fill=(0, 0, 0), anchor='mm')
    draw.text((width/2, height/2 + name_offset), name, font=font_medium, fill=(0, 0, 0), anchor='mm')
    draw.text((width/2, height/2 + mass_offset), mass, font=font_small, fill=(0, 0, 0), anchor='mm')

    return img

@app.route('/test')
def test():
    return jsonify({
        "status": "ok",
        "message": "서버가 정상적으로 실행 중입니다. PIL 라이브러리를 사용하지 않는 테스트 엔드포인트입니다."
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5500)