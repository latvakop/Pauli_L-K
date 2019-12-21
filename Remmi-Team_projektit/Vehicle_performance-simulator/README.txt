Ohjelman tarkoituksena on simuloida Remmi-teamin ajokin ajoa pohjautuen csv-dataan joka ajokilla on mitattu ennemmin.  
Ohjelmassa lasketaan monia erilaisia asioita auton toiminnasta kuten: nopeus, sijainti radalla, korkeus radalla, kitkan 
aiheuttama energiahäviö, aika, bensan kulutus yms. ja lopuksi lasketaan auton suorituskyky yksikössä km/l ja voidaan piirtää erilaisia kuvaajia datasta. 
Remmi-teamin jäsen Jesper Granat on myös lisännyt ohjelmaan optimointi algoritmin jolla voidaan hakea parasta mahdollista kiihdytyksen alku- 
ja loppunopeutta bensankulutuksen minimoimiseksi. Alkuperäinen ohjelma on toteutettu Matlabilla ja se on lähes kokonaan
muiden remmi-tiimin jäsenten tekemä, omaa koodiani tässä alkuperäisessä ohjelmassa oli hyvin vähän. Olemme yhteityössä
Jesper Granatin kanssa yrittäneet refactoroida tätä konemiesten koodia pythonille ja lisänneet siihen uutena kiihdytysnopeuksien
optimoinnin. Sanoisin että noin puolet refactoroinnista on tehnyt Jesper Granat, puolet minä, mutta tarkempi selvitys koodin
tekijästä ja alkuperästä lukee koodissa. 

Ohjelma on tehty pythonilla ja sen voi ajaa Pycharmilla tai Visual Studio Codella, tarvittavat kirjastot löytyvät requirements.txt tiedostosta. 
