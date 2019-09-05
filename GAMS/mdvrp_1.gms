$eolCom //

OPTION optCr = 0, limRow = 0, limCol = 0, solPrint = OFF, LP = CPLEX ;


SET
I       FABRICAS /BARNA,BILBAO,MADRID,VALENC/
J       ZONAS /CATAL, NORTE, NOROE, LEVAN, CENTR, SUR/
U       ZONAS_U /CATAL, NORTE, NOROE, LEVAN, CENTR, SUR/


TABLE D(I,J)    DISTANCES VARIABLES DE DISTRIBUCION Y TRANSPORTE
              CATAL     NORTE     NOROE     LEVAN     CENTR     SUR
BARNA         10        62        110        35        62       100
BILBAO        62        10         63        63        40        86
MADRID        62        40         60        35        70        54
VALENC        35        63         96        10        35        67;

TABLE DD(J,I)    DISTANCES VARIABLES DE DISTRIBUCION Y TRANSPORTE - TRASPUESTA
              BARNA    BILBAO     MADRID    VALENC
CATAL          10        62        62        35
NORTE          62        10        40        63
NOROE          110       63        60        96
LEVAN          35        63        35        10
CENTR          62        40        70        35
SUR            100       86        54        67;

TABLE JU(J,U)    DISTANCES VARIABLES DE DISTRIBUCION Y TRANSPORTE ENTRE ZONAS
              CATAL     NORTE     NOROE     LEVAN     CENTR     SUR
CATAL           0        40        35        35         45       32
NORTE          40         0        30        45         25      100
NOROE          35        30         0        65         50       45
LEVAN          35        45        65         0         28       70
CENTR          45        25        50        28          0       60
SUR            32       100        45        70         60        0;

PARAMETER CA(I) CAPACIDAD DE LAS FABRICAS
/BARNA   1000
 BILBAO  1000
 MADRID  1000
 VALENC  1000/;

PARAMETER DZ(J) DEMANDA DE LA ZONAS
/CATAL   480
 NORTE   356
 NOROE   251
 LEVAN   349
 CENTR   598
 SUR     326/;

SET M(I,J) MATRIX DE DISTANCIAS;
M(I,J)$(D(I,J) > 0.0 )   = YES ;


SET MM(J,I) MATRIX DE DISTANCIAS TRASPUESTA;
MM(J,I)$(DD(J,I) > 0.0 )   = YES ;



SET MU(J,U) MATRIX DE DISTANCIAS PARA SUBTOURES;
MU(J,U) = ORD(J) and ORD(U);


SCALAR CVK  COSTO DE UN VEHICULO POR KILOMETRO
/2/ ;

PARAMETER
C(I,J);
C(I,J) = D(I,J)*CVK;

FREE VARIABLES
Z
UJ(J)
UU(U);

BINARY VARIABLE
X(I,J)
XX(J,I)
XXX(J,U)
UX(I,U)
XU(U,J)
AD(I,J);


EQUATIONS
OBJ
X_ij_rule 'Cada zona j debe ser asignado a un fabricante'
CA_rule(I,J) 'Capacidad del conjunto de fabricas '
X_ij_X_ji_rule 'Conservacion de Flujos'
X_ij__rule 'Garantiza que cada fabrica atienda almenos una unica ruta'
X_u_rule(U,I,J) 'Garantiza asignacion de zona j si transita por las fabricas i'
U_u_rule(J,U) 'Garantiza la eliminacion de SubTours';;


OBJ..                                                Z =E= SUM(M(I,J), C(I,J)*X(I,J));
X_ij_rule ..                                              SUM(M(I,J),X(I,J))  =e=  1 ;
CA_rule(I,J) ..                                  SUM(M(I,J),DZ(J)*AD(I,J))  =l= CA(I);
X_ij_X_ji_rule ..                  SUM(M(I,J),X(I,J)) - SUM(MM(J,I),XX(J,I))  =e=  0 ;
X_ij__rule ..                                             SUM(M(I,J),X(I,J))  =l=  1 ;
X_u_rule(U,I,J) ..                  SUM(M(I,J),UX(I,U) + XU(U,J)) - AD(I,J)   =l=  1 ;
U_u_rule(J,U) ..                   UJ(J) - UU(U) + CARD(J)*XXX(J,U) =l= CARD(J) - 1;





MODEL LOCALIZ /ALL/;
SOLVE LOCALIZ MINIZING Z USING MIP ;
DISPLAY XXX.l,  UJ.l, UU.l;
