from pathlib import Path
from document_loader import load_single_pdf

DATA_DIR = Path(__file__).parent / "data"


def find_pdfs(data_dir: Path) -> list[Path]:
    """Recursively find all PDF files under the data directory."""
    return sorted(data_dir.rglob("*.pdf"))


def main() -> None:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Missing data directory: {DATA_DIR}")

    pdf_paths = find_pdfs(DATA_DIR)

    if not pdf_paths:
        print(f"0 PDFs found in {DATA_DIR}")
        return

    print(f"Found {len(pdf_paths)} PDF(s) in {DATA_DIR}:")

    total_pages = 0

    for pdf_path in pdf_paths:
        docs = load_single_pdf(str(pdf_path))
        pages_in_this_pdf = len(docs)
        total_pages += pages_in_this_pdf

        print(f" - {pdf_path.name} -> {pages_in_this_pdf} page(s)")

    total_documents = len(pdf_paths)

    print("\n✅ Ingest complete!!!! ^-^")
    print(f"Total documents loaded: {total_documents}")
    print(f"Total pages loaded: {total_pages}")


if __name__ == "__main__":
    main()
