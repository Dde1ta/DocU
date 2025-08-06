"""
This class job is to convert pdf to json file with useful info

Format :-
{
    'name':<file_name>,
    'author':<author: None>,
    'title':<title: None>,
    'subject':<subject: None>,
    'creator':<creator: None>,
    'producer':<producer: None>,
    'length': <int: number of pages>,
    'text':
    {
        '-1':<Header>
        '0':<str>
    }
    'images'
    {
        '-1': <Header>
        '0': <Image bytes to base64>
    }
}
"""
from collections import defaultdict

from pypdf import PdfReader
from pypdf._page import VirtualListImages, ImageFile
from json import JSONEncoder
import base64


class Pdf:

    def __init__(self, location):
        self.name = location.split('/')[-1][:-4]
        self.pdf = PdfReader(location)
        self.parts = []
        self.images_hash = defaultdict(bool)

    def get_page(self, page_number: int) -> dict:
        page = {'text': self.get_page_text(page_number)}
        images_list = self.get_page_images(page_number)
        image = {}
        for x in images_list:
            image[x.name] = self.serialize_image(x)

        page['images'] = image

        return page

    def get_page_text(self, page_number: int) -> str:
        return self.pdf.pages[page_number].extract_text()

    def get_pdf_meta_data(self) -> dict[str, str]:
        meta = self.pdf.metadata

        return {
            'author': meta.author,
            'title': meta.title_raw,
            'subject': meta.subject,
            'creator': meta.creator,
            'producer': meta.producer,
        }

    def get_pdf_text(self, range_to_scan: list[int]=None) -> dict:
        if range_to_scan is not None:
            i = range_to_scan[0]
            j = range_to_scan[1]
        else:
            i = 1,
            j = self.pdf.get_num_pages()
        texts = {}

        for i in range(i - 1, j):
            texts[i] = self.get_page_text(i)
            print(i)

        return texts

    def get_pdf_images(self, range_to_scan: list[int]=None) -> dict:
        if range_to_scan is not None:
            i = range_to_scan[0]
            j = range_to_scan[1]
        else:
            i = 1,
            j = self.pdf.get_num_pages()

        images = {}
        for i in range(i - 1, j):
            print(i)
            new_image = self.get_page_images(i)
            for x in new_image:
                coded = self.serialize_image(x)
                if coded == {}:
                    continue
                else:
                    images[i] = coded
        return images

    def get_pdf(self, range_to_scan: list[int] =None) -> str:

        to_json = self.get_pdf_meta_data()
        to_json['name'] = self.name

        to_json['text'] = self.get_pdf_text(range_to_scan)

        to_json['images'] = self.get_pdf_images(range_to_scan)

        converter = JSONEncoder()
        converted = converter.encode(to_json)

        return converted

    def serialize_image(self, image: ImageFile) -> dict:
        name = image.name
        byte_array = image.image.tobytes()

        byte_encoded = base64.urlsafe_b64encode(byte_array).decode("utf-8")

        if not self.images_hash[byte_encoded]:

            self.images_hash[byte_encoded] = True

            return {
                "name": name,
                "data": byte_encoded
            }
        else:
            return {}

    def get_page_images(self, page_number: int) -> VirtualListImages:
        page = self.pdf.pages[page_number]

        images = page.images

        return images

    def close(self):
        self.pdf.close()


if __name__ == "__main__":
    # testing the reader

    loc = ""

    pdf = Pdf("data/Sample 1.pdf")

    file = open("../tests/dataOf1.json", 'w')

    s = pdf.get_pdf()

    file.write(s)

    file.close()

    pdf.close()
