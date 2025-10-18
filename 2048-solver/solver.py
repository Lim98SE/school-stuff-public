import pydirectinput as pyautogui
import pytesseract as tess
from PIL import ImageGrab, Image, ImageEnhance

tess.pytesseract.tesseract_cmd = r"C:\Users\934713\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
tess_config = r"--oem 1 --psm 7 --dpi 70 digits"

ss_start = [715, 220]
tile_size = 106
margin_size = 15
threshold = 100

def coords_to_screen(coords):
    x = ss_start[0] + margin_size + (tile_size * coords[0]) + (margin_size * coords[0])
    y = ss_start[1] + margin_size + (tile_size * coords[1]) + (margin_size * coords[1])
    return [x, y]

class Tile:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.value = val

def get_tiles():
    state = []
    for y in range(4):
        for x in range(4):
            coords = coords_to_screen([x, y])
            region = [coords[0], coords[1], coords[0] + tile_size, coords[1] + tile_size]

            ss = ImageGrab.grab(region)
            ss = ss.convert("LA")

            ss = ImageEnhance.Contrast(ss).enhance(5.0)

            ss.save(f"cell_{x}_{y}.png")
            cell = tess.image_to_string(Image.open(f"cell_{x}_{y}.png"), "eng", config=tess_config)
            cell = cell.strip()

            if (cell) == "":
                continue
            
            else:
                value = (int(cell))
            
            final_cell = Tile(x, y, value)

            state.append(final_cell)
    
    return state

state = get_tiles()

for i in state:
    print(i.x, i.y, i.value)