from PIL import Image, ImageDraw, ImageFont
from pypinyin import STYLE_TONE, pinyin
import re

# 字体文件路径，根据你的系统和字体文件的位置进行修改
font_path = '/System/Library/Fonts/Supplemental/Songti.ttc'

# 从文件中读取汉字
with open('characters.txt', 'r', encoding='utf8') as f:
    lines = f.readlines()
    chinese_characters = [char for line in lines for char in line.strip(
    ) if re.match(r'^[\u4e00-\u9fff]+$', char)]

# 每30个汉字一组
groups = [chinese_characters[i:i+30]
          for i in range(0, len(chinese_characters), 30)]

for group_index, group in enumerate(groups):
    # 创建一个空白图片
    img = Image.new('RGB', (2600, 3200), color=(255, 255, 255))

    d = ImageDraw.Draw(img)

    # 加载字体
    fnt = ImageFont.truetype(font_path, 180)
    fnt_pinyin = ImageFont.truetype(font_path, 100)

    # 为每个汉字生成一个格子
    for i, character in enumerate(group):
        row = i // 5
        col = i % 5

        x = 100 + col * 500
        y = 100 + row * 500

        # 获得汉字的拼音
        pinyin_with_tone = pinyin(character, style=STYLE_TONE)

        # 在格子里写拼音
        d.text(
            (x+100, y), ''.join(pinyin_with_tone[0]), font=fnt_pinyin, fill=(0, 0, 0))

        # 在格子里写汉字
        d.text((x+100, y + 150), character, font=fnt, fill=(0, 0, 0))

        # 为格子添加边框
        d.rectangle([x, y, x + 400, y + 400], outline=(0, 0, 0))

    # 保存图片，每个图片的文件名都是基于其组的索引
    img.save(f'card_{group_index}.png')
