import re


def clean_text(text):
    """
    Clean extracted PDF text while preserving paragraph structure.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Preserve paragraph breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_documents(
    documents,
    min_chunk_size=400,
    max_chunk_size=900,
):

    chunks = []

    skip_words = {
        "table of contents",
        "contents",
        "copyright",
        "all rights reserved",
        "isbn",
        "published by",
    }

    for doc in documents:

        book = doc["book"]
        page = doc["page"]

        text = clean_text(doc["text"])

        # Skip pages with very little useful text
        if len(text) < 80:
            continue

        lower_text = text.lower()

        # Skip non-content pages
        if any(word in lower_text for word in skip_words):
            continue

        # Detect paragraph boundaries
        if "\n\n" in text:
            units = text.split("\n\n")
        else:
            units = text.split("\n")

        current_chunk = ""
        paragraph = 1

        for unit in units:

            unit = unit.strip()

            if not unit:
                continue

            # Add line to current chunk
            if len(current_chunk) + len(unit) <= max_chunk_size:

                current_chunk += unit + "\n"

            else:

                # Save completed chunk
                if len(current_chunk) >= min_chunk_size:

                    chunk_text = current_chunk.strip()

                    chunks.append({
                        "book": book,
                        "page": page,
                        "paragraph": paragraph,
                        "title": chunk_text.split("\n")[0][:80],
                        "length": len(chunk_text),
                        "text": chunk_text
                    })

                    paragraph += 1

                current_chunk = unit + "\n"

        # Save remaining text
        if current_chunk:

            chunk_text = current_chunk.strip()

            chunks.append({
                "book": book,
                "page": page,
                "paragraph": paragraph,
                "title": chunk_text.split("\n")[0][:80],
                "length": len(chunk_text),
                "text": chunk_text
            })

    return chunks