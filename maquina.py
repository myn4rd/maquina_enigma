import os 
from dotenv import load_dotenv 

load_dotenv()

alfabeto_global=os.getenv("ALFABETO_EN")
alfabeto_type="EN"
diccionario_frac="EN"

def menu():
    opc = 0
    print("===SELECTOR===")
    print("1) Crypt Word")
    print("2) Decrypt Word")
    print("3) Exit")
    opc = int(input("Select Option: "))
    if opc == 1:
        crypt_word()
    elif opc == 2:
        decrypt_word()
    else:
        os._exit(1)


def load_rotors(rotor_opc):
    alfabeto = alfabeto_global
    rotor_I = os.getenv(f"ROTOR_I_{alfabeto_type}")
    rotor_II = os.getenv(f"ROTOR_II_{alfabeto_type}")
    rotor_III = os.getenv(f"ROTOR_III_{alfabeto_type}")
    reflector = os.getenv(f"REFLECTOR_{alfabeto_type}")

    if rotor_opc == 1: 
        return rotor_I 
    elif rotor_opc == 2:
        return rotor_II 
    elif rotor_opc == 3:
        return rotor_III
    elif rotor_opc == "alfabeto":
        return alfabeto
    elif rotor_opc == "reflector":
        return reflector
       
def map_key(rotor_opc, char_key):
    rotor = load_rotors(rotor_opc)
    print(f"Rotor {rotor_opc} cargado...")
    print(f"Buscando valor de {char_key} en rotor {rotor_opc}")
    obj = char_key.upper()
    for index, char_key_upper in enumerate(rotor): 
        if char_key_upper == obj:
            print(f"{char_key} tiene la posicion de {index}")
            return index



def map_char(rotor_opc, char):
    rotor = load_rotors(rotor_opc)
    print(f"Rotor {rotor_opc} cargado...")
    print(f"Buscando valor de {char} en rotor {rotor_opc}")
    obj = char.upper()
    for index, char_upper in enumerate(rotor): 
        if char_upper == obj:
            char_pos = index
            print(f"{char} tiene la posicion de {char_pos}")
            return char_pos

def find_char(rotor_opc, index):
    global alfabeto_global
    rotor = load_rotors(rotor_opc)
    print(f"Rotor {rotor_opc} cargado...")
    print(f"Buscando el valor de la posicion {index} en rotor {rotor_opc}")
    index_seguro = index % len(alfabeto_global) 
    value = rotor[index_seguro]
    return value 
    
def compare_value_notch(value_char, notch_value, key_pos):
    global alfabeto_type
    if value_char != notch_value: 
        return key_pos
    else: 
        key_pos = (key_pos + 1) % len(alfabeto_global)
        print(f"VALOR DEL KEY {value_char} MODIFICADO A {key_pos}")
        return key_pos

def main_cipher_logic(word, key):
    global alfabeto_global
    print(len(alfabeto_global))
    palabra_cifrada = [0] * len(word)
    print(f"Mapeando key {key} en alfabeto")
    key_positions = [0] * len(key)
    for i, char_key in enumerate(key):
        char_key_pos = map_key("alfabeto", char_key)
        key_positions[i] = char_key_pos
    

    for i, char in enumerate(word):
        if char == " ":
            palabra_cifrada[i] = char
            continue 

        char_pos = map_char("alfabeto", char)
        x = ((char_pos + key_positions[0]) % len(alfabeto_global))
        value_char = find_char(1, x) 
        key_positions[0] = compare_value_notch(value_char, "Q", key_positions[0])
        
        x = ((map_char("alfabeto", value_char) + key_positions[1]) % len(alfabeto_global))
        value_char = find_char(2, x)
        key_positions[1] = compare_value_notch(value_char, "E", key_positions[1])
        
        x = ((map_char("alfabeto", value_char) + key_positions[2]) % len(alfabeto_global) )
        value_char = find_char(3, x)
        key_positions[2] = compare_value_notch(value_char, "V", key_positions[2])
        
        index = map_char("alfabeto", value_char)
        char_from_reflector = find_char("reflector", index)

        x = map_char(3, char_from_reflector)
        key_positions[2] = compare_value_notch(value_char, "V", key_positions[2])
        x = (((x) - key_positions[2]) % len(alfabeto_global))

        value_char = find_char("alfabeto", x)
        x = map_char(2, value_char)
        key_positions[1] = compare_value_notch(value_char, "E", key_positions[1])
        x = ((x) - key_positions[1]) % len(alfabeto_global)

        value_char = find_char("alfabeto", x)
        x = map_char(1, value_char)
        key_positions[0] = compare_value_notch(value_char, "Q", key_positions[0])
        final = (((x) - key_positions[0]) % len(alfabeto_global))

        char_cipher=find_char("alfabeto", final)
        
        print(f"Letra {char}\nCifrado {char_cipher}")

        palabra_cifrada[i] = char_cipher

    return "".join(palabra_cifrada)

def load_abc(abc):
    global alfabeto_global
    if abc.upper() == "ES":
        alfabeto_global = os.getenv("ALFABETO_ES")
    elif abc.upper() == "EN": 
        alfabeto_global = os.getenv("ALFABETO_EN")


def load_abc_type(abc):
    global alfabeto_type
    global diccionario_frac
    diccionario_frac = f"frac_{abc}"
    alfabeto_type = abc.upper() 


def crypt_word():
    abc=input("Select lenguage (es/en): ")
    if abc == "es": 
        load_abc(abc)
    elif abc == "en":
        load_abc(abc)
    else:
        print('PLEASE SELECT "US" FOR ENGLISH OR "ES" FOR SPANISH')
        os._exit(1)
    load_abc_type(abc)
    word=input("Word to crypt: ")
    key=input("Key Word (the key length must be 3 letters): ").replace(" ","")
    if len(key) != 3:
        print("THE KEY LENGHT MUST BE 3 LETTERS")
        os._exit(1) 
    crypted_word=main_cipher_logic(word, key)
    print(f"Word in plain text: {word}")
    print(f"Crypted word: {crypted_word}")

def main_decrypt_logic(word, key):
    global alfabeto_global
    n_alfabeto = len(alfabeto_global)
    
    key_positions = [0] * len(key)
    for i, char_key in enumerate(key):
        key_positions[i] = map_key("alfabeto", char_key)

    caminos_validos = []

    def explorar_rama(idx_letra, estado_actual, palabra_acumulada):
        if idx_letra == len(word):
            caminos_validos.append(palabra_acumulada)
            return

        char_cipher = word[idx_letra]
        if char_cipher == " ":
            explorar_rama(idx_letra + 1, estado_actual, palabra_acumulada + " ")
            return 

        for intento_idx in range(n_alfabeto):
            temp_k0, temp_k1, temp_k2 = estado_actual
            char_intento = find_char("alfabeto", intento_idx)
            
            x = ((intento_idx + temp_k0) % n_alfabeto)
            v1 = find_char(1, x)
            temp_k0 = compare_value_notch(v1, "Q", temp_k0)
            
            x = ((map_char("alfabeto", v1) + temp_k1) % n_alfabeto)
            v2 = find_char(2, x)
            temp_k1 = compare_value_notch(v2, "E", temp_k1)
            
            x = ((map_char("alfabeto", v2) + temp_k2) % n_alfabeto )
            v3 = find_char(3, x)
            temp_k2 = compare_value_notch(v3, "V", temp_k2)
            
            index = map_char("alfabeto", v3)
            char_from_reflector = find_char("reflector", index)

            x = map_char(3, char_from_reflector)
            temp_k2 = compare_value_notch(v3, "V", temp_k2)
            x = (((x) - temp_k2) % n_alfabeto)

            value_char_regreso = find_char("alfabeto", x)
            x = map_char(2, value_char_regreso)
            temp_k1 = compare_value_notch(value_char_regreso, "E", temp_k1)
            x = ((x) - temp_k1) % n_alfabeto

            value_char_regreso2 = find_char("alfabeto", x)
            x = map_char(1, value_char_regreso2)
            temp_k0 = compare_value_notch(value_char_regreso2, "Q", temp_k0)
            final = (((x) - temp_k0) % n_alfabeto)

            char_cifrado_prueba = find_char("alfabeto", final)
            
            if char_cifrado_prueba == char_cipher:
                explorar_rama(idx_letra + 1, [temp_k0, temp_k1, temp_k2], palabra_acumulada + char_intento)

    explorar_rama(0, key_positions, "")


    
    frec_EN = {
        'E':.127, 'T':.091, 'A':.082, 'O':.075, 'I':.070, 'N':.067, 'S':.063, 'H':.061,
        'R':.060, 'D':.043, 'L':.040, 'C':.028, 'U':.028, 'M':.024, 'W':.024, 'F':.022,
        'G':.020, 'Y':.020, 'P':.019, 'B':.015, 'V':.010, 'K':.008, 'J':.002, 'X':.002,
        'Q':.001, 'Z':.001
    }
    frec_ES = {
        'E': .1368, 'A': .1253, 'O': .0868, 'S': .0798, 'R': .0687, 'N': .0671,
        'I': .0625, 'D': .0586, 'L': .0497, 'C': .0468, 'T': .0463, 'U': .0393,
        'M': .0315, 'P': .0251, 'B': .0142, 'G': .0101, 'V': .0090, 'Y': .0090,
        'Q': .0088, 'H': .0070, 'F': .0069, 'Z': .0052, 'J': .0044, 'Ñ': .0031,
        'X': .0022, 'K': .0002, 'W': .0001
    }

    global alfabeto_type
    diccionario_frec = frec_ES if alfabeto_type == "ES" else frec_EN
    
    mejor_palabra = max(caminos_validos, key=lambda s: sum(diccionario_frec.get(c, 0.001) for c in s))
    
    return mejor_palabra

def decrypt_word():
    abc = input("Select language (es/en): ")
    if abc.lower() == "es": 
        load_abc(abc)
    elif abc.lower() == "en":
        load_abc(abc)
    else:
        print('PLEASE SELECT "EN" FOR ENGLISH OR "ES" FOR SPANISH')
        os._exit(1)
        
    load_abc_type(abc)
    
    word = input("Word to decrypt: ")
    key = input("Key Word (the key length must be 3 letters): ")
    if len(key) != 3:
        print("THE KEY LENGTH MUST BE 3 LETTERS")
        os._exit(1) 
        
    decrypted_word = main_decrypt_logic(word, key)
    
    print(f"Crypted text input: {word}")
    print(f"Decrypted word: {decrypted_word}")




## main 

menu()

