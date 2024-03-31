import os, time, sys
from cryptography.fernet import Fernet
#from multiprocessing import Pool

PROGNAME = 'Cryplock'
VERSION = '1.0_beta'

def showhelp():
    print ("Help for "+PROGNAME+":")
    print ("-encrypt    : Use this option for encryption.")
    print ("-decrypt    : Use this option for decryption. -key=<keyfile> must be specified if using -decrypt.")
    print ("-target     : Specify the directory path, files of which will be encrypted/decrypted. Directory path must be absolute.")
    print ("-key        : Specify the key file when using the -decrypt option. File path must be absolute.")
    print ("-help       : Show this help menu.")

print (PROGNAME+" "+VERSION+"\n")
print (PROGNAME+" is a command line encryption/decryption utility.")
print ("Copyright (c) Arijit Kumar Das (Github: @ArijitKD).")
print ("By using this software, you agree to the terms of the MIT License.\n")
    
KEY_FILE = ""
TASK = ""
if (len(sys.argv) == 1):
    print ("No options specified. Use -help to see the list of available options.")
    raise SystemExit
for arg in sys.argv[1::]:
    if (arg.lower().startswith('-encrypt')):
        TASK='encrypt'
    elif (arg.lower().startswith('-decrypt')):
        TASK='decrypt'
    elif (arg.lower().startswith('-target')):
        TARGET_DIR = arg+"/" if not arg.endswith('/') else arg
        if (TARGET_DIR.find("=") == -1 or arg=="-target="):
            print ("Error: Target directory path not specified in -target option.")
            raise SystemExit
        TARGET_DIR = TARGET_DIR[TARGET_DIR.index('=')+1::].strip().strip("\"").strip("\'").strip()
        if (not os.path.isdir(TARGET_DIR)):
            print ("Error: Target directory path specified either does not exist or is not absolute.")
            raise SystemExit
    elif (arg.lower().startswith('-key')):
        KEY_FILE = arg
        if (KEY_FILE.find("=") == -1 or arg=="-key="):
            print ("Error: Key file path not specified in -key option.")
            raise SystemExit
        KEY_FILE = KEY_FILE[KEY_FILE.index('=')+1::].strip().strip("\"").strip("\'").strip()
        if (not os.path.isfile(KEY_FILE)):
            print ("Error: Key file path specified either does not exist or is not absolute.")
            raise SystemExit
    elif (arg.lower().startswith("-help")):
        showhelp()
        raise SystemExit
    else:
        print ("Unknown option: '"+arg+"'. Use -help to see the list of available options.")
        raise SystemExit
        
target_files = []
for file in os.listdir(TARGET_DIR):
    if (os.path.isfile(TARGET_DIR+file)):
        target_files.append(TARGET_DIR+file)
encrypted_id = PROGNAME.encode()+b"encrypted"

'''
def _crypt_chunk(data_chunk, key, crypted_data_packets, insert_index):
    newdata = b''
    k=i=0
    while (i<len(data_chunk)):
        changed_byte = 0
        bitlist = list(bin(data_chunk[i])[2::])
        bitlist = ['0']*(8-len(bitlist))+bitlist
        if (k==0):
            k=key
        for j in range(7,-1,-1):
            l = k%10
            k = k//10
            if (l%2==0):
                if (bitlist[j] == '0'):
                    bitlist[j] = '1'
                else:
                    bitlist[j] = '0'
            changed_byte += (2**(7-j))*int(bitlist[j])
        newdata += int.to_bytes(changed_byte, byteorder=byteorder)
        i+=1
        crypted_data_packets[insert_index] = newdata   

def _packetify_data(data, chunk_size):
    data_packets = []
    number_of_chunks = len(data)//chunk_size if len(data)%chunk_size == 0 else len(data)//chunk_size+1
    for i in range(number_of_chunks):
        data_packets.append(data[i*chunk_size : (i+1)*chunk_size])
    return data_packets


def cryptdata(data, key, chunk_size, job):
    f = Fernet(key)
    data_packets = _packetify_data(data, chunk_size)
    print (data_packets)
    crypted_data = b''  
    if (job.lower() == 'decrypt'):
        with Pool(len(data_packets)) as p:
            crypted_data_packets = p.map(f.decrypt, data_packets)
    else: 
        with Pool(len(data_packets)) as p:
            crypted_data_packets = p.map(f.decrypt, data_packets)
    for crypted_data_packet in crypted_data_packets:
        crypted_data += crypted_data_packet
    return crypted_data

'''

def cryptdata(data, key, job):
    f = Fernet(key)
    if (job.lower() == 'decrypt'):
        crypted_data = f.decrypt(data)
    else: 
        crypted_data = f.encrypt(data)
    return crypted_data

if (TASK == "encrypt"):
    show_keywrite_msg = False
    keyfile_specified = False
    if (KEY_FILE == ""):
        KEY = Fernet.generate_key()
        KEY_FILE = os.getcwd()+"/key"+str(int(time.time()))
        with open(KEY_FILE, 'wb') as keyfile:
            keyfile.write(KEY)
            show_keywrite_msg = True
    else:
        keyfile_specified = True
        with open(KEY_FILE, 'rb') as keyfile:
            KEY = keyfile.read()
        try:
            f = Fernet(KEY)
            data = b"This is a test code"
            encrypted = f.encrypt(data)
            decrypted = f.decrypt(encrypted)
            if (data != decrypted):
                raise Exception
        except:
            print ("Error: Invalid key provided.")
            print ("Generate new key for encryption? [Y/N]: ", end="")
            choice = (input().strip())[0].upper()
            if (choice == 'Y'):
                KEY = Fernet.generate_key()
                KEY_FILE = os.getcwd()+"/key"+str(int(time.time()))
                with open(KEY_FILE, 'wb') as keyfile:
                    keyfile.write(KEY)
                    show_keywrite_msg = True
            else:
                print ("Aborted.")
                raise SystemExit
    skipped_files = {'Large file size': [], 'Already encrypted': []}
    init_time = time.time()
    for file in target_files:
        if (os.path.getsize(file)>1.074e+9):
            print ("Error: Skipping operation on", file, "because it is too large (>1GB).")
            skipped_files['Large file size'].append(file)
            continue
        starttime = time.time()
        encrypt_filename = False
        with open(file, 'r+b') as current_file:
            current_file.seek(0)
            if (current_file.read(len(encrypted_id)) == encrypted_id):
                print (file,"has already been encrypted by", PROGNAME+".")
                skipped_files["Already encrypted"].append(file)
            else:
                current_file.seek(0)
                try:
                    encrypted_data = cryptdata(current_file.read(), KEY, "encrypt")
                except:
                    print ("Error while encrypting file: "+file+". Key is probably incorrect or invalid.\nAborted.")
                    raise SystemExit
                current_file.seek(0)
                current_file.write(encrypted_id)
                current_file.write(encrypted_data)
                encrypt_filename = True
                print ("Operation successful on:", file, "(ETA:", round(time.time()-starttime, 2), "seconds)")
        if (encrypt_filename):
            actual_filename = file[file.rindex('/')+1::]
            directory = file[0:file.rindex('/')+1]
            os.rename(file, directory+cryptdata(actual_filename.encode(), KEY, "encrypt").decode())
    print ()
    if (len(skipped_files["Large file size"])>0):
        print ("The following files could not be encrypted due to large file size (>1GB):")
        for file in skipped_files["Large file size"]:
            print ("*\t"+file)
        print ("Large file encryption/decryption ability will be implemented soon, stay tuned.\n")
    if (len(skipped_files["Already encrypted"])>0):
        print ("The following files could not be encrypted these were already encrypted previously using %s:"%(PROGNAME,))
        for file in skipped_files["Already encrypted"]:
            print ("*\t"+file)
        print ()
    if (len(skipped_files["Large file size"]) == len(skipped_files["Already encrypted"]) == 0):
        print ("All files have been successfully encrypted. (ETA: %0.2f seconds)."%(time.time()-init_time,))
    else:
        operated_file_count = len(target_files)-len(skipped_files["Already encrypted"])-len(skipped_files["Large file size"])
        if (operated_file_count == 0):
            if (not keyfile_specified): 
                os.remove(KEY_FILE)
                show_keywrite_msg = False
            print ("No files were encrypted.")
        else:
            print (str(operated_file_count)+" out of "+str(len(target_files))+" files were successfully encrypted (ETA: %0.2f seconds)."%(time.time()-init_time,))
    if (show_keywrite_msg):
        print ("Key file has been generated at", KEY_FILE+" and is required for future decryption. Keep it safely.")
elif (TASK == "decrypt"):
    if (KEY_FILE == ""):
        print ("Key file not specified for decryption. Use -keyfile=<keyfilepath> to specify the key file.")
        raise SystemExit
    else:
        with open(KEY_FILE, 'rb') as keyfile:
            KEY = keyfile.read()
        try:
            f = Fernet(KEY)
            data = b"This is a test code"
            encrypted = f.encrypt(data)
            decrypted = f.decrypt(encrypted)
            if (data != decrypted):
                raise Exception
        except:
            print ("Error: Invalid key provided.\nAborted.")
    skipped_files = {'Large file size': [], 'Not encrypted': []}
    init_time = time.time()
    for file in target_files:
        if (os.path.getsize(file)>1.074e+9):
            print ("Error: Aborted operation on", file, "because it is too large (>1GB).")
            skipped_files["Large file size"].append(file)
            continue
        starttime = time.time()
        decrypt_filename = False
        with open(file, 'r+b') as current_file:
            current_file.seek(0)
            if (current_file.read(len(encrypted_id)) == encrypted_id):
                try:
                    decrypted_data = cryptdata(current_file.read(), KEY, "decrypt")
                except:
                    print ("Error while decrypting file: "+file+". Key is probably incorrect or invalid.\nAborted.")
                    raise SystemExit
                with open(file, 'w') as clearfile:
                    pass
                current_file.seek(0)
                current_file.write(decrypted_data)
                decrypt_filename = True
                print ("Operation successful on:", file, "(ETA:", round(time.time()-starttime, 2), "seconds)")
            else:
                print (TARGET_DIR+file,"has not yet been encrypted by", PROGNAME+". Decryption not possible.")
                skipped_files["Not encrypted"].append(file)
            if (decrypt_filename):
                actual_filename = file[file.rindex('/')+1::]
                directory = file[0:file.rindex('/')+1]
                os.rename(file, directory+cryptdata(actual_filename.encode(), KEY, "decrypt").decode())
    print ()
    if (len(skipped_files["Large file size"])>0):
        print ("The following files could not be decrypted due to large file size (>1GB):")
        for file in skipped_files["Large file size"]:
            print ("*\t"+file)
        print ("These files were probably not encrypted before due to "+PROGNAME+"\'s limitations.")
        print ("Large file encryption/decryption ability will be implemented soon, stay tuned.\n")
    if (len(skipped_files["Not encrypted"])>0):
        print ("The following files could not be decrypted because these were not encrypted previously using %s:"%(PROGNAME,))
        for file in skipped_files["Not encrypted"]:
            print ("*\t"+file)
        print ()
    if (len(skipped_files["Large file size"]) == len(skipped_files["Not encrypted"]) == 0):
        print ("All files have been successfully decrypted (ETA: %0.2f seconds)."%(time.time()-init_time,))
    else:
        operated_file_count = len(target_files)-len(skipped_files["Not encrypted"])-len(skipped_files["Large file size"])
        if (operated_file_count == 0):
            print ("No files were decrypted.")
        else:
            print (str(operated_file_count)+" out of "+str(len(target_files))+" files were successfully decrypted (ETA: %0.2f seconds)."%(time.time()-init_time,))
else:
    if (TASK == ""):
        print ("Please specify an option: -encrypt or -decrypt.")
    else:
        print ("Unknown task: \""+TASK+"\".")
