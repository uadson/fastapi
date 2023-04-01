from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_passwd(passwd: str, hash_passwd: str) -> bool:
    """
        Function to verify if the password is correct, 
        comparing the password in plain text, informed 
        by the user, and the hash of the password that 
        will be saved in the database during the creation 
        of the account.
    """
    return CRIPTO.verify(passwd, hash_passwd)


def generate_hash_passwd(passwd: str) -> str:
    """
        Function that generates and returns the password hash
    """
    return CRIPTO.hash(passwd)
