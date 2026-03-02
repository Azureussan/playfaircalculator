import streamlit as st
import re

def prepare_text(text):
    """Mempersiapkan teks untuk enkripsi Playfair"""
    # Ubah ke huruf besar dan hapus karakter non-huruf
    text = re.sub(r'[^A-Za-z]', '', text.upper())
    # Ganti J dengan I
    text = text.replace('J', 'I')
    return text

def create_playfair_matrix(key):
    """Membuat matriks Playfair 5x5 dari key yang diberikan"""
    # Siapkan key
    key = prepare_text(key)
    
    # Buat list untuk matriks
    matrix = []
    used_chars = set()
    
    # Tambahkan karakter dari key
    for char in key:
        if char not in used_chars and char != 'J':
            matrix.append(char)
            used_chars.add(char)
    
    # Tambahkan sisa alfabet (kecuali J)
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
    
    # Ubah menjadi matriks 5x5
    playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    
    return playfair_matrix

def display_matrix(matrix):
    """Menampilkan matriks Playfair dalam format tabel"""
    matrix_str = ""
    for row in matrix:
        matrix_str += " | ".join(row) + "\n"
        matrix_str += "-" * 20 + "\n"
    return matrix_str

def find_position(matrix, char):
    """Mencari posisi karakter dalam matriks"""
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None

def process_digraphs(text):
    """Memproses teks menjadi digraf untuk Playfair Cipher"""
    text = prepare_text(text)
    digraphs = []
    i = 0
    
    while i < len(text):
        if i == len(text) - 1:
            # Jika karakter terakhir, tambahkan X
            digraphs.append(text[i] + 'X')
            i += 1
        elif text[i] == text[i+1]:
            # Jika dua karakter sama, sisipkan X
            digraphs.append(text[i] + 'X')
            i += 1
        else:
            digraphs.append(text[i] + text[i+1])
            i += 2
    
    return digraphs

def playfair_encrypt(plaintext, key):
    """Enkripsi teks menggunakan Playfair Cipher"""
    # Buat matriks
    matrix = create_playfair_matrix(key)
    
    # Proses plaintext menjadi digraf
    digraphs = process_digraphs(plaintext)
    
    ciphertext = ""
    
    for digraph in digraphs:
        a, b = digraph[0], digraph[1]
        
        # Cari posisi
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        # Enkripsi berdasarkan aturan Playfair
        if row1 == row2:
            # Baris sama, geser ke kanan
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            # Kolom sama, geser ke bawah
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            # Berbeda baris dan kolom, tukar kolom
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]
    
    return ciphertext, matrix

def playfair_decrypt(ciphertext, key):
    """Dekripsi teks menggunakan Playfair Cipher"""
    # Buat matriks
    matrix = create_playfair_matrix(key)
    
    # Proses ciphertext menjadi digraf
    digraphs = process_digraphs(ciphertext)
    
    plaintext = ""
    
    for digraph in digraphs:
        a, b = digraph[0], digraph[1]
        
        # Cari posisi
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        # Dekripsi berdasarkan aturan Playfair
        if row1 == row2:
            # Baris sama, geser ke kiri
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            # Kolom sama, geser ke atas
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            # Berbeda baris dan kolom, tukar kolom
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
    
    return plaintext, matrix

def main():
    st.set_page_config(
        page_title="Playfair Cipher Calculator",
        layout="wide"
    )
    
    st.title("Playfair Cipher Encryption/Decryption Calculator")
    st.markdown("---")
    
    # Sidebar untuk informasi
    with st.sidebar:
        st.header("About Playfair Cipher")
        st.markdown("""
        **Playfair Cipher** adalah teknik enkripsi simetris yang menggunakan matriks 5x5 
        yang berisi 25 huruf (menggabungkan I dan J).
        
        **Aturan Enkripsi:**
        1. Jika dua huruf dalam baris yang sama → geser ke kanan
        2. Jika dua huruf dalam kolom yang sama → geser ke bawah
        3. Jika berbeda baris dan kolom → tukar kolom
        
        **Aturan Dekripsi:**
        1. Jika dua huruf dalam baris yang sama → geser ke kiri
        2. Jika dua huruf dalam kolom yang sama → geser ke atas
        3. Jika berbeda baris dan kolom → tukar kolom
        """)
        
        st.header("Key Information")
        st.info("""
        **Current Key:** SCHALE
        
        Key ini akan digunakan untuk membuat matriks Playfair 5x5.
        """)
        
        st.header("Notes")
        st.warning("""
        - Huruf J akan diganti dengan I
        - Karakter non-huruf akan dihapus
        - Semua huruf akan diubah menjadi kapital
        """)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input")
        
        # Input teks
        plaintext = st.text_area(
            "Plaintext:",
            value="WHERE ALL MIRACLES BEGIN",
            height=100,
            help="Masukkan teks yang akan dienkripsi"
        )
        
        # Input key
        key = st.text_input(
            "Key:",
            value="SCHALE",
            help="Masukkan kunci untuk enkripsi/dekripsi"
        )
        
        # Pilihan mode
        mode = st.radio(
            "Mode:",
            ["Encrypt", "Decrypt"],
            horizontal=True
        )
        
        # Tombol proses
        if st.button("Process", type="primary"):
            if mode == "Encrypt":
                result, matrix = playfair_encrypt(plaintext, key)
                st.session_state['result'] = result
                st.session_state['matrix'] = matrix
                st.session_state['mode'] = 'encrypt'
            else:
                result, matrix = playfair_decrypt(plaintext, key)
                st.session_state['result'] = result
                st.session_state['matrix'] = matrix
                st.session_state['mode'] = 'decrypt'
    
    with col2:
        st.subheader("Output")
        
        if 'result' in st.session_state:
            # Tampilkan hasil
            st.text_area(
                "Result:",
                value=st.session_state['result'],
                height=100,
                disabled=True
            )
            
            # Tampilkan matriks Playfair
            st.subheader("Playfair Matrix")
            matrix_display = ""
            for row in st.session_state['matrix']:
                matrix_display += "| " + " | ".join(row) + " |\n"
            
            st.text(matrix_display)
            
            # Detail proses
            st.subheader("Process Details")
            
            if st.session_state['mode'] == 'encrypt':
                # Tampilkan proses enkripsi
                digraphs = process_digraphs(plaintext)
                
                st.markdown("**Digraphs:**")
                digraph_text = " ".join([f"{d}" for d in digraphs])
                st.code(digraph_text)
                
                st.markdown("**Encryption Process:**")
                st.info("""
                Setiap pasangan huruf (digraph) diproses berdasarkan aturan Playfair:
                - Baris sama → geser ke kanan
                - Kolom sama → geser ke bawah
                - Berbeda → tukar kolom
                """)
            else:
                # Tampilkan proses dekripsi
                digraphs = process_digraphs(plaintext)
                
                st.markdown("**Digraphs:**")
                digraph_text = " ".join([f"{d}" for d in digraphs])
                st.code(digraph_text)
                
                st.markdown("**Decryption Process:**")
                st.info("""
                Setiap pasangan huruf (digraph) diproses berdasarkan aturan Playfair:
                - Baris sama → geser ke kiri
                - Kolom sama → geser ke atas
                - Berbeda → tukar kolom
                """)
if __name__ == "__main__":
    main()