from typing import cast
from ezgraphics import GraphicsWindow

from campominato import *
class Player:
        def __init__(self,number:str, name:str, games:str) -> None:
            self._number = int(number)
            self._name = name
            self._games = int(games)

        @property
        def number(self):
            return self._number
        
        @property
        def name(self):
            return self._name
        
        @property
        def games(self):
            return self._games
        
        @games.setter
        def games(self, s:str):
            self._games = s
        
        def get_player(self):
            return str(self.number)+'\t'+str(self.name)+'\t games '+str(self.games)+'\t'
        
        def __str__(self) -> str:
            return str(self.number)+'\t'+str(self.name)+'\t'+str(self.games)+'\t'
class GUI :
    
    def __init__ (self, p:Partita):
        self._p = p
        self._colore_attuale:list[list[str]] = [['lightgray' for _ in range (p.larghezza)] for _ in range(p.altezza)]
        self._colore_precedente:list[list[str]] = [['lightgray' for _ in range (p.larghezza)] for _ in range(p.altezza)] 
        #le due matrici di colore servono per ottimizzare il gioco permettono di stampare
        # sul canvas una cella solo se ha cambiato colore, non è possibile a tale scopo sfruttare
        # evoluzione perché segnare una cella non è considerata una mossa
        self._numeri:list[list[int]] = [[0 for _ in range (p.larghezza)] for _ in range(p.altezza)]
        
        self._win = GraphicsWindow(50*p.larghezza,50+50*p.altezza)
        self._win.setTitle("Campo minato")
        self._win.enableEvents("MouseDown", "KeyPress")
        self._win.setEventHandler(self.event_handler)
        self._canvas = self._win.canvas()

        
        self._player_attuale:Player|None = None# player precedente alla scelata
        self._window:str = "players" 
        self._player:str = ''# palyer da iniserire con add player
        self._lettere:list[int] = []
        self._gioca = True #impedisce di fare un'altra mossa dopo che il gioco termina
                            # inoltre permette di mostrare la casella nera sotto la scritta
                            # HAI VINTO o HAI PERSO
        self.set_griglia(p)
        try:
            with open("players.txt", "r") as file:
                if len(file.readlines()) == 0:
                    self._first_player:bool = True
                else:
                    self._first_player:bool = False
                if self._first_player:
                    self.new_player_window()
                else:
                    self._players:list[Player] = self.players()
                    self.players_window()
        except FileNotFoundError or FileExistsError:
            with open("players.txt", "w") as file:
                self._window = 'new_player'
                self._first_player = True
                self.new_player_window()
        
            
        
    def set_griglia(self, p:Partita):
        for i in range (p.altezza):
            for j in range (p.larghezza):
                self._colore_precedente[i][j] = self._colore_attuale[i][j]
                if p.evoluzione[-1].is_coperta(i, j) and not p.evoluzione[-1].is_segnata(i, j): 
                    self._colore_attuale[i][j] = 'lightgray'
                elif p.evoluzione[-1].is_segnata(i, j):
                    self._colore_attuale[i][j] = 'red'
                elif p.evoluzione[-1].griglia_attuale[i][j] == 'Z':
                    self._colore_attuale[i][j] = 'black'
                elif p.evoluzione[-1].griglia_attuale[i][j] == '0':
                    self._colore_attuale[i][j] = 'white'
                elif not p.evoluzione[-1].is_coperta(i, j):
                    self._colore_attuale[i][j] = 'white'
                    self._numeri[i][j] = int(p.evoluzione[-1].griglia_attuale[i][j])

        if self._window == "end_game": # ESC premuto
            for i in range (p.altezza):
                for j in range (p.larghezza):
                    self._colore_precedente[i][j] = self._colore_attuale[i][j]
                    if p.evoluzione[-1].griglia_attuale[i][j] == 'X': 
                        self._colore_attuale[i][j] = 'black'

    def players_window(self):
        self._gioca = True
        self._window = "players"
        self._canvas.clear()
        self._canvas.setFontSize(20)
        self._canvas.setColor('black')
        self._canvas.setTextAnchor('nw')
        self._canvas.drawText(0, 10, 'Chi vuole giocare?')
        for i in range(len(self._players)):
            self._canvas.drawLine(0, 50 * i +50, 50 * self._p.larghezza, 50 * i +50)
            self._canvas.drawText(0, 50 * (i + 1) + 10, self._players[i].get_player())
            self._canvas.drawLine(0, 50 * (i + 1) +50, 50 * self._p.larghezza, 50 * (i + 1)+50)
        self._canvas.setColor('red')
        #self._canvas.setTextAnchor("center")
        self._canvas.drawLine(0, 50 * self._p.altezza , 50 * self._p.larghezza, 50 * self._p.altezza)  
        self._canvas.drawText(20*(self._p.larghezza - 1), 50*self._p.altezza+10 , 'new player')
        self._canvas.setColor('white')
        self._win.wait()

    def play(self):
        self.bar()
        #self._window = "game"
        self.set_griglia(self._p)
        if self._gioca :
            for i in range (self._p.altezza):
                for j in range(self._p.larghezza):
                    if len(self._p.evoluzione) == 1:
                        self._canvas.setColor(self._colore_attuale[i][j])
                        self._canvas.setOutline ("black")
                        self._canvas.drawRectangle(50 * j, 50 * i + 50, 50, 50)
                        if self._numeri[i][j] != 0:
                            self._canvas.setColor('black')
                            self._canvas.drawText(50 * j + 17, 50 * i + 50 + 10, str(self._numeri[i][j]))
                    elif self._colore_attuale[i][j]!= self._colore_precedente[i][j]: 
                        self._canvas.setColor(self._colore_attuale[i][j])
                        self._canvas.setOutline ("black")
                        self._canvas.drawRectangle(50 * j, 50 * i + 50, 50, 50)
                        if self._numeri[i][j] != 0:
                            self._canvas.setColor('black')
                            self._canvas.drawText(50 * j + 17, 50 * i + 50 + 10, str(self._numeri[i][j]))

        print('partita sin qui giocata')
        print(self._p)

        if self._p.stato_corrente == 1:
            self._canvas.setTextAnchor('center')
            self._canvas.setColor('white')
            self._canvas.setOutline ("black")
            self._canvas.drawRectangle(25 * (self._p.larghezza-3), 25 * (self._p.altezza-1), 150, 50)
            self._canvas.setColor('black')
            self._canvas.drawText(25 * self._p.larghezza, 25 * self._p.altezza,'HAI VINTO')
            self._window = "end_game"
            self._gioca = False
            self.update_player()
        elif self._p.stato_corrente == 2:
            self._canvas.setTextAnchor('center')
            self._canvas.setColor('white')
            self._canvas.setOutline ("black")
            self._canvas.drawRectangle(25 * (self._p.larghezza-3), 25 * (self._p.altezza-1), 150, 50)
            self._canvas.setColor('black')
            self._canvas.drawText(25 * self._p.larghezza, 25 * self._p.altezza, 'HAI PERSO')
            self._window = "end_game"
            self._gioca = False
            self.update_player()
        elif self._window == "end_game":
            self._canvas.setTextAnchor('center')
            self._canvas.setColor('white')
            self._canvas.setOutline ("black")
            self._canvas.drawRectangle(25 * (self._p.larghezza-3), 25 * (self._p.altezza-1), 150, 50)
            self._canvas.setColor('black')
            self._canvas.drawText(25 * self._p.larghezza, 25 * self._p.altezza, 'END GAME')
            self._gioca = False
            #self.reset()
            self.update_player()
        self._win.wait()

    def bar (self):
        self._canvas.setFontSize(20)
        self._canvas.setOutline('black')
        self._canvas.setFill('white')
        self._canvas.setTextAnchor('nw')
        self._canvas.drawRectangle(0, 0, 50 * p.larghezza, 50)
        string = self._player_attuale.name + " games: "+ str(self._player_attuale.games)
        self._canvas.drawText(0, 5, string)

    def update_player(self):
        self._player_attuale = cast(Player, self._player_attuale)
        line = -1
        for i in range(len(self._players)):
            if self._players[i].number == self._player_attuale.number:
                self._players[i] = self._player_attuale
            line = i
        with open("players.txt", 'r') as file:
            lines = file.readlines()
            lines[line] = f'{self._player_attuale.number} {self._player_attuale.name} \
                            {self._player_attuale.games}\n'
        with open("players.txt", 'w') as file:
            file.writelines(lines)


    def players(self) -> list[Player]:
        '''
        Restituisce una lista di dizionari contenenti informazioni sui players
        '''
        players: list[dict[str,str]] = []
        players = GUI.get_players()
        #print(players)
        playersRis:list[Player] = []
        for p in players:
            if 'number' in p:
                player = Player(p['number'], p['name'], p['games']) 
                playersRis.append(player)
        return playersRis

    @staticmethod
    def get_players()->list[dict[str,str]]:
        '''
        Restituisce una lista di dizionari contenenti informazioni sui players
        prese dal file
        '''
        with open("players.txt", "r") as file:
            #players: list[dict[str,str]] = [{} for _ in range(len(file.readlines()))]
            players: list[dict[str,str]] = [{},{},{},{},{},{},{},{},{},{},{}]
            lines = 0
            words = 0
            for riga in file.readlines():
                for word in riga.split():
                    if words == 0: players[lines]['number'] = word
                    if words == 1: players[lines]['name'] = word
                    if words == 2: players[lines]['games'] = word
                    words += 1
                words = 0
                lines += 1
        return players

    def event_handler (self, oggetto, evento) :
        print (f"mouse_handler : oggetto = {oggetto} evento = {evento}")
            
        if self._window == "players":
            y = (evento.y // 50) - 1
            print (y)
            if y == 9 and y>= len(self._players):
                self.new_player_window()
            elif y < len(self._players):
                self._player_attuale = self._players[y]
                self._player_attuale.games = str( int(self._player_attuale.games) + 1)
                self._window = "game"
                self._first_player = False
                self._canvas.clear()
                self.play()
        elif self._window == "game":
            x = evento.x // 50
            y = evento.y // 50
            print (x)
            print (y - 1)
            if evento.num == 1:
                self._p.scopriCasella(y - 1, x)
                
            elif evento.num == 3:
                self._p.segna_casella(y - 1, x)
                
            elif evento.keycode == 27 or evento.keycode == 9: #ESC
                self._window = "end_game"
            self.play()
            #print(self._p.evoluzione[-1])
        elif self._window == "new_player":
            
            if evento.char != '??': #esclude caratteri speciali
                if evento.keycode != 8 and (evento.keycode != 9 and evento.keycode != 27):
                    self._canvas.drawText(sum(self._lettere), 200, evento.char)
                if evento.char == 'i' or evento.char == 'I' or evento.char == 'l':
                    self._lettere.append(5)
                elif evento.char == 'D' or evento.char == 'O':
                    self._lettere.append(20)
                elif (evento.keysym != 'Shift_L' and evento.keysym != 'Caps_Lock' and evento.keycode != 8) and (evento.keycode != 9 and evento.keycode != 27):
                    self._lettere.append(15)
                if evento.char != '\r' and evento.char != '\x08' and (evento.keycode != 9 and evento.keycode != 27):
                    self._player += evento.char
                if evento.keycode == 8:#cancella l'ultima lettera
                    self._player = self._player[:-1]
                    print(self._player)
                    self._canvas.setColor('white')
                    s = 0
                    for i in range(len(self._lettere)-1):
                        s += self._lettere[i]
                    self._canvas.drawRectangle(s,200, self._lettere[-1] + 2, 30)
                    self._lettere.pop()
                    self._canvas.setColor('black')
                #print(self._player)
            if sum(self._lettere) != 0:
                    self._canvas.drawLine(0, 450, 50 * self._p.larghezza, 450)
                    self._canvas.setTextAnchor('center')
                    self._canvas.drawText(250, 500, "GIOCA")
                    self._canvas.setTextAnchor('nw')

            elif sum(self._lettere) == 0:
                    self._canvas.setColor("white")
                    self._canvas.drawLine(0, 450, 500, 450)
                    self._canvas.drawRectangle(200, 450, 100, 70)
                    self._canvas.setColor("black")

            if 0 <= evento.x <=500 and 450<= evento.y <= 550 and sum(self._lettere) != 0 and self._first_player:
                self._first_player = False
                with open("players.txt", 'w') as file:
                    p= Player('1', self._player, '1')
                    file.writelines(f'{p.number} {p.name} {p.games}\n')
                self._players:list[Player] = [p]
                self._player_attuale = p
                self._player = ''
                self._window = "game"
                self.play()
            elif 0 <= evento.x <=500 and 450<= evento.y <= 550 and not self._first_player and (evento.keycode != 9 and evento.keycode != 27):
                self._lettere = []
                p = Player(str(len(self._players)+1), self._player, '1')
                self._players.append(p)
                self._player_attuale = p
                self._window = "game"
                with open("players.txt", 'r') as file:
                    lines = file.readlines()
                    lines.append(f'{p.number} {p.name} {p.games}\n')
                    print(lines)
                with open("players.txt", 'w') as file:
                    file.writelines(lines)
                self._player = ''
                self.play()

            if (evento.keycode == 27 or evento.keycode == 9) and (sum(self._lettere) == 0):
                self._canvas.clear()
                self.players_window()
            elif (evento.keycode == 27 or evento.keycode == 9) and (sum(self._lettere) != 0): # ESC
                print ("TASTO ESC PREMUTO, ciao")
                print (self._lettere)
                #azzerare la lista degli spazi dei caratteri
                self._lettere = []
                self._canvas.clear()
                self.new_player_window()
                
        if (self._window == "end_game" or self._p.stato_corrente == 1 or self._p.stato_corrente == 2)\
            and not self._gioca and evento.keycode == 27 or evento.keycode == 9:
            print ("TASTO ESC PREMUTO")
            self.reset()
            self.players_window()
             
            
    def new_player_window(self):
        self._window = 'new_player'
        self._canvas.clear()
        self._canvas.setColor("black")
        self._canvas.setFontSize(20)
        self._canvas.drawText(10, 0, 'Clicca ovunque in questa finestra,')
        self._canvas.drawText(10, 30, 'scrivi il nome del nuovo player')
        self._canvas.drawText(10, 60, 'poi premi gioca per giocare.')
        self._win.wait()

    def reset(self) -> None:
        self._window='players'
        self._canvas.clear()
        Tabellone.n = 0
        match diff:
            case '1': p = Partita(10,10,10)
            case '2': p = Partita(15,10,15)
            case '3': p = Partita(20,10,20)
            case _: p = None
        p = cast(Partita, p)
        self._p = p
        #print(self._p.evoluzione[-1].griglia_attuale)
        self._numeri= [[0 for _ in range (p.larghezza)] for _ in range(p.altezza)]
        self.set_griglia(p)
        self.players_window()
        
if  __name__ == "__main__" :
    flag = True
    diff = '' #difficoltà variabile globale
    while flag:
        diff = input("scegli la difficoltà: 1=facile, 2=medio 3=difficile. ")
        if diff == '1' or diff == '2' or diff == '3':
            flag = False
        else:
            print("inserisci: 1, 2 o 3.")
    match diff:
        case '1': p = Partita(10,10,10)
        case '2': p = Partita(15,10,15)
        case '3': p = Partita(20,10,20)
        case _: p = None
    p = cast(Partita, p)
    g = GUI(p)
    