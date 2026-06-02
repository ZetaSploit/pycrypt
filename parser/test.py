from collections import defaultdict
from pathlib import Path
import hashlib


def hash_file(path: Path, chunk_size: int = 4096) -> str:
    sha256 = hashlib.sha256()

    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(directory: str):
    hashes = defaultdict(list)

    for file in Path(directory).rglob("*"):
        if file.is_file():
            try:
                file_hash = hash_file(file)
                hashes[file_hash].append(file)
            except PermissionError:
                continue

    duplicates = {
        h: paths
        for h, paths in hashes.items()
        if len(paths) > 1
    }

    return duplicates


if __name__ == "__main__":
    dupes = find_duplicates(".")

    if not dupes:
        print("No duplicate files found.")
    else:
        for file_hash, files in dupes.items():
            print(f"\nDuplicate group: {file_hash[:12]}...")
            for f in files:
                print(f"  - {f}")
