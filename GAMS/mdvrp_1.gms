$TITLE PROBLEMA DE LOCALIZACIONOPTION LIMROW=100;OPTION LIMCOL =100;OPTIONS OPTCR = 0.01;
SET
I       FABRICAS /BARNA,BILBAO,MADRID,VALENC/
J       ZONAS /CATAL, NORTE, NOROE, LEVAN, CENTR, SUR/

TABLE C(I,J)    COSTES VARIABLES DE DISTRIBUCION Y TRANSPORTE
              CATAL     NORTE     NOROE     LEVAN     CENTR     SUR
BARNA         0.010     0.062     0.0110     0.035    0.062     0.0100
BILBAO        0.062     0.010     0.063      0.063    0.040     0.086
MADRID        0.062     0.040     0.060      0.035    0.07      0.054
VALENC        0.035     0.063     0.096      0.010    0.035     0.067;


SET M(I,J) MATRIX DE COSTOS;
M(I,J)$(C(I,J)> 0.003)= YES ;


PARAMETER F(I) COSTES FIJOS
/BARNA   100000
 BILBAO  100000
 MADRID   80000
 VALENC  100000/;

PARAMETER D(J) DEMANDA DE LA ZONAS
/CATAL   480
 NORTE   356
 NOROE   251
 LEVAN   349
 CENTR   598
 SUR     326/;

PARAMETER CA(I) CAPACIDAD DE LAS FABRICAS
/BARNA   1000
 BILBAO  1000
 MADRID  1000
 VALENC  1000/;

PARAMETER CI(I) CAPACIDAD INICIAL
/BARNA   500
 BILBAO    0
 MADRID  700
 VALENC    0/;

VARIABLES
FO
X(I,J)
Y(I);

BINARY VARIABLE
X
Y;



EQUATIONS
OBJ;


OBJ..   FO =E= SUM((I,J), C(I,J)*X(I,J));


MODEL LOCALIZ /ALL/;
SOLVE LOCALIZ USING MIP MINIZING FO;
DISPLAY X.L;
