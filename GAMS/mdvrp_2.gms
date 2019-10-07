$eolCom //

OPTION optCr = 0, limRow = 0, limCol = 0, solPrint = OFF, LP = CPLEX ;

SET
N       NODOSDEPOCLIENTES /BARNA, BILBAO, MADRID, VALENC, CATAL, NORTE, NOROE, LEVAN, CENTR, SUR/
K       VEHICULOS         /CAMION1, CAMION2, CAMION3, CAMION4/
d(N)    depositos /BARNA, BILBAO, MADRID, VALENC/
z(N)    zonas /CATAL, NORTE, NOROE, LEVAN, CENTR, SUR/ ;

alias(N,I,J,L);

TABLE dist(I,J)    DISTANCIAS VARIABLES DE DISTRIBUCION Y TRANSPORTE
                 BARNA   BILBAO  MADRID  VALENC         CATAL    NORTE   NOROE   LEVAN   CENTR   SUR
BARNA            0       0       0       0              10       62      110     35      62     100
BILBAO           0       0       0       0              62       10       63     63      40      86
MADRID           0       0       0       0              62       40       60     35      70      54
VALENC           0       0       0       0              35       63       96     10      35      67
CATAL           10      62      62      35               0       40       35     35      45      32
NORTE           62      10      40      63              40        0       30     45      25     100
NOROE          110      63      60      96              35       30        0     65      50      45
LEVAN           35      63      35      10              35       45       65      0      28      70
CENTR           62      40      70      35              45       25       50     28       0      60
SUR            100      86      54      67              32      100       45     70      60       0;


PARAMETER CD(d) CAPACIDAD DE LOS DEPOSITOS
/BARNA   10000
 BILBAO  10000
 MADRID  10000
 VALENC  10000/;

PARAMETER DC(z) DEMANDA DE LOS CLIENTES
/CATAL    600
 NORTE    700
 NOROE    500
 LEVAN    800
 CENTR    1000
 SUR      600  /;

PARAMETER CV(K) CAPACIDAD DE VEHICULOS
/CAMION1    6000
 CAMION2    6000
 CAMION3    6000
 CAMION4    6000/;

SCALAR CVK  COSTO DE UN VEHICULO POR KILOMETRO
/70/ ;

PARAMETER
C(I,J);
C(I,J) = Dist(I,J)*CVK;

variables

x(i,j,k) 1 si el nodo i precede al nodo j en la ruta k
y(d,z) 1 si el deposito d atiende la zona z
U(l) subtoures en la ruta k
costototal valor de la fo;

binary variables x, y;

integer variable u ;

x.fx(i,j,k)$(dist(i,j)=0)=0 ;

equations

fo funcion objetivo
cobertura cobertura de cada zona
capacidadvehiculos capacidad de los vehiculos
flujo ecuaciones de flujo
vehiculoruta  un vehiculo en una sola ruta
capacidaddepositos no se excede la capacidad de los depositos
relacion relacion entre variables
subtoures(i,j,k) eliminacion de subtoures

;

fo .. costototal =e= sum((i,j,k),C(i,j)*X(i,j,k)) ;
cobertura(z) .. sum((n,k),X(n,z,k)) =e= 1 ;
capacidadvehiculos(k) ..  sum((n,z),dc(z)*x(n,z,k)) =l= CV(k) ;
flujo(n,k) .. sum(j,X(j,n,k)) =e= sum(j,X(n,j,k)) ;
vehiculoruta(k) .. sum((d,z),x(d,z,k)) =l= 1 ;
capacidaddepositos(d) ..  sum(z,dc(z)*y(d,z)) =l=  CD(d) ;
relacion(d,z,k) .. -y(d,z) + sum(n,x(n,z,k)+x(z,n,k)) =l= 1 ;
subtoures(i,j,k) .. U(i)- U(j) + 4*x(i,j,k) =l= 3;

model mdvrp /all/;
solve mdvrp minimizing costototal using mip
display L;



