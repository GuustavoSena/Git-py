import sys
import os

def main():
     command = sys.argv[1]
     if command == "init":
         os.mkdir(".sena")
         os.mkdir(".sena/objects")
         os.mkdir(".sena/refs")
         with open(".sena/HEAD", "w") as f:
             f.write("ref: refs/heads/main\n")
         print("Initialized git directory")
     else:
         raise RuntimeError(f"Unknown command {command}")

if __name__ == "__main__":
    main()