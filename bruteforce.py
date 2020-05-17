import sys
import zipfile as zp

def main():
    # The script assumes that the words in the wordlist are each separated by '\n'
    n = len(sys.argv)
    wordlist_path = None
    zip_file_path = None

    # Verbose mode availible with -v flag. Shows additional prints
    verbose = False
    more_verbose = False

    # Input handling
    for i in range(n):
        if sys.argv[i] == "-l":
            try:
                wordlist_path = sys.argv[i+1]
            except:
                print("[!] No wordlist provided")
                print("[!] Exiting...")
                return

        if sys.argv[i] == "-f":
            try:
                zip_file_path = sys.argv[i+1]
            except:
                print("[!] No ZIP file provided")
                print("[!] Exiting...")
                return
        if sys.argv[i] == "-v":
            verbose = True
        if sys.argv[i] == "-V":
            verbose = True
            more_verbose = True

    if wordlist_path is None:
        print("[!] No wordlist provided")
        print("[!] A path to the wordlist must be provided with the flag -l")
        print("[!] Exiting...")
        return
    if zip_file_path is None:
        print("[!] No ZIP file provided")
        print("[!] A path to the zip file must be provided with the flag -f")
        print("[!] Exiting...")
        return

    password = bruteforce(wordlist_path, zip_file_path, verbose, more_verbose)

    return


def bruteforce(wordlist_path, zip_file_path, verbose, more_verbose):
    # Attempts to find the password for the given zip file with the words in the given wordlist
    if verbose:
        print(f"[*] Attempting to bruteforce {zip_file_path} with {wordlist_path}")
    
    try:
        with open(wordlist_path, "r") as wordlist:
            
            try:
                with zp.ZipFile(zip_file_path, 'r') as zip_file:

                    # Tries to open the zip file without a password
                    try:
                        zip_file.testzip()
                    except:
                        pass
                    else:
                        print(f"[*] File {zip_file_path} isn't password protected")
                        print(f"[*] Exiting...")
                        return None

                    # Shows the files in the zip file if verbose mode is active
                    if more_verbose:
                        files = zip_file.namelist()
                        print(f"[*] Files in {zip_file_path}:")
                        for file in files:
                            print(f"\t[->] {file}")

                    # Initializes password_candidate with the first word from the wordlist
                    password_candidate = wordlist.readline().rstrip("\n")

                    # While there's still words on the wordlist
                    while(password_candidate != ""):
                        # Tries to use the password to open the zip file
                        try:
                            zip_file.setpassword(password_candidate.encode())
                            zip_file.testzip()

                        # If the password is incorrect, a RunTimeError exception is generated when executing testzip()
                        except:
                            if more_verbose:
                                print(f"[^] Password fail: {password_candidate}")

                        # If a password is found, no error emergers from testzip() which indicates we have the correct password
                        else:
                            if verbose:
                                print(f"\n[+] Password found: {password_candidate}\n")
                                print(f"[*] Exiting...")
                            else:
                                print(f"The password is: {password_candidate}")
                            return password_candidate

                        # Reads the next word from the wordlist
                        password_candidate = wordlist.readline().rstrip("\n")
            
            # If there is an error while trying to open the zip file
            except EnvironmentError:
                print(f"[!] Could not open {zip_file_path}")
                return None

    # If there is an error while trying to open the wordlist
    except EnvironmentError:
        print(f"[!] Could not open {wordlist_path}")
        return None

    # If all the words in the wordlist were tested and none where a match
    print(f"[^] Password not found")
    return None


if __name__ == "__main__":
    main()
