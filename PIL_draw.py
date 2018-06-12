import os
from PIL import Image, ImageDraw, ImageFont
import argparse
from bs4 import BeautifulSoup
import glob


font = ImageFont.truetype("simsun.ttc",20)


def draw_rectangle(im, box, name):
    assert len(box)== 4 and isinstance(box, list), "box 不合法"
    draw_img = ImageDraw.Draw(im)
    draw_img.rectangle(box, outline=(0,255,0))

    draw_img.text((box[2], box[3]), name, fill=(255,255,0), font=font)
    return im


def main_argparse():
    parser = argparse.ArgumentParser(description="参数说明")
    parser.add_argument('-img', help="输入的图片路径")
    parser.add_argument("-xml", help="图片对应的xml标签")
    parser.add_argument("-outdir", help="图片输出目录")
    return parser.parse_args()

def parse_xml(args):
    xmls = glob.glob(os.path.join(args.xml,'*.xml'))

    print(os.path.join(args.xml,'*.xml'))
    for xml in xmls:
        print(repr(xml))
        try:
            soup = BeautifulSoup(open(xml, 'r'), "lxml")

            file_name = soup.find('filename').get_text()
            im = Image.open(os.path.join(args.img,file_name + '.jpg'))

            for object in soup.find_all('object'):
                label = object.find('name').get_text()
                xmin = int(object.find('xmin').get_text())
                ymin = int(object.find('ymin').get_text())
                xmax = int(object.find('xmax').get_text())
                ymax = int(object.find('ymax').get_text())
                im = draw_rectangle(im, [xmin,ymin,xmax,ymax], label)
            if not os.path.exists(args.outdir):
                os.makedirs(args.outdir)
            im.save('{outdir}/{img_file}.jpg'.format(outdir=args.outdir, img_file=file_name))
        except Exception as e:

            print(e)
            # exit()


if __name__ == '__main__':
    args = main_argparse()
    print(args)
    parse_xml(args)
    print('处理完成！')
