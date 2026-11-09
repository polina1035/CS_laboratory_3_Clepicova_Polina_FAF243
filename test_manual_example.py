"""Check of the algorithm against the example from the laboratory manual
(key FIRST AMENDMENT, 5x5 matrix, J replaced by I)."""
import playfair as p

ALPHABET_5X5 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
matrix, pos = p.build_matrix("FIRSTAMENDMENT", ALPHABET_5X5, 5, 5)
print("Matrix:")
for row in matrix:
    print(" ", " ".join(row))

prepared = ("CO NG RE SX SZ SH AL LM MA KE NO LA WR ES PE CT IN GA NE ST AB "
            "LI SH ME NT OF RE LI GI ON OR PR OH IB IT IN GT FR EX EZ EX").split()
expected = ("OWEHEGRYTYNQBVOAEMGDMQVBXINRXGKISMBEDNTFBLOF"
            "NQENDSLIEGOFCRQMPIXEQCFCRFSMKRISGRDXGRGEOMRNSK")  # from the manual

result = "".join(p.crypt_pair(x, matrix, pos, +1, 5, 5) for x in prepared)
print("Prepared text :", " ".join(prepared[:10]), "...")
print("Computed      :", result)
print("From manual   :", expected[:len(result)])
print("Encryption matches the manual:", result == expected[:len(result)])

back = "".join(p.crypt_pair(result[i:i+2], matrix, pos, -1, 5, 5)
               for i in range(0, len(result), 2))
print("Decryption returns the prepared text:", back == "".join(prepared))
