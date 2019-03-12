# 人間 vs AIのサンプルです．
import quoridor
import quoridor_ai

def main():
    game = quoridor.Quoridor()
    ai = quoridor_ai.QuoridorAI()

    turn = True # 先攻が人間
    while not game.is_over():
        game.display()
        if turn:
            ok = False
            while not ok:
                op = list(input().split())
                y = int(op[0])
                x = int(op[1])
                if len(op) == 3:
                    d = quoridor.WallDir.N
                    if op[2] == 'V':
                        d = quoridor.WallDir.V
                    else:
                        d = quoridor.WallDir.H
                    print(y,x,d)
                    ok = game.operate((y,x,d))
                else:
                    print(y,x)
                    ok = game.operate((y,x))
                if not ok :
                    print( "Invalid operation" )
        else:
            move = ai.bestmove(game)
            print(move)
            game.operate(move)
        turn = not turn

    game.display()

if __name__ == '__main__':
    main()
