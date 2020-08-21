from PIL import Image
from PIL import UnidentifiedImageError


class WB:
    class RectangleCursor:
        def __init__(self, left_top: tuple, right_bottom: tuple):
            """ Initialized rect cursor which should be used in data writing or reading"""
            self.left_x, self.top_y = left_top
            self.right_x, self.bottom_y = right_bottom
            self.width = self.right_x - self.left_x
            self.height = self.bottom_y - self.top_y

        def __call__(self):
            return self.__next_position_gen()

        def __next_position_gen(self):
            """ Generator whose __next__ method returns the next empty pixel"""
            for horizontal in range(self.width):
                for vertical in range(self.height):
                    yield (horizontal + self.left_x, vertical + self.top_y)

    @staticmethod
    def __generate_border(img: Image.Image):
        """ Generates border 1px black, 1px white, 1px black. Rewrites image pixels (doesn't create new)"""
        for i in range(img.width):
            img.putpixel((i, 0), 0)
            img.putpixel((i, img.width - 1), 0)
            img.putpixel((0, i), 0)
            img.putpixel((img.width - 1, i), 0)
        for i in range(1, img.width - 1):
            img.putpixel((i, 1), 1)
            img.putpixel((i, img.width - 2), 1)
            img.putpixel((1, i), 1)
            img.putpixel((img.width - 2, i), 1)
        for i in range(2, img.width - 2):
            img.putpixel((i, 2), 0)
            img.putpixel((i, img.width - 3), 0)
            img.putpixel((2, i), 0)
            img.putpixel((img.width - 3, i), 0)

    @staticmethod
    def row_encrypt(data: str, file_name: str = 'default.png'):
        """ Writes your data in file_name image"""
        size = int((len(data) * 8) ** (1/2)) + 8
        img: Image.Image = Image.new(mode='1', size=(size, size))
        WB.__generate_border(img)
        cursor = WB.RectangleCursor((3, 3), (size-4, size-4))
        byte_list: list = []
        for x in data:
            byte = str(bin(ord(x)))[2:]
            byte_list.append('0'*(8-len(byte)) + byte)
        byte_string = ''.join(byte_list)
        for pixel_pos, bit in zip(cursor(), byte_string):
            img.putpixel(pixel_pos, int(bit))
        img.save(file_name)
        return img

    @staticmethod
    def row_decrypt(file_name: str = 'default.png'):
        """ Decrypts your data: str from image file with name in :param file_name"""
        try:
            img: Image.Image = Image.open(file_name)
            assert img.width == img.height
            size = img.width
            cursor = WB.RectangleCursor((3, 3), (size-4, size-4))
            byte = ''
            data = ''
            for number, pixel_pos in enumerate(cursor()):
                bit = str(int(img.getpixel(pixel_pos) == 255))
                if number != 0 and (number + 1) % 8 == 0:
                    byte += bit
                    data += chr(int(byte, 2)) if int(byte) != 0 else ''
                    byte = ''
                else:
                    byte += bit
            else:
                data += chr(int(byte, 2)) if int(byte) != 0 else ''
                byte = ''
            return data

        except FileNotFoundError:
            print('Exception FileNotFoundError got')
        except UnidentifiedImageError:
            print('Exception UnidentifiedImageError got. Maybe your file is corrupted')
        except AssertionError:
            print('Your image is not square')
        data = None
        return data
