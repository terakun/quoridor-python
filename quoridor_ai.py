# Quoridor AIのサンプルです．
import random
import quoridor

class QuoridorAI:
    def __init__(self):
        self.game = quoridor.Quoridor()

    def bestmove( game ):
        ops = game.next_operations()
        return ops[ random.randint(0,len(ops)-1) ]

