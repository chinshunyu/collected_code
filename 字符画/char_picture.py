from PIL import Image

IMG = '/Users/junyongchen/Desktop/coding_study/实用代码块收藏/字符画/pictures/1.jpg'
WIDTH = 80
HEIGHT = 40
OUTPUT = './ascii.txt'

ascii_char = list('@#$%^&*jdioefhowfZMLASNFOIELFPW-][./,?].,<>!')


# 将256灰度映射到字符上
def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


im = Image.open(IMG)
im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

txt = ''

for i in range(HEIGHT):
    for j in range(WIDTH):
        txt += get_char(*im.getpixel((j, i)))
    txt += '\n'
print(txt)

with open(OUTPUT, 'w') as f:
    f.write(txt)
