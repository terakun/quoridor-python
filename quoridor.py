from enum import Enum

W = 9
H = 9

DY = [0,1,0,-1]
DX = [1,0,-1,0]

WHITE_GOAL_Y = H - 1 
BLACK_GOAL_Y = 0 

def in_wallarea(y,x):
    return (0 <= y < H-1) and (0 <= x < W-1)

class WallDir(Enum):
    N = 0
    H = 1
    V = 2

class MoveDir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class Color(Enum):
    N = 0
    WHITE = 1
    BLACK = 2

class Board:
    def __init__(self):
        self.table = [[WallDir.N for i in range(W-1)] for j in range(H-1)]
        self.walldy = [ [ 0,0,0,-1] , [-1,0,-1,-1] ]
        self.walldx = [ [ 0,0,-1,0] , [0,-1,-1,-1] ]
        self.walldir = [ WallDir.V , WallDir.H , WallDir.V , WallDir.H ]

    def set( self, y , x , d ):
        self.table[y][x] = d

    def get( self, y , x ):
        if in_wallarea( y , x ) :
            return self.table[y][x]
        else:
            return WallDir.N

    def check_wallmovable( self , y , x , movedir ):
        return (self.get(y+self.walldy[0][movedir],x+self.walldx[0][movedir]) != self.walldir[movedir]) \
                and (self.get(y+self.walldy[1][movedir],x+self.walldx[1][movedir]) != self.walldir[movedir])

    def reachable(self,wall_pos,walldir,pos,gy):
        self.set(wall_pos[0],wall_pos[1],walldir)
        visited = [[False for i in range(W)] for j in range(H)]
        is_reachable = self.dfs(pos[0],pos[1],gy,visited)
        self.set(wall_pos[0],wall_pos[1],WallDir.N)
        return is_reachable

    def next_wallmoves( self , y , x ):
        wallmoves = []
        for d in range(4):
            if self.check_wallmovable( y , x , d ) and 0 <= y + DY[d] < H and 0 <= x + DX[d] < W :
                wallmoves.append((y+DY[d],x+DX[d]))
        return wallmoves

    def dfs(self,y,x,gy,visited):
        if y == gy:
            return True
    
        visited[y][x] = True

        for (ny,nx) in self.next_wallmoves( y , x ):
            if not visited[ny][nx]:
                if self.dfs(ny,nx,gy,visited):
                    return True
        return False


class Quoridor:
    def __init__(self):
        self.board = Board()
        self.white_pos = ( 0 , int(W / 2) )
        self.black_pos = ( H - 1 , int(W / 2) )
        self.white_wall_num = 10
        self.black_wall_num = 10
        self.is_white_turn = True
        
    def is_over(self):
        if self.white_pos[0] == WHITE_GOAL_Y :
            Color.WHITE
        elif self.black_pos[0] == BLACK_GOAL_Y :
            Color.BLACK
        else:
            Color.N

    def settable( self, y , x , d ):
        if self.board.get(y,x) != WallDir.N :
            return False

        if ( self.is_white_turn and self.white_wall_num == 0 ) or ( not self.is_white_turn and self.black_wall_num == 0 ) : 
            return False

        if not self.board.reachable( (y,x) , d , self.white_pos , WHITE_GOAL_Y ) or not self.board.reachable( (y,x) , d , self.black_pos , BLACK_GOAL_Y ):
            print(" not reachable ")
            return False

        if d == WallDir.H :
            return self.board.get(y,x-1) != WallDir.H and self.board.get(y,x+1) != WallDir.H
        else:
            return self.board.get(y-1,x) != WallDir.V and self.board.get(y+1,x) != WallDir.V


    def movable( self , y , x , player_pos , enemy_pos ):
        if (y,x) in self.next_moves(player_pos,enemy_pos) :
            return True
        else:
            return False

    # 壁，移動両方の可能な手を返す
    def valid_operations( self ):
        operations = []
        if self.is_white_turn :
            operations.extend( self.next_moves( self.white_pos , self.black_pos ) )
        else:
            operations.extend( self.next_moves( self.black_pos , self.white_pos ) )

        for wy in range(H-1):
            for wx in range(W-1):
                if self.settable( wy , wx , WallDir.H ) :
                    operations.append( ( wy , wx , WallDir.H ) )
                if self.settable( wy , wx , WallDir.V ) :
                    operations.append( ( wy , wx , WallDir.V ) )

        return operations


    def next_moves( self , player_pos , enemy_pos  ):
        moves = []
        y = player_pos[0]
        x = player_pos[1]
        for d in range(4):
            ny = y + DY[d]
            nx = x + DX[d]
            if not self.board.check_wallmovable(y,x,d) or ny < 0 or H <= ny or nx < 0 or W <= nx:
                continue

            # 移動先に敵がいたら
            if ny == enemy_pos[0] and nx == enemy_pos[1] :
                    # 飛び越えられたら
                    if self.board.check_wallmovable(ny,nx,d):
                        moves.append((ny+DY[d],nx+DX[d]))
                    else:
                        for d2 in range(4):
                            if self.board.check_wallmovable(ny,nx,d2) and ( ny + DY[d2] , nx + DX[d2] ) != ( y , x ):
                                moves.append((ny+DY[d2],nx+DX[d2]))
            else:
                moves.append((ny,nx))

        print(moves)
        return moves

    # 壁を'|' , '-'，白を'w'，黒を'b'
    def display(self): 
        table = [[' ' for i in range(2*W-1)] for j in range(2*H-1)]
        for y in range(H):
            for x in range(W):
                if (y,x) == self.white_pos:
                    table[2*y][2*x] = 'w'
                elif (y,x) == self.black_pos: 
                    table[2*y][2*x] = 'b'
                if y < H-1 and x < W-1:
                    table[2*y+1][2*x+1] = "*"
                if self.board.get(y,x) == WallDir.V:
                    table[2*y][2*x+1] = '|'
                    table[2*(y+1)][2*x+1] = '|'
                elif self.board.get(y,x) == WallDir.H:
                    table[2*y+1][2*x] = '-'
                    table[2*y+1][2*(x+1)] = '-'
        for row in table:
            print("".join(row))


    def operate( self , op ):
        y = op[0] 
        x = op[1]
        if len(op) == 3:        # 壁を置く操作
            d = op[2]
            if self.settable( y , x , d ):
                self.board.set(y,x,d)
                if self.is_white_turn :
                    self.white_wall_num = self.white_wall_num - 1
                else:
                    self.black_wall_num = self.black_wall_num - 1

                self.is_white_turn = not self.is_white_turn
                return True
            else:
                return False
        else:                   # 駒の移動
            if self.is_white_turn :
                if self.movable( y,x,self.white_pos , self.black_pos ):
                    self.white_pos = ( y , x )
                    self.is_white_turn = not self.is_white_turn
                    return True
                else:
                    return False
            else:
                if self.movable( y,x,self.black_pos , self.white_pos ):
                    self.black_pos = ( y , x )
                    self.is_white_turn = not self.is_white_turn
                    return True
                else:
                    return False

