from pypdf import PdfReader


class Pdf:

    def __init__(self, location):
        self.pdf = PdfReader(location)
        self.parts = []

    def get_page(self, page_number: int) -> str:
        return self.pdf.pages[page_number].extract_text()

    def get_pdf(self) -> str:
        total = self.pdf.get_num_pages()
        in_file = ""

        for i in range(total):
            in_file += self.get_page(i)

        return in_file


if __name__ == "__main__":
    # testing the reader

    loc = ""

    pdf = Pdf("data/Sample 1.pdf")

    s = pdf.get_pdf()

    print(s.split("\n \n"))


