lst = ["Nume / Last Name: Doe | Prenume / First Name: Jane | E-mail: oprisaalin@gmail.com | Numar Telefon / Phone Number: 0123456789 | Data Nasterii / Date of Birth: 11-02-1992 | Adresa / Address: asdfqwer | Localitate / City: Test | Judet / County: ASD | Tara / Country: Romania | Sex: F | Marime Tricou / T-SHIRT SIZE: Small | Paste cu Branza (vineri) / Mac &#039;n Cheese (Friday): Da | Gulyas (sambata) / Gulyas (Saturday): Da | Sandwich (vineri si sambata) / Sandwiches (Friday, Saturday ): Da-carne | : Da",
       "Nume / Last Name: Does | Prenume / First Name: John | E-mail: oprisaalin@gmail.com | Numar Telefon / Phone Number: 9876546321 | Data Nasterii / Date of Birth: 22-02-1990 | Adresa / Address: asdfqwerqwer | Localitate / City: qqqeqw | Judet / County: zzxcv | Tara / Country: fghgyje | Sex: M | Marime Tricou / T-SHIRT SIZE: Large | Paste cu Branza (vineri) / Mac &#039;n Cheese (Friday): Da | Gulyas (sambata) / Gulyas (Saturday): Da | Sandwich (vineri si sambata) / Sandwiches (Friday, Saturday ): Da-veg | : Da",
       "Nume / Last Name: Oprisa | Prenume / First Name: Alin | E-mail: oprisaalin@gmail.com | Numar Telefon / Phone Number: 0733726843 | Data Nasterii / Date of Birth: 17-01-1992 | Adresa / Address: str. Unirii 57 E | Localitate / City: Aiud | Judet / County: Alba | Tara / Country: Romania | Sex: M | Marime Tricou / T-SHIRT SIZE: Large | Paste cu Branza (vineri) / Mac &#039;n Cheese (Friday): Da | Gulyas (sambata) / Gulyas (Saturday): Da | Sandwich (vineri si sambata) / Sandwiches (Friday, Saturday ): Da-veg | : Da"]

new = []

for i in lst:
    temp = []
    for j in i.split("|"):
        for k in j.split(":"):
            temp.append(k.strip())
    new.append(temp)

test = []
for i in new:
    temp2 = []
    for j in range(1, len(i), 2):
        temp2.append(i[j])
    test.append(temp2)


dct = {"Nume": "", "Prenume": "", "E-mail": "", "Telefon": "", "Data Nasterii": "",
       "Adresa": "", "Localitate": "", "Judet": "", "Tara": "",
       "Sex": "","Tricou": "",
       "Paste cu Branza": "", "Gulyas": "", "Sandwich": "",
       "Acord Reg": ""}

for i in test:
    dct["Nume"] += i[0] + " "
    dct["Prenume"] += i[1] + " "
    dct["E-mail"] += i[2] + " "
    dct["Telefon"] += i[3] + " "
    dct["Data Nasterii"] += i[4] + " "
    dct["Adresa"] += i[5] + " "
    dct["Localitate"] += i[6] + " "
    dct["Judet"] += i[7] + " "
    dct["Tara"] += i[8] + " "
    dct["Paste cu Branza"] += i[9] + " "
    dct["Gulyas"] += i[10] + " "
    dct["Paste cu Branza"] += i[11] + " "
    dct["Sandwich"] += i[12] + " "
    dct["Acord Reg"] += i[13] + " "

print(dct)

