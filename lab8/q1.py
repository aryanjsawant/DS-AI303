import random

text1 = ''
text2 = ''

with open("doc1.txt", "w") as f:
    f.write(text1)
with open("doc2.txt", "w") as f:
    f.write(text2)

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

doc1 = read_file("doc1.txt")
doc2 = read_file("doc2.txt")

def get_shingles(text, k=2):
    words = text.lower().split()
    return set([' '.join(words[i:i+k]) for i in range(len(words)-k+1)])

shingles1 = get_shingles(doc1, k=2)
shingles2 = get_shingles(doc2, k=2)

print("Shingles of Doc1:", shingles1)
print("Shingles of Doc2:", shingles2)

def jaccard_similarity(set1, set2):
    return len(set1 & set2) / (len(set1 | set2)+1)

exact_jaccard = jaccard_similarity(shingles1, shingles2)
print("\nExact Jaccard Similarity:", round(exact_jaccard, 3))

def minhash_signature(shingles, all_shingles, num_hashes=100):
    signature = []
    shingle_index = {shingle: idx for idx, shingle in enumerate(all_shingles)}

    for i in range(num_hashes):
        a = random.randint(1, 1000)
        b = random.randint(0, 1000)
        p = 2147483647
        min_hash = float('inf')

        for shingle in shingles:
            x = shingle_index[shingle]
            hash_val = (a * x + b) % p
            if hash_val < min_hash:
                min_hash = hash_val
        signature.append(min_hash)
    return signature

all_shingles = list(shingles1 | shingles2)
sig1 = minhash_signature(shingles1, all_shingles)
sig2 = minhash_signature(shingles2, all_shingles)

def estimate_similarity(sig1, sig2):
    matches = sum(1 for i in range(len(sig1)) if sig1[i] == sig2[i])
    return matches / len(sig1)

approx_jaccard = estimate_similarity(sig1, sig2)
print("Estimated Jaccard (via MinHash):", round(approx_jaccard, 3))
