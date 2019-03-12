# Quoridor AIのサンプルです．
import random
import quoridor

class QuoridorAI:
    def __init__(self):
        self.game = quoridor.Quoridor()
        self.game.display()

    def bestmove( self , game ):
        game.display()
        ops = game.valid_operations()
        return ops[ random.randint(0,len(ops)-1) ]
