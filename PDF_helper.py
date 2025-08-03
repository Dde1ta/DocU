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
    'creation_date':<date: None>,
    'length': <int: number of pages>,
    'header':
    {
        'text':<text of header>,
        'image':<image in the header>
    },
    'pages':
    {
        '0':
        {
            'text':<text in the page as string>,
            'images':<IMAGE object of python of the images in the page>
        } so on
    },
    'footer':{
        'text':<text of header>,
        'image':<image in the header>
    }
}
"""


from pypdf import PdfReader
from pypdf._page import VirtualListImages
from json import JSONEncoder


class Pdf:

    def __init__(self, location):
        self.pdf = PdfReader(location)
        self.parts = []

    def get_page(self, page_number: int) -> str:
        return self.pdf.pages[page_number].extract_text()

    def get_pdf_meta_data(self) -> dict[str, str]:
        meta = self.pdf.metadata

        return {
            'author': meta.author,
            'title': meta.title_raw,
            'subject': meta.subject,
            'creator': meta.creator,
            'producer': meta.producer,
            'creation_date': meta.creation_date,
        }

    def get_pdf(self) -> str:
        ...

    def get_page_images(self, page_number: int) -> VirtualListImages:
        page = self.pdf.pages[page_number]

        images = page.images

        return images


if __name__ == "__main__":
    # testing the reader

    loc = ""

    pdf = Pdf("data/Sample 1.pdf")

    s = pdf.get_page_images(1)

    pdf.pdf.close()
