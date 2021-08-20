import os
# from itertools import zip

from PIL import Image, ImageGrab


def iter_rows(pil_image):
    """Yield tuple of pixels for each row in the image.

    From:
    http://stackoverflow.com/a/1625023/1198943

    :param PIL.Image.Image pil_image: Image to read from.

    :return: Yields rows.
    :rtype: tuple
    """
    iterator = zip(*(iter(pil_image.getdata()),) * pil_image.width)
    for row in iterator:
        yield row


def find_subimage(large_image, subimg_path):
    """Find subimg coords in large_image. Strip transparency for simplicity.

    :param PIL.Image.Image large_image: Screen shot to search through.
    :param str subimg_path: Path to subimage file.

    :return: X and Y coordinates of top-left corner of subimage.
    :rtype: tuple
    """
    # Load subimage into memory.
    with Image.open(subimg_path) as rgba, rgba.convert(mode='RGB') as subimg:
        si_pixels = list(subimg.getdata())
        si_width = subimg.width
        si_height = subimg.height
    si_first_row = tuple(si_pixels[:si_width])
    si_first_row_set = set(si_first_row)  # To speed up the search.
    si_first_pixel = si_first_row[0]

    # Look for first row in large_image, then crop and compare pixel arrays.
    for y_pos, row in enumerate(iter_rows(large_image)):
        if si_first_row_set - set(row):
            continue  # Some pixels not found.
        for x_pos in range(large_image.width - si_width + 1):
            if row[x_pos] != si_first_pixel:
                continue  # Pixel does not match.
            if row[x_pos:x_pos + si_width] != si_first_row:
                continue  # First row does not match.
            box = x_pos, y_pos, x_pos + si_width, y_pos + si_height
            with large_image.crop(box) as cropped:
                if list(cropped.getdata()) == si_pixels:
                    # We found our match!
                    return x_pos, y_pos
    return 0, 0


def find_insideimage(subimg_path, bbox_used):
    """Take a screenshot and find the subimage within it.

    :param str subimg_path: Path to subimage file.
    """
    assert os.path.isfile(subimg_path)

    # Take screenshot.
    # (540+65*i, 610, 610+65*i, 680)
    with ImageGrab.grab(bbox = bbox_used) as rgba, rgba.convert(mode='RGB') as screenshot:
        return find_subimage(screenshot, subimg_path)

# for i in range(6):
#     image_found = find_insideimage('imagenes/ability'+str(i)+'.png', (540+65*i, 610, 610+65*i, 680))
#     print(image_found)
# image_found = find_insideimage('imagenes/random.png', (540, 610, 610, 680))
# print(image_found, image_found==(0,0))

# image_found = find_insideimage('imagenes/mercenary_up.png', (525, 480, 600, 550))
# print(image_found)
