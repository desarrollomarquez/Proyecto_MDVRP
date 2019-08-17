$eolCom //

option optCr = 0, limRow = 0, limCol = 0, solPrint = off;

Sets
i 'depositos'
       / d1 'Pud Thai Vs Pho', d2 'Hungry Jack s', d3 'The Comics Lounge', d4 'Fat Face Food', d5 'Saddles@HQ',
         d6 'DepMcDonalds', d7 'Eat & Grab', d8 'Coffee Hq', d9 'Australian Education Academy Cafe', d10 'Subway Vic Harbour' /,

j 'clientes'
       / c1 'The Coffee Cup', c2 'Cafe Max', c3 'Saquella Caffe', c4 'Ciao Pizza Napoli', c5 'Cafe Malone', c6 'Chambers Fine Foods',
         c7 'Becco', c8 'The Gourmet Gulp', c9 'Cafe Q', c10 'Lady Jade Tea House', c11 'Borlotti Restaurant', c12 'Lures Gourmet Sandwich Bar',
         c13 'Hermes Fine Foods', c14 'McDonalds', c15 'Menzies Tavern', c16 'Cafe Exchange', c17 'Cafe Cento Venti', c18 'Garden Plaza Cafe',
         c19 'Mediterranean Deli', c20 'Nauru House Cafe', c21 'Dr Martins Tavern', c22 'Janils Cafe', c23 'Edoya Restaurant', c24 'Taco Bills Restaurant',
         c25 'Centro Citta Restaurant', c26 'Bistro 1', c27 'Pizza Napoli', c28 'Stamford Plaza Hotel', c29 'Daniels Charcoal Grill' / ,

k 'vehiculos'
       / v1 'TRUCK-SHORT1', v2 'TRUCK-SHORT2', v3 'TRUCK-SHORT3', v4 'TRUCK-SHORT4', v5 'TRUCK-SHORT5',
         v6 'TRUCK-SHORT6', v7 'TRUCK-SHORT7', v8 'TRUCK-SHORT8', v9 'TRUCK-SHORT9' /;


Table d(i,j)   'distancia desde los depositos i a los clientes j'
                 c1                c2                    c3                c4                  c5                  c6                  c7                   c8                  c9                  c10                 c11                 c12                 c13                 c14                 c15                 c16                 c17                 c18                 c19                 c20                 c21                 c22                 c23                 c24                 c25                 c26                 c27                 c28                 c29
d1        0.0130355057        0.0128974266        0.0128333254        0.0126201448        0.0124601290        0.0122777125        0.0217397334        0.0072929223        0.0072929223        0.0072929223        0.0072929223        0.0076025691        0.0069453512        0.0078906746        0.0072860067        0.0067619469        0.0190482464        0.0190482464        0.0204107244        0.0204107244        0.0201416823        0.0194920637        0.0187114699        0.0187114699        0.0194478182        0.0195957691        0.0187382624        0.0195297230        0.0161624307
d2        0.0158213522        0.0154748419        0.0153173418        0.0153078935        0.0152826815        0.0155025683        0.0186465046        0.0136708598        0.0136708598        0.0136708598        0.0136708598        0.0141067672        0.0126958117        0.0124109338        0.0128207075        0.0130325219        0.0156694893        0.0156694893        0.0165469974        0.0165469974        0.0161759114        0.0156692283        0.0163112108        0.0163112108        0.0167149526        0.0166126808        0.0159758338        0.0160851884        0.0194773031
d3        0.0140370998        0.0143585373        0.0145019527        0.0143365668        0.0142395944        0.0138232782        0.0221764956        0.0141398151        0.0141398151        0.0141398151        0.0141398151        0.0137000426        0.0151149065        0.0154399583        0.0149849145        0.0147967883        0.0216093029        0.0216093029        0.0226525233        0.0226525233        0.0226812600        0.0222847961        0.0203146033        0.0203146033        0.0209237177        0.0212814177        0.0207709039        0.0218343387        0.0123625160
d4        0.0204424016        0.0207346526        0.0208643294        0.0206689616        0.0205478283        0.0201080969        0.0290497589        0.0192610730        0.0192610730        0.0192610730        0.0192610730        0.0188744840        0.0202040269        0.0207872345        0.0201622008        0.0198125341        0.0283348822        0.0283348822        0.0294315755        0.0294315755        0.0294392475        0.0290118782        0.0270752216        0.0270752216        0.0277118421        0.0280645815        0.0275126287        0.0285871553        0.0191797591
d5        0.0528188373        0.0531274486        0.0532643397        0.0530821957        0.0529708485        0.0525386944        0.0605978229        0.0516271289        0.0516271289        0.0516271289        0.0516271289        0.0512639487        0.0525417694        0.0532021279        0.0525320299        0.0521300868        0.0603622037        0.0603622037        0.0613294418        0.0613294418        0.0613902134        0.0610331497        0.0590340524        0.0590340524        0.0595975721        0.0599610204        0.0595107057        0.0605550056        0.0510709649
d6        0.0116076722        0.0114460961        0.0113806818        0.0116360951        0.0118102425        0.0122389887        0.0026178854        0.0163214322        0.0163214322        0.0163214322        0.0163214322        0.0163341636        0.0160537304        0.0149509662        0.0157792333        0.0164320693        0.0033751882        0.0033751882        0.0020061070        0.0020061070        0.0021844581        0.0028195554        0.0043138438        0.0043138438        0.0035980335        0.0032709951        0.0039929376        0.0029524661        0.0120870019
d7        0.0192439865        0.0190299346        0.0189388552        0.0191806407        0.0193417186        0.0197885011        0.0104580189        0.0232102101        0.0232102101        0.0232102101        0.0232102101        0.0233167548        0.0227425911        0.0216621293        0.0225222079        0.0231651243        0.0109733585        0.0109733585        0.0098184704        0.0098184704        0.0098273908        0.0103016993        0.0121812755        0.0121812755        0.0115371484        0.0111841422        0.0117637465        0.0106816488        0.0200903608
d8        0.0053422028        0.0054314166        0.0054836718        0.0057076139        0.0058759181        0.0061223078        0.0059449652        0.0111579903        0.0111579903        0.0111579903        0.0111579903        0.0109591585        0.0113685658        0.0104386658        0.0110294498        0.0115865400        0.0058623635        0.0058623635        0.0066153461        0.0066153461        0.0067263930        0.0064862434        0.0044765784        0.0044765784        0.0049067933        0.0052722711        0.0050025153        0.0059388599        0.0039955454
d9        0.0336821757        0.0340107564        0.0341571840        0.0339990224        0.0339064805        0.0334940391        0.0409349257        0.0333645856        0.0333645856        0.0333645856        0.0333645856        0.0329568069        0.0343255309        0.0348207225        0.0342546190        0.0339528399        0.0408698347        0.0408698347        0.0417717477        0.0417717477        0.0418546513        0.0415331656        0.0395179072        0.0395179072        0.0400460846        0.0404114475        0.0400096826        0.0410324459        0.0316006936
d10       0.0191947719        0.0192311570        0.0192448252        0.0189861625        0.0188032911        0.0184415499        0.0291155393        0.0139415650        0.0139415650        0.0139415650        0.0139415650        0.0139358009        0.0142802791        0.0153780588        0.0145276343        0.0138753491        0.0268907806        0.0268907806        0.0282744627        0.0282744627        0.0280784253        0.0274526447        0.0261914739        0.0261914739        0.0269634097        0.0271984738        0.0263703520        0.0273340310        0.0209915514     ;




Parameters
       w(i) capacidad del deposito
            /    Pud Thai Vs Pho                    1400
                 Hungry Jack s                       750
                 The Comics Lounge                   400
                 Fat Face Food                       550
                 Saddles@HQ                          800
                 DepMcDonalds                       1100
                 Eat & Grab                          700
                 Coffee Hq                           600
                 Australian Education Academy Cafe  1000
                 Subway Vic Harbour                 1100 /

       d(j) demanda del cliente
            /     The Coffee Cup             1100
                  Cafe Max                    800
                  Saquella Caffe              900
                  Ciao Pizza Napoli           560
                  Cafe Malone                 490
                  Chambers Fine Foods         550
                  Becco                       370
                  The Gourmet Gulp            600
                  Cafe Q                      180
                  Lady Jade Tea House         240
                  Borlotti Restaurant         760
                  Lures Gourmet Sandwich Bar  540
                  Hermes Fine Foods           220
                  McDonalds                  1000
                  Menzies Tavern              120
                  Cafe Exchange               330
                  Cafe Cento Venti            800
                  Garden Plaza Cafe           850
                  Mediterranean Deli          440
                  Nauru House Cafe            180
                  Dr Martins Tavern           180
                  Janils Cafe                 100
                  Edoya Restaurant            150
                  Taco Bills Restaurant       700
                  Centro Citta Restaurant     320
                  Bistro 1                     80
                  Pizza Napoli                 70
                  Stamford Plaza Hotel        100
                  Daniels Charcoal Grill      260 /

       Q(k) capacidad del vehiculo;
             /    TRUCK-SHORT1   1500
                  TRUCK-SHORT2   1500
                  TRUCK-SHORT3   1500
                  TRUCK-SHORT4   1500
                  TRUCK-SHORT5   1500
                  TRUCK-SHORT6   1500
                  TRUCK-SHORT7   1500
                  TRUCK-SHORT8   1500
                  TRUCK-SHORT9   1500 /


Scalar cv  costo de un vehiculo por kilometro  /0.03/ ;

Parameter
       c(i,j) costo de transporte por pedido;
       c(i,j) = cv * d(i,j);

Free Variable
       z;

Binary Variable
       x(i,j,k);


Equation obj
         X_ijk 'Cada cliente j debe ser asignado a un vehiculo k'
         Q_k_rule 'Capacidad del conjunto de vehiculos K';

obj ..    z =e= sum((i,j,k),c(i,j)*x(i,j,k));

X_ijk ..        sum((i,j,k),x(i,j,k))  =e=  1 ;

Model mdvrp / obj /;

solve mdvrp minimizing z using mip;


