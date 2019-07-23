from hashlib import md5

def hash_receiver(xml):
    try:
        file_name = xml
        hasher = md5()

        with open(file_name, 'rb') as f:
                hasher.update(f.read())

        f_hash = hasher.hexdigest()
        return f_hash
    except FileNotFoundError:
            print('Could not get hash. The specified file is missing.')
            return None
                
