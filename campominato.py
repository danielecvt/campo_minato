from random import randint

class Griglia:
    def __init__(self, righe:int, colonne:int, mine:int) -> None:
        self._griglia:list[list[str]] = [['0' for _ in range (colonne)] for _ in range(righe)]
        for _ in range(mine):
            x = randint(0, righe - 1)
            y = randint(0, colonne - 1)
            #impedice che due o più bombe siano messe nella stessa casella
            while self._griglia[x][y] == 'X':
                x = randint(0, righe - 1)
                y = randint(0, colonne - 1)
            self._griglia[x][y] = 'X'

        def mine_adiacenti(i:int, j:int)->str:
            mine = 0
            if  i  and j  and i < righe - 1 and j < colonne - 1:
                #se casella non è sul bordo della griglia tranne gli angoli
                if self._griglia[i - 1][j - 1] == 'X': mine += 1
                if self._griglia[i - 1][j] == 'X': mine += 1
                if self._griglia[i - 1][j + 1] == 'X': mine += 1
                if self._griglia[i][j - 1] == 'X': mine += 1
                if self._griglia[i][j + 1] == 'X': mine += 1
                if self._griglia[i + 1][j - 1] == 'X': mine += 1
                if self._griglia[i + 1][j] == 'X': mine += 1
                if self._griglia[i + 1][j + 1] == 'X': mine += 1
            
            if i == 0 and 0 < j < colonne - 1:
                #se è la casella sulla prima riga tranne gli angoli
                if self._griglia[i][j - 1] == 'X': mine += 1
                if self._griglia[i][j + 1] == 'X': mine += 1
                if self._griglia[i + 1][j - 1] == 'X': mine += 1
                if self._griglia[i + 1][j] == 'X': mine += 1
                if self._griglia[i + 1][j + 1] == 'X': mine += 1
            
            if i == righe - 1 and 0 < j < colonne - 1:
                #se la casella è sull'ultima riga tranne gli angoli
                if self._griglia[i - 1][j - 1] == 'X': mine += 1
                if self._griglia[i - 1][j] == 'X': mine += 1
                if self._griglia[i - 1][j + 1] == 'X': mine += 1
                if self._griglia[i][j - 1] == 'X': mine += 1
                if self._griglia[i][j + 1] == 'X': mine += 1

            if j == 0 and 0 < i < righe - 1 :
                #se la casella è sulla prima colonna tranne gli angoli
                if self._griglia[i - 1][j] == 'X': mine += 1
                if self._griglia[i - 1][j + 1] == 'X': mine += 1
                if self._griglia[i][j + 1] == 'X': mine += 1
                if self._griglia[i + 1][j] == 'X': mine += 1
                if self._griglia[i + 1][j + 1] == 'X': mine += 1

            if j == colonne - 1 and 0 < i < righe - 1:
                #se la casella è sull'ultima colonna tranne gli angoli
                if self._griglia[i - 1][j - 1] == 'X': mine += 1
                if self._griglia[i - 1][j] == 'X': mine += 1
                if self._griglia[i][j - 1] == 'X': mine += 1
                if self._griglia[i + 1][j - 1] == 'X': mine += 1
                if self._griglia[i + 1][j] == 'X': mine += 1

            if i == 0 and j == 0:
                if self._griglia[i][j + 1] == 'X': mine += 1
                if self._griglia[i + 1][j + 1] == 'X': mine += 1
                if self._griglia[i + 1][j] == 'X': mine += 1

            if i == righe - 1 and j == 0:
                if self._griglia[i][j + 1] == 'X': mine += 1
                if self._griglia[i - 1][j + 1] == 'X': mine += 1
                if self._griglia[i - 1][j] == 'X': mine += 1

            if i == righe - 1 and j == colonne - 1:
                if self._griglia[i][j - 1] == 'X': mine += 1
                if self._griglia[i - 1][j - 1] == 'X': mine += 1
                if self._griglia[i - 1][j] == 'X': mine += 1
            
            if i == 0 and j == colonne - 1:
                if self._griglia[i][j - 1] == 'X':mine += 1
                if self._griglia[i + 1][j-1] == 'X':mine += 1
                if self._griglia[i + 1][j] == 'X':mine += 1
            if mine: return str(mine)
            return '0'

        for i in range(righe):
            for j in range(colonne):
                if self._griglia[i][j] != 'X':
                    self._griglia[i][j] = mine_adiacenti(i,j)

    def __str__(self) -> str:
        ris = ''
        for l in self._griglia:
            ris += str(l) + '\n'
        return ris

    @property
    def griglia(self):
        return self._griglia

class StateError(Exception):
    def __init__(self, stato: int):
        self.statoErr = stato

class Partita:
    def __init__(self, larghezza:int, altezza:int, n_mine:int) -> None:
        self._larghezza = larghezza
        self._altezza = altezza
        self._n_mine = n_mine
        self._stato_corrente:int = 0 #0 = in corso; 1 = terminata con successo; 2 = terminata fallendo
        g = Griglia(altezza, larghezza, n_mine)
        self._griglia_sottostante: list[list[str]] = g.griglia
        self._storico_x: list[int] = [-1]
        self._storico_y: list[int] = [-1]
        self._evoluzione: list[Tabellone] = [Tabellone(self)]
    
    @property
    def larghezza(self) -> int:
        return self._larghezza
    
    @property
    def altezza(self) -> int:
        return self._altezza
    
    @property
    def n_mine(self) -> int:
        return self._n_mine
    
    @property
    def stato_corrente(self) -> int:
        return self._stato_corrente

    @property
    def storico_x(self):
        return self._storico_x
    
    @property
    def storico_y(self):
        return self._storico_y
    
    @property
    def evoluzione(self) -> list['Tabellone']:
        return self._evoluzione
    
    @evoluzione.setter
    def evoluzione(self, t: 'Tabellone'):
        self.evoluzione.append(t)
    
    @property
    def griglia_sottostante(self) -> list[list[str]]:
        return self._griglia_sottostante
    
    def segna_casella(self, riga:int, colonna:int) -> None:
        ''' 
        se lo stato della partita è partita in corso e la casella è coperta,
        contrassegna la casella di riga e colonna passati come parametri come contenente
        una mina, se non era già stata contrassegnata tale;
        altrimenti toglie il contrassegno dalla casella stessa.
        Se lo stato della partita non è partita in corso, 
        oppure la casella è scoperta, viene lanciata un’eccezione opportuna.

        Tabellone corrente, le caselle sono rappredentate con:
        C = coperta senza mina con mina non segnata;
        D = coperta senza mina ed è segnata;
        X = coperta contiene mina e non è segnata;
        Y = coperta con mina e segnata;
        Z = scoperta con mina.
        ''' 
        try:
            if self._stato_corrente != 0 or not self.is_coperta(riga, colonna):
                raise StateError(self._stato_corrente)
            
            self.evoluzione[-1].segna_casella(riga, colonna)

        except StateError as e:
            print('impossibile segnare una cella scoperta')
            if e.statoErr == 1: print("Partita finita con successo")
            if e.statoErr == 2: print("Partita finita senza successo")

    def get_casella_segnata(self, riga:int, colonna:int) -> bool:
        '''
        restituisce True se, nel tabellone della configurazione corrente,
        la casella di riga e colonna passati come parametri è stata contrassegnata
        dal giocatore come casella contenente una mina, False altrimenti.
        ''' 
        return self.evoluzione[-1].is_segnata(riga, colonna)

    def  scopriCasella(self, riga:int, colonna:int) -> None: 
        '''
        se lo stato della partita è partita in corso e la casella non è segnata,
        scopre la casella di riga e colonna passati come parametri, e di conseguenza
        se è stata scoperta una casella che non contiene una mina: se tale casella 
        è sicura (cioè non ha nessuna casella adiacente contenente mine), vengono 
        scoperte tutte le caselle adiacenti, iterando il procedimento fino a che tutte 
        le caselle sicure hanno tutte le caselle a loro adiacenti scoperte.
        La partita viene portata in stato di terminazione con successo se dopo
        aver scoperto la casella di riga e colonna passati come parametro (ed 
        eventualmente le caselle adiacenti alle caselle sicure) rimangono da scoprire solo 
        caselle che contengono mine. 
        se è stata scoperta una casella contenente una mina porta la partita in stato di 
        terminazione senza successo.
        Al termine, viene opportunamente memorizzato il tabellone così ottenuto in modo 
        che possa essere in seguito restituito dalla proprietà evoluzione.
        Se lo stato della partita non è partita in corso, oppure la casella è segnata,
        viene lanciata una eccezione opportuna.
        '''
        try:
            if self._stato_corrente != 0 or self.get_casella_segnata(riga, colonna):
                raise StateError(self.stato_corrente)   
            
            t = Tabellone.copia_tabellone(self.evoluzione[-1])
            self.storico_x.append(riga)
            self.storico_y.append(colonna)
            self._scopriCasella(t, riga, colonna)
            # numero mine = numero caselle coperte? 
            # Cioè il gioco è finito con successo?
            if self.stato_corrente == 2:
                #evita che restando due caselle coperte di cui una è una bomba
                #si scopra la bomba e si vinca
                self.evoluzione = t
                return
            
            coperte = 0
            for i in range(len(t.griglia_attuale)):
                for j in range(len(t.griglia_attuale[i])):
                    if t.is_coperta(i,j):
                        coperte += 1

            if coperte == self.n_mine:
                self._stato_corrente = 1
                self.evoluzione = t
                return
            self.evoluzione = t

        except StateError as e:
            if self.evoluzione[-1].is_segnata(riga, colonna):
                print('Non puoi scoprire una casella segnata')
            if e.statoErr == 1: print("Partita finita con successo")
            if e.statoErr == 2: print("Partita finita senza successo")
            print(self.evoluzione)
            return
    
    def _scopriCasella(self, t: 'Tabellone', riga:int, colonna:int) :
        if riga == -1 or colonna == -1 or riga == t.righe or colonna == t.colonne: return
        if not t.is_coperta(riga, colonna): return
        t.scopri_casella(riga, colonna)            
        if self.griglia_sottostante[riga][colonna] != 'X' and self.griglia_sottostante[riga][colonna] == '0':
            for i in range (-1, 2):
                for j in range (-1,2):
                    if -1 < riga + i < t.righe and -1 < colonna + j < t.colonne :
                        if self.griglia_sottostante[riga+i][colonna+j] != 'X':
                            self._scopriCasella(t, riga + i, colonna + j)
        elif self.griglia_sottostante[riga][colonna] == 'X':
            self._stato_corrente = 2
            return
        
    def get_mine_adiacenti(self, riga:int, colonna:int) -> int:
        '''
        se la casella di riga e colonna passati come paremtri non contiene mine, 
        restituisce il numero di caselle ad essa adiacenti contenenti mine 
        (0 se la casella è sicura). Se la casella di riga e 
        colonna passati come paremtri contiene mine, viene restituito -1.
        '''
        if self.griglia_sottostante[riga][colonna] != 'X':
            return int(self.griglia_sottostante[riga][colonna]) 
        else:
            return -1

    def  contiene_mina(self, riga:int, colonna:int) -> bool:
        '''
        restituisce True se la casella di riga e colonna passati come parmetri
        contiene una mina, False altrimenti.
        '''
        return self.griglia_sottostante[riga][colonna] == 'X'

    def  is_coperta (self, riga:int, colonna:int) -> bool:
        '''
        restituisce True se la casella di riga e colonna passati come paremetri
        è coperta nel tabellone della configurazione corrente, False altrimenti.
        '''    
        return self.evoluzione[-1].is_coperta(riga, colonna)

    def __str__(self) -> str:
        '''
        deve restituire una stringa che contiene, in sequenza, le rappresentazioni 
        di tutti i tabelloni ottenuti a seguito del fatto che il giocatore scopre 
        delle caselle, preceduta dall’indicazione della mossa (che consiste nello 
        scoprire una casella) che ha condotto a tale tabellone.
        '''
        ris = ''
        for i in range(len(self.evoluzione)):
            ris += f"Mossa {i}: riga {self.storico_x[i]} colonna {self.storico_y[i]}\n"
            for j in range(len(self.evoluzione[i].griglia_attuale)):
                for z in range(len(self.evoluzione[i].griglia_attuale[j])):
                    ris += self.evoluzione[i].griglia_attuale[j][z]
                ris += '\n'
        return ris
        

        
class Tabellone:
    n = 0
    def __init__(self, p:Partita) -> None:
        self._righe = p.altezza
        self._colonne = p.larghezza
        self._n_mine = p.n_mine 
        self._partita = p
        if Tabellone.n == 0:
            griglia_attuale: list[list[str]] = []
            for i in range(len(p.griglia_sottostante)):
                griglia_attuale.append([])
                for j in range(len(p.griglia_sottostante[0])):              
                    if p.griglia_sottostante[i][j] != 'X':
                        griglia_attuale[i].append('C')
                    else:
                        griglia_attuale[i].append('X')
        else:
            griglia_attuale: list[list[str]] = [[p.evoluzione[-1].griglia_attuale[j][i] for i in range (p.larghezza)] for j in range(p.altezza)]
            
        self._griglia_attuale:list[list[str]] = griglia_attuale
        Tabellone.n += 1
    
    @property
    def griglia_attuale(self):
        return self._griglia_attuale
    
    @griglia_attuale.setter
    def griglia_attuale(self, riga:int, colonna:int, value:str):
        self._griglia_attuale[riga][colonna] = value
    
    @property
    def righe(self):
        return self._righe
    
    @property
    def colonne(self):
        return self._colonne
    
    @property
    def n_mine(self):
        return self._n_mine
    
    
    @classmethod
    def copia_tabellone (cls, t: 'Tabellone') -> 'Tabellone':
        '''
        costruisce un tabellone che è la copia del tabellone t. 
        Attenzione: le modifiche eventualmente fatte al nuovo 
        tabellone non devono ripercuotersi su t e viceversa.
        '''
        p = t._partita
        newT = Tabellone(p)
        return newT

    def segna_casella(self, riga:int, colonna:int) -> None:
        '''
        contrassegna la casella di riga e colonna
        passati come parametri come contenente una mina, se 
        non era già stata contrassegnata tale; 
        altrimenti toglie il contrassegno dalla casella stessa.
        '''
        if self.is_segnata(riga, colonna): 
            if self._griglia_attuale[riga][colonna] == 'D': self._griglia_attuale[riga][colonna] = 'C'
            if self._griglia_attuale[riga][colonna] == 'Y': self._griglia_attuale[riga][colonna] = 'X'
        else:
            if self._griglia_attuale[riga][colonna] == 'C': self._griglia_attuale[riga][colonna] = 'D'
            if self._griglia_attuale[riga][colonna] == 'X': self._griglia_attuale[riga][colonna] = 'Y'

    
    def  is_segnata(self, riga:int, colonna:int) -> bool:
        '''
        restituisce True se la casella di riga e colonna 
        passati come parametri è stata contrassegnata come 
        casella contenente una mina, False altrimenti.
        '''
        return self._griglia_attuale[riga][colonna] == 'D' or self._griglia_attuale[riga][colonna] == 'Y'

    def scopri_casella(self, riga:int, colonna:int) -> None:
        '''
        segna come scoperta la casella di riga e colonna passati come parametri.
        '''
        if self.is_coperta(riga, colonna):
            if self._griglia_attuale[riga][colonna] == 'C':
                self._griglia_attuale[riga][colonna] = self._partita.griglia_sottostante[riga][colonna]
            if self._griglia_attuale[riga][colonna] == 'X':
                self._griglia_attuale[riga][colonna] = 'Z'
        
    def is_coperta (self, riga:int, colonna:int) -> bool:
        '''
        restituisce True se la casella di riga e colonna passati come parametri 
        è coperta nel tabellone, False altrimenti.
        '''
        return self._griglia_attuale[riga][colonna] == 'C' or \
                self._griglia_attuale[riga][colonna] == 'D' or \
                self._griglia_attuale[riga][colonna] == 'X' or \
                self._griglia_attuale[riga][colonna] == 'Y'    
                
    def __str__(self) -> str:
        '''
        Tabellone corrente, le caselle sono rappredentate con:
        C = coperta senza mina con mina non segnata;
        D = coperta senza mina ed è segnata;
        X = coperta contiene mina e non è segnata;
        Y = coperta con mina e segnata;
        Z = scoperta con mina.
        n da 0 a 8 scoperta che non contiene mine ma ha n mine adiacenti.
        '''
        ris = 'Griglia attuale \n'
        for l in self._griglia_attuale:
            for c in l:
                ris += c
            ris += '\n'
        # ris += 'Griglia sottostante \n'
        # for l in self._partita.griglia_sottostante:
        #     for c in l:
        #         ris += c
        #     ris += '\n'

        return ris
    
    def gioca(self):
        '''
        Permette di vedere le caselle e giocare da terminale
        '''
        ris = "tabellone attuale \n"
        for l in self._griglia_attuale:
            for c in l:
                if c == "X":
                    ris += "C"
                else:
                    ris += c
            ris += '\n'
        return ris
def _test():
    i = 0
    p = Partita(10, 10, 10)
    print(p.evoluzione[-1].gioca())
    print("inserisci numeri da 1 a 10 compresi")
    while p.stato_corrente == 0:
        riga = int(input("mossa "+str(i + 1)+", riga:"))
        colonna = int(input("mossa "+str(i + 1)+", colonna:"))
        if 1 <= riga <= 10 and 1 <= colonna <= 10:
            p.scopriCasella(riga - 1, colonna - 1)
            i += 1
            print(p.evoluzione[-1].gioca())
        else:
            print("Bisogna inserire numeri da 1 a 10 compresi!")
    if p.stato_corrente == 1:
        print("HAI VINTO")
    if p.stato_corrente == 2:
        print("HAI PERSO")

if __name__ == "__main__":
    _test()


    