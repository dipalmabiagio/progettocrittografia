#imports
from src.FindGenerators import findGenerators
from src.FindKValue import gen_key


# i numeri primi devono necessariamente essere composti di almeno 8 bit: questo
# è necessario al fine di poter cifrare anche le stringhe, si farà uso dello
# stesso numero primo per tutti i cifrari, cambierà solamente il gammaValue
# NB = verra' inizializzati a zero per comodita'
from pip._vendor.distlib.compat import raw_input

q =0

# generatore trovato tramite il modulo "findGenerators.py"
# NB = verra' inizializzati a zero per comodita'
g =0


# il valore della key rappresenta la chiave privata, in tal caso la chiave privata
# sarà unica per tutti gli utenti, l'obiettivo di questa soluzione è quello di
# sfruttare la sicurezza e le performance dei cifrari asimmetrici associandolo
# alla versatilità di quelli simmetrici. L'ABE sarà realizzata attraverso l'uso
# del gammaValue
# NB = verra' inizializzati a zero per comodita'
key = 0

"""
Questo metodo è utile per trasformare le lettere in numeri, entra in gioco
quando si produce il gammaValue
"""
def stringToNumbers(string):
    outputValue = []
    finalValue = 1
    for character in string:
        number = ord(character)
        outputValue.append(number)

    for index in range (1,len(outputValue)-1):
        finalValue = outputValue[index] * finalValue

    return finalValue

"""
Questo metodo genera un valore gamma, utile a cifrare lo stesso messaggio
in modo diverso in base agli attributi inseriti 
"""
def generateGammaValue(username, matricola, secretKey, q):
    intUser = stringToNumbers(username)
    secretKey =  stringToNumbers(secretKey)
    gammaValue = (intUser * matricola * secretKey) % q

    print ('gammaValue: ', gammaValue)
    return gammaValue

"""
Metodo di esponenziazione modulare
"""
def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)

    return x % c

def collectAttributes():

    print ('inserisci i tuoi attributi per la cifratura.')
    username = str(raw_input('username: '))
    matricola = int(raw_input('matricola: '))
    secretKey = str(raw_input('secret key: '))

    return username, matricola, secretKey



"""
Algoritmo di ElGamal di cifratura asimmetrica
@:param msg: plaintext da cifrare
        q = numero primo scelto 
        h = betaValue, valore di Beta dato dal pow(generatore, alfa)
        g = generatore utilizzato
@:return en_msg = array del messaggio cifrato
        p = generatore elevato alla k mod q
"""


def encrypt(msg, h, k, q, g, gammaValue):
    en_msg = []

    s = power(h, k, q)
    p = power(g, k, q)

    for i in range(0, len(msg)):
        en_msg.append(msg[i])

    print("g^k used : ", p)
    print("g^ak used : ", s)
    for i in range(0, len(en_msg)):
        en_msg[i] = (s * ord(en_msg[i])) + gammaValue

    print('messaggio cifrato: ', en_msg)

    return en_msg, p

"""
Algoritmo di ElGamal di decifratura asimmetrica
@:param en_msg: ciphertext da decifrare
        q = numero primo scelto 
        p = generatore elevato alla k mod q
        key = k scelto
@:return dr_msg = array del messaggio decifrato

"""

def decrypt(en_msg, p, key, q, gammaValue):
    dr_msg = []
    h = power(p, key, q)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int((en_msg[i] - gammaValue) / h)))

    return dr_msg

""""
Funzione di main 
"""
def main():
    global q, g, key

    #scelta del numero primo da usare
    q = int(raw_input('inserisci il numero primo che vuoi usare (suggerimento: un numero primo grande è 3613): '))

    print ('il numero primo che hai scelto è {0}'.format(q))
    #raccolta attributi
    username, matricola, secretKey = collectAttributes()
    gammaValue = generateGammaValue(username, matricola, secretKey, q)

    #trovo il generatore
    g = findGenerators(q)

    print ('il generatore trovato è: {0}'.format(g))

    msg = str(raw_input('inserisci il messaggio da cifrare: '))
    print("Messaggio originale :", msg)

    #genero la chiave privata tramite il metodo gen_key
    key = gen_key(q)

    betaValue = power(g, key, q)

    en_msg, p = encrypt(msg, betaValue,key, q, g, gammaValue)
    dr_msg = decrypt(en_msg, p, key, q, gammaValue)
    dmsg = ''.join(dr_msg)
    print("il messaggio cifrato per questo utente è:", dmsg);

    print ("*******************")

    print ("considero gli attributi di un altro utente, usando lo stesso plaintext {0}, lo stesso numero primo {1}, lo stesso generatore {2},"
           "la stessa chiave {3} e lo stesso ciphertext {4}".format(msg, q, g, key, en_msg))
    usr, mat, secKey = collectAttributes()

    gammaV = generateGammaValue(usr, mat, secKey, q)

    dr_msg2 = decrypt(en_msg, p, key, q, gammaV)
    dmsg2 = ''.join(dr_msg2)
    print("il messaggio cifrato per questo utente è:", dmsg2);


if __name__ == '__main__':
    main()
