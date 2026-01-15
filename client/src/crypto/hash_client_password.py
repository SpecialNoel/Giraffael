# hash_client_password.py
# Utilizes Argon2 library to hash client password on client side (thus achieving E2EE)

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# An instance of the reusable argon2 password hasher
ph = PasswordHasher()

# Returns hashed password if success; raises an exception and returns None otherwise
# The format of the hashed password is: '$argon2id$v=...$m=...,t=...,p=...$salt_base64$hash_base64'
'''
    $argon2id$: Specifies the Argon2 variant (Argon2id is the recommended hybrid).
    v=...: The version number.
    m=...,t=...,p=...: The memory cost, time cost (iterations), and parallelism parameters.
    $salt_base64: The unique, randomly generated salt.
    $hash_base64: The actual password hash. 
'''
# This complete encoded string is the only thing needed
def hash_password(password: str):
    try: 
        hashed_password = ph.hash(password=password)
        return hashed_password
    except Exception as e:
        print(f'Error in hash_password(): {e}')
        return None

# Returns True if password matches the hashed password; 
#   raises an exception and returns False otherwise
def verify_password_with_hashed_password(password: str, hashed_password: str):
    try: 
        ph.verify(hash=hashed_password, password=password)
        print('Password matches with hashed password')
        return True
    except VerifyMismatchError:
        print('Password does not match with hashed password')
        return False
    except Exception as e:
        print(f'Error in verify_password_with_hashed_password(): {e}')
        return False

# Returns a new hashed password if parameters are outdated;
#   returns the same hashed password otherwise
def rehash_if_required(password: str, hashed_password: str):
    if ph.check_needs_rehash(hash=hashed_password):
        print('Parameters are outdated; rehashing with new parameters')
        new_hashed_password = ph.hash(password=password)
        return new_hashed_password
    else:
        print('Parameters are current; no rehash required')
        return hashed_password
    