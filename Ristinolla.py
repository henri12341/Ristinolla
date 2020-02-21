"""
Ohjelmassa on toteutettu ristinollapeli. Tarkoitus on saada kolme omaa merkkiä
pystyyn, vinottain tai samalle riville. Peli on 3x3 kokoisessa ruudukossa, joka
on tallennettu self.__peliruudukkoon nappeina. Nappeja painamalla voi laittaa
pelaajan X tai O merkin ruutuun. Vuoro vaihtuu automaattisesti. Peli tarkistaa,
että uutta merkkiä ei laiteta jo pelatulle ruudulle eikä pelin päättymisen
jälkeen voida tehdä uusia siirtoja.

self.__vuorotekstissä ilmoitetaan vuorossa olevan pelaajan merkki ja pelin
päättymisen ilmoittaminen. Self.__pistetilanteessa on ilmoitettu kummankin
pelaajan voitot ja tasapelit. Pelin voi aloittaa uudestaan uusi peli -
painnikkeesta pelin päätyttyä ja ohjelma voidaan sulkea self.__lopeta_nappaimella.
Uuden pelin voi aloittaa vain, jos edellinen peli on päättynyt. Aloittava pelaaja
vaihtuu, kun aloitetaan uusi peli.
"""

from tkinter import *

class Kayttoliittyma():
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Ristinolla")
        self.__pelatut_vuorot = 0
        self.__merkki = "X"
        self.__peli_paattynyt = False
        self.__pelaajan_X_voitot = 0
        self.__pelaajan_O_voitot = 0
        self.__tasapelit = 0
        self.__pelatut_pelit = 0

        self.__vuoroteksti = Label(self.__window, text="Pelaajan {:s} vuoro".format(self.__merkki), borderwidth=3)
        self.__vuoroteksti.grid(row=0, column=0, columnspan=3)

        self.__uusi_peli_nappain = Button(self.__window, text="Uusi peli", command=self.aloita_uusi_peli, borderwidth=3, state=DISABLED)
        self.__uusi_peli_nappain.grid(row=6, column=0, sticky=W, columnspan = 3)

        self.__lopeta_nappain = Button(self.__window, text="Lopeta", command=self.__window.destroy, borderwidth=3)
        self.__lopeta_nappain.grid(row=7, column=0, sticky=W, columnspan = 3)

        self.__pistetilanne = Label(self.__window, text="Pelaaja X voitot: {:d}, Pelaaja O voitot: {:d}, Tasapelit: {:d}".format(self.__pelaajan_X_voitot, self.__pelaajan_O_voitot, self.__tasapelit))
        self.__pistetilanne.grid(row = 5, column = 0, sticky=W, columnspan = 3)

        self.__peliruudukko = []
        for y in range(0, 3):
            napit = []
            for x in range(0, 3):
                nappi = Button(self.__window, text=" ", command= lambda x=x, y=y : self.lisaa_siirto(x, y))
                nappi.grid(row=y+1, column=x, sticky=W + E)
                nappi.configure(height=3, width=3)
                napit.append(nappi)
            self.__peliruudukko.append(napit)

        self.__window.mainloop()

    def aloita_uusi_peli(self):
        """
        Uuden pelin aloittaminen self.__uusi_peli - napista.
        :return:
        """
        self.__pelatut_vuorot = 0

        # Vaihtaa aloittavan pelaajan.
        if self.__pelatut_pelit % 2 == 0:
            self.__merkki = "X"
        else:
            self.__merkki = "O"

        self.__peli_paattynyt = False
        self.__vuoroteksti.configure(text="Pelaajan {:s} vuoro".format(self.__merkki))
        for y in range(0,3):
            for x in range(0,3):
                self.__peliruudukko[y][x].configure(text=" ", state=ACTIVE)
        self.__uusi_peli_nappain.configure(state=DISABLED)

    def lisaa_siirto(self, x, y):
        """
        self.__peliruudukon nappainta klikatessa tapahtuva toiminta.
        :param x:
        :param y:
        :return:
        """
        nappi = self.__peliruudukko[y][x]
        if nappi.cget("text") == " ":
            if self.__merkki == "X":
                nappi.configure(text="X")
            else:
                nappi.configure(text="O")
            self.__pelatut_vuorot += 1
            self.tarkista_voittaako_siirto(x, y)
            if self.__peli_paattynyt == False:
                self.vaihda_merkki()


    def vaihda_merkki(self):
        """
        Vaihtaa merkin X -> O tai toisinpäin. Päivittää self.__vuorotekstin.
        :return:
        """
        if self.__merkki == "X":
            self.__merkki = "O"
        else:
            self.__merkki = "X"
        self.__vuoroteksti.configure(text="Pelaajan {:s} vuoro".format(self.__merkki))


    def tarkista_voittaako_siirto(self, x, y):
        """
        Tarkistaa päättääkö tehty siirtopelin ja päivittää tietoja, jos peli
        päättyy.
        :param x:
        :param y:
        :return:
        """
        voittaako = False
        if self.__peliruudukko[0][0].cget("text") == self.__peliruudukko[1][1].cget("text") == self.__peliruudukko[2][2].cget("text") and self.__peliruudukko[0][0].cget("text") != " ":
            voittaako = True
        if self.__peliruudukko[2][0].cget("text") == self.__peliruudukko[1][1].cget("text") == self.__peliruudukko[0][2].cget("text") and self.__peliruudukko[1][1].cget("text") != " ":
            voittaako = True
        if self.__peliruudukko[0][x].cget("text") == self.__peliruudukko[1][x].cget("text") == self.__peliruudukko[2][x].cget("text") and self.__peliruudukko[0][x].cget("text") != " ":
            voittaako = True
        if self.__peliruudukko[y][0].cget("text") == self.__peliruudukko[y][1].cget("text") == self.__peliruudukko[y][2].cget("text") and self.__peliruudukko[y][0].cget("text") != " ":
            voittaako = True

        # Jos siirto voittaa
        if voittaako == True:
            for y in range(0, 3):
                for x in range(0, 3):
                    nappi = self.__peliruudukko[y][x]
                    nappi.configure(state=DISABLED)
            self.__vuoroteksti.configure(text="Pelaaja {:s} voittaa!".format(self.__merkki))
            self.__peli_paattynyt = True
            if self.__merkki == "X":
                self.__pelaajan_X_voitot += 1
            else:
                self.__pelaajan_O_voitot += 1
            self.paivita_pistetilanne()
            self.__pelatut_pelit += 1
            self.__uusi_peli_nappain.configure(state=ACTIVE)

        # Tasapeli, jos peliruudukko on täynnä siirron jälkeen eikä viimeinen siirto voita.
        elif self.__pelatut_vuorot >= 9:
            for y in range(0, 3):
                for x in range(0, 3):
                    nappi = self.__peliruudukko[y][x]
                    nappi.configure(state=DISABLED)
            self.__vuoroteksti.configure(text="Tasapeli!")
            self.__peli_paattynyt = True
            self.__tasapelit += 1
            self.paivita_pistetilanne()
            self.__pelatut_pelit += 1
            self.__uusi_peli_nappain.configure(state=ACTIVE)

    def paivita_pistetilanne(self):
        """
        Päivittää pistetilanteen, kun peli päättyy voittoon tai tasapeliin.
        :return:
        """
        self.__pistetilanne.configure(text="Pelaaja X voitot: {:d}, Pelaaja O voitot: {:d}, Tasapelit: {:d}".format(self.__pelaajan_X_voitot,self.__pelaajan_O_voitot,self.__tasapelit))

def main():

    kaynnistys = Kayttoliittyma()

main()