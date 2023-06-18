import sys
import timeit
class DAWG:

    def __init__(self):
        #hat die Form (n0,a):(n1,type) ; 0... primary edge, 1... secondary edge
        self.edges = {}
        self.suffixpointer = {}
        self.input = ""
        self.nodecounter = 0
        self.source = 0


    def builddawg(self):
        #1
        currentsink = self.source
        round = 1
        for letter in self.input:
            currentsink = self.update(currentsink,letter)
            print("Round " + str(round) +" done.")
            round += 1
        return self.source

    def update(self,currentsink , letter):
        #1
        self.nodecounter += 1
        newsink = self.nodecounter
        self.edges[(currentsink, letter)] = (newsink, 0)

        #2
        currentstate = currentsink
        suffixstate = None

        #3
        while self.source != currentstate and suffixstate == None:
            #a)
            currentstate = self.suffixpointer[currentstate]

            #b)
            #try:
             #   self.edges[(currentstate, letter)]
             #   if self.edges[(currentstate, letter)] == 0:
             #       #2
               #     self.edges[(currentstate, letter)] = (suffixstate, 0)
              #  else:
                    #3
                #    childstate = self.edges[(currentstate, letter)][0]
                #    suffixstate = self.split(currentstate, childstate, letter)
                #1
           # except KeyError:
            #    self.edges[(currentstate, letter)] = (newsink, 1)
            try:
                self.edges[(currentstate, letter)]
                ## 3 (b) (2)
                if self.edges[(currentstate, letter)][1] == 0:
                    ## currentstate has a primary outgoing ...
                    suffixstate = self.edges[(currentstate, letter)][0]
                else:
                    ## currentstate has a secondary outgoing ...
                    ## 3 (b) (3)
                    childstate = self.edges[(currentstate, letter)][0]
                    suffixstate = self.split(currentstate, childstate, letter)
            except KeyError:
                ## 3 (b) (1)
                ## currentstate does not have an outgoing edge labled a ...
                self.edges[(currentstate, letter)] = (newsink, 1)

        #4
        if suffixstate == None:
            suffixstate = self.source

        #5
        self.suffixpointer[newsink] = suffixstate
        return newsink



    def split(self, parentstate, childstate, letter):
        #1
        self.nodecounter += 1
        newchildstate = self.nodecounter

        #2
        self.edges[(parentstate, letter)] = (newchildstate, 0)

        #3
        all_outgoing_edges_from_childstate = [childstate_item for childstate_item in dict(self.edges).items() if childstate_item[0][0] == childstate]
        for item in all_outgoing_edges_from_childstate:
            self.edges[newchildstate, item[0][1]] = (item[1][0], 1)

        #4
        self.suffixpointer[newchildstate] = self.suffixpointer[childstate]

        #5
        self.suffixpointer[childstate] = newchildstate

        #6
        currentstate = parentstate

        #7
        while currentstate != self.source:
            #a
            currentstate = self.suffixpointer[currentstate]

            #b
            all_secondary_edges_from_currentstate_to_childstate = [pair for pair in self.edges.items() if pair[0][0] == currentstate and pair[1][0] == childstate and pair[1][1] == 1]
            if len(all_secondary_edges_from_currentstate_to_childstate) != 0:
                for pair in all_secondary_edges_from_currentstate_to_childstate:
                    self.edges[pair[0]] = (newchildstate, 1)
            else:
                break

        return newchildstate

    def checkword(self, word):
        tempnode = 0
        for letter in word:
            try:
                tempnode = self.edges[(tempnode, letter)][0]
            except KeyError:
                print("Word not in DAWG")
                return
        print("Word in DAWG")

    def readfile(self, path):
        with open(path, 'r', encoding="utf-8") as file:
            self.input = file.read().replace("\n", " ")
            print(len(self.input))

if __name__ == '__main__':

    path = input("Willkommen beim DAWG. Bitte geben Sie ihren Pfadnamen des .txt Dokument an, mit welchem der Graph aufgebaut werden sollte.\n"
                 "Das Textdokument muss in UTF-8 kodiert sein. Jakob Murauer v.2.0\n")
    x = DAWG()
    try:
        x.readfile(path)
    except FileNotFoundError:
        print("Datei konnte nicht gefunden werden. Programm wird geschlossen.")
        sys.exit(0)

    print("read done")
    x.builddawg()
    print("build done")


    query = "query"
    while query != "":
        query = input("Bitte geben Sie ihr Suchwort an. Wenn Sie das Programm verlassen möchten bitte ENTER drücken.")
        if query != "":
            x.checkword(query)

