# Import Required Libraries
import heapq
from collections import defaultdict

# === Run-Length Encoding Functions ===
def run_length_encoding(data):
    encoded_data = []
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            count += 1
            i += 1
        encoded_data.append(f"{data[i]}{count}")
        i += 1
    return ''.join(encoded_data)

def run_length_decoding(encoded_data):
    decoded_data = []
    i = 0
    while i < len(encoded_data):
        symbol = encoded_data[i]
        count = int(encoded_data[i+1])
        decoded_data.append(symbol * count)
        i += 2
    return ''.join(decoded_data)

# === Huffman Coding Functions ===
def calculate_frequencies(data):
    freq = defaultdict(int)
    for symbol in data:
        freq[symbol] += 1
    return freq

def build_priority_queue(freq):
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)
    return heap

def build_huffman_tree(heap):
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def create_huffman_dict(huffman_tree):
    huff_dict = {}
    for symbol, code in huffman_tree:
        huff_dict[symbol] = code
    return huff_dict

def huffman_encoding(data, huff_dict):
    return ''.join(huff_dict[symbol] for symbol in data)

def huffman_decoding(compressed_data, huff_dict):
    reverse_huff_dict = {v: k for k, v in huff_dict.items()}
    decoded_data = []
    temp = ""
    for bit in compressed_data:
        temp += bit
        if temp in reverse_huff_dict:
            decoded_data.append(reverse_huff_dict[temp])
            temp = ""
    return ''.join(decoded_data)

# === Compression and Decompression Functions ===
def compress(data):
    rle_data = run_length_encoding(data)
    frequencies = calculate_frequencies(rle_data)
    heap = build_priority_queue(frequencies)
    huffman_tree = build_huffman_tree(heap)
    huff_dict = create_huffman_dict(huffman_tree)
    compressed_data = huffman_encoding(rle_data, huff_dict)
    return compressed_data, huff_dict

def decompress(compressed_data, huff_dict):
    huffman_decoded_data = huffman_decoding(compressed_data, huff_dict)
    original_data = run_length_decoding(huffman_decoded_data)
    return original_data

# === Testing and Execution ===
if __name__ == "__main__":
    data = "aaaaabbbbcccddehhjjkhkjkjlkolkoksoko;kojijihuygftcdjikjolko;k;kjiugt"
    compressed_data, huff_dict = compress(data)
    print(f"Compressed Data: {compressed_data}")
    decompressed_data = decompress(compressed_data, huff_dict)
    print(f"Decompressed Data: {decompressed_data}")
    assert data == decompressed_data, "Decompression failed!"
