from os import listdir
from os.path import exists
from traceback import format_exc

from PIL import Image


def create_thumbnail(infile, outfile):
    if not '800' in infile and not '200' in infile and not exists(outfile):
        if exists(infile):
            print(resize_image(infile, outfile, 800))
            outfile = outfile.replace('.800.', '.200.')
            print(resize_image(infile, outfile, 200))
        else:
            print('Image not available for resize')


def create_cover_images(path):
    image = Image.open(path)
    print(f'Image: {path} Size: {image.size[0]}x{image.size[1]}')
    print(f'Shape: 1000x{image.size[1]*1000/image.size[0]}')
    image = crop_image(image)

    image = save_image(image, path, 1600)
    image = save_image(image, path, 800)
    image = save_image(image, path, 400)
    image = save_image(image, path, 200)


# def crop_cover_image():
#     path1 = 'Documents/images/CoverArtwork/Originals/pexels-asad-photo-maldives-9470508.jpg'
#     path2 = path1.replace('.jpg', '-crop.jpg')
#     im = Image.open(path1)
#     newsize = im.size[1]*10/16, im.size[1]
#     print(im.size)
#     # offset = im.size[0]/2
#     offset = 0
#     im = im.crop((offset, 0, newsize[0]+offset, newsize[1]))
#     im.save(path2)


def crop_image(image):
    if image.size[1]*1000 > image.size[0]*1600:
        print('Too Tall')
        size = image.size[0], int(image.size[0]*1600/1000)
    else:
        print('Too Wide')
        size = int(image.size[1] * 1000 / 1600), image.size[1]
    offset = 0, 0
    image = image.crop(
        (offset[0], offset[1], size[0]+offset[0], size[1]+offset[1]))
    print(f'Crop Size: {size[0]}x{size[1]}',
          f'Shape: 1000x{int(size[1]*1000/size[0])}')
    print(f'Crop Shape: 1000x{image.size[1]*1000/image.size[0]}')
    return image


def save_image(image, path, size):
    image = image.resize((size, int(size * 16 / 10)))
    path = path.replace('.png', f'-{size}.png')
    path = path.replace('.jpg', f'-{size}.jpg')
    image.save(path)
    print(f'Image: {path} Size: {image.size[0]}x{image.size[1]}')
    print(f'Shape: 1000x{image.size[1] * 1000 / image.size[0]}')
    return image


def downsample_photos(directory):
    for f in listdir(directory):
        infile = f'{directory}/{f}'
        outfile = infile.replace('.png', '.jpg').replace(
            '.jpeg', '.jpg').replace('.jpg', '.800.jpg')
        create_thumbnail(infile, outfile)


def resize_image(path, newpath, size):
    if path != newpath:
        try:
            im = Image.open(path)
            im.thumbnail((int(size*1.6), size))
            im.save(newpath)
        except IOError:
            print(format_exc())
            return "Cannot resize '%s'" % path
    return '%s --> %s (%s pixels)' % (path, newpath, size)


def resize_profile_photos():
    infile = '/Users/seaman/Desktop/MarkSeaman-Full.jpg'
    print(resize_image(infile, '/Users/seaman/Desktop/Mark-Seaman-800.jpg', 800))
    print(resize_image(infile, '/Users/seaman/Desktop/Mark-Seaman-400.jpg', 400))
    print(resize_image(infile, '/Users/seaman/Desktop/Mark-Seaman-200.jpg', 200))
    print(resize_image(infile, '/Users/seaman/Desktop/Mark-Seaman-100.jpg', 100))


def resize_image_file(path, size):
    print(resize_image(path, path.replace('.png', f'-{size}.png'), size))


def resize_book_cover():
    path = 'Documents/images/book/quest/cover.png'
    # path = 'Documents/images/book/journey/cover.png'
    resize_image_file(path, 1600)
    resize_image_file(path, 800)
    resize_image_file(path, 400)
    resize_image_file(path, 200)
