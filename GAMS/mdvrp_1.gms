$eolCom //

OPTION optCr = 0, limRow = 0, limCol = 0, solPrint = on, LP = CPLEX ;


SET
I       FABRICAS /BARNA,BILBAO,MADRID,VALENC/
J       ZONAS /CATAL, NORTE, NOROE, LEVAN, CENTR, SUR/

TABLE D(I,J)    DISTANCES VARIABLES DE DISTRIBUCION Y TRANSPORTE
              CATAL     NORTE     NOROE     LEVAN     CENTR     SUR
BARNA         10        62        110        35        62       100
BILBAO        62        10         63        63        40        86
MADRID        62        40         60        35        70        54
VALENC        35        63         96        10        35        67;

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

SCALAR CVK  COSTO DE UN VEHICULO POR KILOMETRO
/0.03/ ;

PARAMETER
C(I,J);
C(I,J) = D(I,J)*CVK;

FREE VARIABLES
Z;

BINARY VARIABLE
X(I,J);


EQUATIONS
OBJ
X_ij_rule 'Cada zona j debe ser asignado a un fabricante'
Q_rule(I,J) 'Capacidad del conjunto de fabricas ';


OBJ..                                            Z =E= SUM(M(I,J), C(I,J)*X(I,J));
X_ij_rule ..                                          SUM(M(I,J),X(I,J))  =e=  1 ;
Q_rule(I,J) ..                                   DZ(J)*SUM(M(I,J),X(I,J))  =l= CA(I);

MODEL LOCALIZ /ALL/;
SOLVE LOCALIZ MINIZING Z USING MIP ;
DISPLAY M;
