def remove_duplicates(input_file, output_file):
    try:
        # Langkah 1: Baca isi dari file input
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Langkah 2: Hapus duplikat dari daftar
        unique_lines = list(set(lines))

        # Langkah 3: Tulis nilai unik ke file output
        with open(output_file, 'w') as file:
            file.writelines(unique_lines)

        print("Duplikat dihapus dan hasil disimpan di suksesremoveduplikat.txt.")
    except FileNotFoundError:
        print("File tidak ditemukan. Harap periksa jalur file dan coba lagi.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


if __name__ == "__main__":
    # Meminta pengguna memasukkan nama file input
    input_file = input("Masukkan nama file input: ")

    # Nama file output
    output_file = "suksesremoveduplikat.txt"

    remove_duplicates(input_file, output_file)
