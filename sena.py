import codecs
import sys
import os
import re
import zlib
import hashlib

def main():
     command = sys.argv[1]
     
     if command == "init":
         os.mkdir(".sena")
         os.mkdir(".sena/objects")
         os.mkdir(".sena/refs")
         with open(".sena/HEAD", "w") as f:
             f.write("ref: refs/heads/main\n")
         print("Initialized sena directory")
         
     elif command == "cat-file":
        option = sys.argv[2]
        file = sys.argv[3]
        if option == "-p":
            with open(f".sena/objects/{file[:2]}/{file[2:]}", "rb") as file:
                content = file.read()
            decompressed_content = zlib.decompress(content)
            text_data = decompressed_content.decode("utf-8")
            filtered_data = re.sub(r"^.*?\x00", "", text_data)
            print(filtered_data, end="")
            
     elif command == "hash-object":
        file_name = sys.argv[3]
        with open(file_name, "rb") as file:
            content = file.read()
            file_len = len(content)
            prefix = f"blob {file_len}\0".encode('utf-8')
            str_to_hash = prefix + content
            result = hashlib.sha1(str_to_hash)
            sha = result.hexdigest()
        os.mkdir(f".sena/objects/{sha[:2]}")
        with open(f".sena/objects/{sha[:2]}/{sha[2:]}", "wb") as new_file:
            compressed_file = zlib.compress(str_to_hash)
            new_file.write(compressed_file)
        print(sha)
        
     elif command == "ls-tree":
        terminal_input_len = len(sys.argv)
        if terminal_input_len == 3:
            # Aqui vai a ls-tree completa
            teste = 0
        else:
            option = sys.argv[2]
            tree_sha = sys.argv[3]
            if option == "--name-only":
                with open(f".sena/objects/{tree_sha[:2]}/{tree_sha[2:]}", "rb") as file:
                    compressed_content = file.read()
                decompressed_content = zlib.decompress(compressed_content)
                header, content = decompressed_content.split(b"\0", 1)
                while content:
                    mode_name, content = content.split(b"\0", 1)
                    hash_, content = content[:20], content[20:]
                    mode_name = mode_name.decode("utf-8")
                    mode, name = mode_name.split(" ")
                    print(name)

     else:
         raise RuntimeError(f"Unknown command {command}")

if __name__ == "__main__":
    main()