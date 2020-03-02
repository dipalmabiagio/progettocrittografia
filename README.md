# Attribute Based Encryption (ABE)

## El Gamal con ABE 
Questo progetto, sviluppato e ideato in un ambiente accademico, propone una soluzione di cifratura basata sugli attributi.
In questo caso gli attributi richiesti all'utente sono:
* Matricola [si suppone essere in un contesto aziendale dove ogni dipendente ha la sua matricola]
* Username
* SecretKey [una sorta di password, nota solo all'utente in questione]

Gli ultimi due paramtri, trattati come delle stringhe, vengono trasformati in numeri dal metodo _stringToNumbers_:
    
    def stringToNumbers(string):
    outputValue = []
    finalValue = 1
    for character in string:
        number = ord(character)
        outputValue.append(number)
    for index in range (1,len(outputValue)-1):
        finalValue = outputValue[index] * finalValue

    return finalValue
    
Questo metodo viene invocato dalla funzione _generateGammaValue_ che genera un unico valore (il GammaValue) da utilizzare nella cifratura partendo proprio dagli attributi dell'utente.
    
    def generateGammaValue(username, matricola, secretKey, q):
    intUser = stringToNumbers(username)
    secretKey =  stringToNumbers(secretKey)
    gammaValue = (intUser * matricola * secretKey) % q

    print ('gammaValue: ', gammaValue)
    return gammaValue
    
Infine il Gammavalue viene sommato semplicemente al valore cifrato di ogni lettera:
        
    for i in range(0, len(en_msg)):
    en_msg[i] = (s * ord(en_msg[i])) + gammaValue
        
## El Gamal Classico
Questo modulo rappresenta una implementazione classica dell'algoritmo di El Gamal, è stato utile come punto di partenza per l'espansione dello stesso con ABE.

## Documentazione completa
Una documentazione più completa è disponibile a questo [link](https://github.com/dipalmabiagio/progettocrittografia/blob/master/doc/ElGamal%20con%20ABE.pdf).

## Contributors
* [Biagio Dipalma](https://www.linkedin.com/in/biagio-dipalma/) - Università degli Studi di Milano | La Statale. CDL Magistrale in Sicurezza Informatica.
* [Sara Longo](https://www.linkedin.com/in/sara-longo-2b2830187/) - Università degli Studi di Milano | La Statale. CDL Magistrale in Sicurezza Informatica.


