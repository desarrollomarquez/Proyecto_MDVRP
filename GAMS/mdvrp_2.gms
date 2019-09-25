$eolCom //

OPTION optCr = 0, limRow = 0, limCol = 0, solPrint = ON, LP = CPLEX ;

SET
I       FABRICAS /BARNA,BILBAO,MADRID,VALENC/
J       ZONAS /CATAL, NORTE, NOROE, LEVAN, CENTR, SUR/
K       VEHICULOS /CAMION1,CAMION2,CAMION3,CAMION4/;
ALIAS (J,U,H);

** J Y U LETRAS PARA HACER REFERENCIA A LOS MISMOS ELEMENTOS..

TABLE D(I,J)    DISTANCES VARIABLES DE DISTRIBUCION Y TRANSPORTE
              CATAL     NORTE     NOROE     LEVAN     CENTR     SUR
BARNA         10        62        110        35        62       100
BILBAO        62        10         63        63        40        86
MADRID        62        40         60        35        70        54
VALENC        35        63         96        10        35        67;


TABLE JU(J,U)    DISTANCES VARIABLES DE DISTRIBUCION Y TRANSPORTE ENTRE ZONAS
              CATAL     NORTE     NOROE     LEVAN     CENTR     SUR
CATAL           0        40        35        35         45       32
NORTE          40         0        30        45         25      100
NOROE          35        30         0        65         50       45
LEVAN          35        55        65         0         28       70
CENTR          45        30        70        28          0       60
SUR            32        90        45        70         60        0;

PARAMETER CA(I) CAPACIDAD DE LAS FABRICAS
/BARNA   500
 BILBAO  500
 MADRID  500
 VALENC  500/;

PARAMETER DZ(J) DEMANDA DE LA ZONAS
/CATAL    600
 NORTE    700
 NOROE    500
 LEVAN    800
 CENTR   1000
 SUR      600/;

PARAMETER CV(K) CAPACIDAD DE VEHICULOS
/CAMION1    400
 CAMION2    400
 CAMION3    400
 CAMION4    400/;

SET M(I,J) MATRIX DE DISTANCIAS;
M(I,J)$(D(I,J) > 0.0 )   = YES ;

SET MU(J,U) MATRIX DE DISTANCIAS PARA SUBTOURES;
MU(J,U)$(JU(J,U) > 0.0 )   = YES ;


SCALAR CVK  COSTO DE UN VEHICULO POR KILOMETRO
/70/ ;

PARAMETER
C(I,J);
C(I,J)  = D(I,J)*CVK;

PARAMETER
CO(J,U);
CO(J,U) = JU(J,U)*CVK;

VARIABLES
F(I,J,K) 1 si la ruta K parte del deposito I hacia el sitio J 0 en caso contrario
X(J,U,K) 1 si la ruta K parte del deposito J hacia el sitio U 0 en caso contrario
L(J,I,K) 1 si la ruta K parte del deposito I hacia el sitio J 0 en caso contrario
Z(I,J)   1 Si la zona J es atendida por el deposito I 0 en caso contrario
S(H,K) Variable de Subtoures
FO Funcion Objetivo

BINARY  VARIABLES F,X,L,Z;
INTEGER VARIABLE S;

EQUATIONS

Fobj Funcion Objetivo
Cobertura
Capacidad
;


Fobj ..               FO =e= SUM((I,J,K),C(I,J)*F(I,J,K)) + SUM((J,U,K),CO(J,U)*X(J,U,K)) + SUM((I,J,K),C(I,J)*L(J,I,K));
Cobertura(J) ..       SUM((I,K),F(I,J,K)) + SUM((U,K),X(J,U,K)) + SUM((I,K),L(J,I,K)) =g= 1;
Capacidad(K) ..       SUM(J,DZ(J))

