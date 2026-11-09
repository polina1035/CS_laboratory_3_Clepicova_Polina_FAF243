"""
Laboratory work No.3, task 3.1 - Playfair cipher for Romanian (31 letters).

Alphabet (31 letters): A Ă Â B C D E F G H I Î J K L M N O P Q R S Ș T Ț U V W X Y Z
Matrix: 6x6 = 36 cells -> 31 letters + 5 free cells, filled with the symbols 0-4
(the manual allows "any symbols" in free cells).

Input rules (from the task):
  * key, message: only letters A-Z / a-z (diacritics are typed without diacritics);
    spaces are accepted and removed;
  * key length >= 7;
  * cryptogram (for decryption): symbols of the matrix, because a cryptogram can
    contain Ă Â Î Ș Ț and the free symbols 0-4;
  * otherwise the program shows the correct range of characters.
"""

import sys

ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"   # 31 letters
FREE = "01234"                                  # 5 free cells of the 6x6 matrix
ROWS = COLS = 6
MIN_KEY_LEN = 7
FILLER, FILLER_ALT = "X", "Q"                   # inserted between double letters


# ----------------------------------------------------------------- validation
def validate(text, allowed, what):
    """Return (clean_text, None) or (None, error message with the correct range)."""
    text = text.replace(" ", "")
    if not text:
        return None, f"The {what} is empty."
    bad = sorted({c for c in text if c.upper() not in allowed})
    if bad:
        return None, (f"Invalid characters in the {what}: {' '.join(bad)}\n"
                      f"Allowed characters: {describe(allowed)} (spaces are ignored).")
    return text.upper(), None


def describe(allowed):
    if allowed == LATIN:
        return "letters A-Z and a-z"
    return "letters A-Z, a-z, Ă Â Î Ș Ț (ă â î ș ț) and digits 0-4"


LATIN = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
MATRIX_SYMBOLS = set(ALPHABET + FREE)


# --------------------------------------------------------------------- matrix
def prepare_key(key):
    """Remove repeated letters (from the second occurrence)."""
    out = ""
    for ch in key:
        if ch not in out:
            out += ch
    return out


def build_matrix(key, alphabet=ALPHABET + FREE, rows=ROWS, cols=COLS):
    """Fill the matrix row by row: first the key, then the rest of the alphabet."""
    seq = prepare_key(key)
    seq += "".join(ch for ch in alphabet if ch not in seq)
    matrix = [list(seq[r * cols:(r + 1) * cols]) for r in range(rows)]
    pos = {matrix[r][c]: (r, c) for r in range(rows) for c in range(cols)}
    return matrix, pos


def show_matrix(matrix):
    print("Encryption matrix:")
    for row in matrix:
        print("  " + " ".join(row))


# ------------------------------------------------------------- text preparing
def make_pairs(text):
    """Split the text in digraphs; insert X (or Q) between equal letters,
    add X (or Q) at the end if the number of letters is odd."""
    pairs, i = [], 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else None
        if b is not None and b != a:
            pairs.append(a + b)
            i += 2
        else:                                        # double letter or last letter
            pairs.append(a + (FILLER if a != FILLER else FILLER_ALT))
            i += 1
    return pairs


# ---------------------------------------------------------------- the cipher
def crypt_pair(pair, matrix, pos, step, rows=ROWS, cols=COLS):
    """step = +1 for encryption, -1 for decryption."""
    (r1, c1), (r2, c2) = pos[pair[0]], pos[pair[1]]
    if r1 == r2:                                     # same row
        return matrix[r1][(c1 + step) % cols] + matrix[r2][(c2 + step) % cols]
    if c1 == c2:                                     # same column
        return matrix[(r1 + step) % rows][c1] + matrix[(r2 + step) % rows][c2]
    return matrix[r1][c2] + matrix[r2][c1]           # rectangle


def encrypt(message, key):
    matrix, pos = build_matrix(key)
    pairs = make_pairs(message)
    return pairs, [crypt_pair(p, matrix, pos, +1) for p in pairs]


def decrypt(cryptogram, key):
    if len(cryptogram) % 2:
        raise ValueError("The cryptogram must have an even number of characters.")
    matrix, pos = build_matrix(key)
    pairs = [cryptogram[i:i + 2] for i in range(0, len(cryptogram), 2)]
    for p in pairs:
        if p[0] == p[1]:
            raise ValueError(f"Invalid cryptogram: the pair {p} has two equal letters.")
    return pairs, [crypt_pair(p, matrix, pos, -1) for p in pairs]


# ------------------------------------------------------------------ interface
def ask(prompt, allowed, what):
    while True:
        value, error = validate(input(prompt), allowed, what)
        if error:
            print(error)
        else:
            return value


def ask_key():
    while True:
        key = ask("Key: ", LATIN, "key")
        if len(key) < MIN_KEY_LEN:
            print(f"The key must contain at least {MIN_KEY_LEN} letters "
                  f"(you entered {len(key)}).")
        else:
            return key


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("PLAYFAIR CIPHER (Romanian alphabet, 31 letters, 6x6 matrix)")
    while True:
        print("\n1 - Encrypt\n2 - Decrypt\n0 - Exit")
        choice = input("Choose the operation: ").strip()
        if choice == "0":
            break
        if choice not in ("1", "2"):
            print("Please enter 1, 2 or 0.")
            continue
        key = ask_key()
        matrix, _ = build_matrix(key)
        print(f"Prepared key (repeated letters removed): {prepare_key(key)}")
        show_matrix(matrix)
        if choice == "1":
            msg = ask("Message: ", LATIN, "message")
            pairs, enc = encrypt(msg, key)
            print("Prepared text :", " ".join(pairs))
            print("Cryptogram    :", "".join(enc))
        else:
            cg = ask("Cryptogram: ", MATRIX_SYMBOLS, "cryptogram")
            try:
                pairs, dec = decrypt(cg, key)
            except ValueError as e:
                print(e)
                continue
            print("Decrypted pairs:", " ".join(dec))
            print("Decrypted text :", "".join(dec))
            print("(spaces and the filler letters X/Q must be restored manually)")


if __name__ == "__main__":
    main()
