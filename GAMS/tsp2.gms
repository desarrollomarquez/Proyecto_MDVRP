$ title Problema de vendedor itinerante: uno (TSP1, SEQ = 177)

$ onText
Este es el primer problema en una serie de vendedores ambulantes.
problemas. En este problema, primero resolvemos una tarea
problema como una relajación del TSP. Subtours de esta solución
son detectados e impresos. Los subtours se eliminan a través de
cortes (restricciones que eliminan la solución con subtours).

Nota: tratamos aquí con un TSP asimétrico. Si simétrico
      se pueden agregar 2 cortes en cada ciclo: adelante y
      hacia atrás.

Se puede encontrar información adicional en:

http://www.gams.com/modlib/adddocs/tsp1doc.htm


Kalvelagen, E, Edificio Modelo con GAMS. próximo

de Wetering, AV, comunicación privada.

Palabras clave: programación lineal entera mixta, problema de vendedor ambulante, iterativo
          eliminación de subtour, generación de corte
$ offText

$ eolCom //

$ include br17.inc

* Para este algoritmo simple, el problema es demasiado difícil
* entonces consideramos solo las primeras 6 ciudades.
Conjunto i (ii) / i1 * i6 /;

* opciones. Asegúrese de que el solucionador MIP encuentre óptimos globales.
opción optCr = 0;

Asignación de modelo / objetivo, filas, colsum /;

resolver asignar usando mip minimizando z;

* buscar y mostrar tours
Establezca t 'tours' / t1 * t17 /;
abortar $ (tarjeta (t) <tarjeta (i)) "El conjunto t es posiblemente demasiado pequeño";

Parámetro tour (i, j, t) 'subtours';

Conjunto Singleton
   from (i) 'contiene siempre un elemento: la ciudad from'
   next (j) 'contiene siempre un elemento: la ciudad'
   tt (t) 'contiene siempre un elemento: el subtour actual';

Establecer visitado (i) 'marcar si una ciudad ya ha sido visitada';

* inicializar
de (i) $ (ord (i) = 1) = sí; // activa el primer elemento
tt (t) $ (ord (t) = 1) = sí; // activa el primer elemento

bucle (i,
   siguiente (j) $ (xl (de, j)> 0.5) = sí; // comprobar xl (de, j) = 1 sería peligroso
   recorrido (desde, siguiente, tt) = sí; // almacenar en la mesa
   visitado (desde) = sí; // marca la ciudad 'desde' como visitada
   de (j) = siguiente (j);
   if (sum (visitado (siguiente), 1)> 0, // si ya lo visitó ...
      tt (t) = tt (t-1);
      loop (k $ (no visitado (k)), // encuentra el punto de partida del nuevo subtour
         de (k) = sí;
      );
   );
);

recorrido de exhibición;

* eliminación de subtour agregando cortes
* la lógica para detectar si hay subtours es similar
* al código de arriba
Establecer cc / c1 * c100 /; // permitimos hasta 100 cortes

Alias ​​(cc, ccc);

Conjunto
   curcut (cc) 'corte actual siempre un elemento'
   allcuts (cc) 'cortes totales';

Parámetro cutcoeff (cc, i, j);

Corte de ecuación (cc) 'cortes dinámicos';

cut (allcuts) .. sum ((i, j), cutcoeff (allcuts, i, j) * x (i, j)) = l = tarjeta (i) - 1;

Modelo tspcut / object, rowsum, colsum, cut /;

curcut (cc) $ (ord (cc) = 1) = yes;

Escalar ok;

bucle (ccc,
   de (i) = ord (i) = 1; // inicializar desde a la primera ciudad
   visitado (i) = no;
   ok = 1;
   loop (i $ ((ord (i) <card (i)) y ok), // la última ciudad puede ser ignorada
      siguiente (j) = xl (de, j)> 0.5; // encuentra la siguiente ciudad
      visitado (desde) = sí;
      de (j) = siguiente (j);
      ok $ sum (visitado (siguiente), 1) = 0; // hemos detectado un subtour
   );
   romper $ (ok = 1); // hecho: sin subtours

   // introduce corte
   cutcoeff (curcut, i, j) $ (xl (i, j)> 0.5) = 1;
   // el siguiente es necesario en el caso general pero no para TSP
   // cutcoeff (curcut, i, j) $ (xl (i, j) <0.5) = -1;
   allcuts (curcut) = sí; // incluye este corte en el set
   curcut (cc) = curcut (cc-1); // obtener el siguiente elemento
   resuelva tspcut usando mip minimizando z;
   tspcut.solPrint =% solPrint.Quiet%;
);

* solución de impresión en el orden correcto
Establezca xtour 'tour ordenado';
de (i) = ord (i) = 1; // inicializar desde a la primera ciudad
visitado (i) = no;
ok = 1;

bucle (t $ ok,
   siguiente (j) = xl (de, j)> 0.5; // encuentra la siguiente ciudad
   xtour (t, desde, siguiente) = sí;
   visitado (desde) = sí;
   de (j) = siguiente (j);
   ok $ sum (visitado (siguiente), 1) = 0; // hemos detectado un subtour
);

opción xtour: 0: 0: 1;
mostrar xtour, xl;

abortar $ (card (allcuts) = card (cc)) "Se necesitan demasiados cortes";