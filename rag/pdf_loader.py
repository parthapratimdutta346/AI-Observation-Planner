import os
import fitz  # PyMuPDF


BOOK_FOLDER = "data/books"


def load_books():
    """
    Loads all PDF books from the data/books folder.

    Returns:
        list of dictionaries:
        {
            "book": book_name,
            "page": page_number,
            "text": extracted_text
        }
    """

    documents = []

    if not os.path.exists(BOOK_FOLDER):
        raise FileNotFoundError(f"{BOOK_FOLDER} not found.")

    pdf_files = [
        file for file in os.listdir(BOOK_FOLDER)
        if file.lower().endswith(".pdf")
    ]

    print(f"\nFound {len(pdf_files)} PDF(s)\n")

    for pdf in pdf_files:

        pdf_path = os.path.join(BOOK_FOLDER, pdf)

        print(f"Reading {pdf}")

        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):

            page = doc.load_page(page_num)

            text = page.get_text()

            if text.strip():

                documents.append({
                    "book": pdf,
                    "page": page_num + 1,
                    "text": text.strip()
                })

        doc.close()

    return documents


if __name__ == "__main__":

    docs = load_books()

    print(f"\nLoaded {len(docs)} pages.\n")

    print(docs[0])