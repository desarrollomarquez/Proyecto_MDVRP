EQUATIONS
OBJ
X_ij_rule(J) 'Cada zona j debe ser asignado a un fabricante'
CA_rule(I,J) 'Capacidad del conjunto de fabricas '
X_ij_X_ji_rule 'Conservacion de Flujos'
//X_ij__rule 'Garantiza que cada fabrica atienda almenos una unica ruta'
X_u_rule(U,I,J) 'Garantiza asignacion de zona j si transita por las fabricas i'
U_u_rule(J,U) 'Garantiza la eliminacion de SubTours';


OBJ..                                             Z =E= SUM(M(I,J), C(I,J)*X(I,J)) ;
//X_ij_rule ..                                        SUM(M(I,J),X(I,J))  =e=  1 ;
X_ij_rule(J) ..                                   SUM(I$(M(I,J)),X(I,J))  =e=  1 ;
CA_rule(I,J) ..                                SUM(M(I,J),DZ(J)*X(I,J))  =l= CA(I) ;
X_ij_X_ji_rule ..                SUM(M(I,J),X(I,J)) - SUM(MM(J,I),XX(J,I))  =e=  0 ;
//X_ij__rule ..                                             SUM(M(I,J),X(I,J))  =l=  1 ;
X_u_rule(U,I,J) ..                  SUM(M(I,J),UX(I,U) + XU(U,J)) - X(I,J)   =l=  1 ;
U_u_rule(MU(J,U)) ..                UJ(J) - UU(U) + CARD(J)*XXX(J,U) =l= CARD(J) - 1 ;


MODEL LOCALIZ /ALL/;
SOLVE LOCALIZ MINIZING Z USING MIP ;
DISPLAY MU,CA_rule.l;


//Ajustes del modelo inicial....