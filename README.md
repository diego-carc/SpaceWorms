# Análisis transcriptómico del efecto de la microgravedad en C. elegans.

### Diego Carmona Campos y Ethan Marcos Galindo Raya

## Introducción

La exploración espacial es una de las empresas más ambiciosas de la humanidad. Dentro de los objetivos a largo plazo de las misiones tripuladas está el generar el conocimiento suficiente para que el ser humano llegue a otros planetas, lo que requiere un acercamiento progresivo al espacio, como la misión Artemis de la NASA. Sin embargo, actualmente existen limitaciones que nos hacen ser modestos con nuestras expectativas para cumplir estos objetivos. Más allá de las dificultades tecnológicas, se han observado efectos negativos en la salud de los astronautas después de distintos periodos en el espacio. Entre ellos, se ha reportado atrofia muscular, reducción en la densidad ósea, cambio en el sistema cardiovascular, así como un debilitamiento del sistema inmunológico.

Para tener una comprensión sistemática de los mecanismos detrás de estos efectos es de gran importancia hacer análisis ómicos que nos permitan evaluar el estado fisiológico de las células expuestas a microgravedad. Por lo tanto, reutilizaremos datos de expresión disponibles en la base de datos de GEO para analizar los cambios a nivel transcriptómico que se presentan cuando las organismos están en vuelo espacial.

En particular, nos centraremos en el análisis de datos disponibles para el organismo modelo Caenorhabditis elegans, ya que es altamente relevante en el estudio de las neurociencias, el funcionamiento muscular así como la biología del desarrollo . Además, la presencia de genes ortólogos con seres humanos puede dar indicios de qué es lo que sucede realmente en los astronautas después de una misión espacial, impulsando el interés por conocer a detalle el transcriptoma de los gusanos espaciales.

## Método/Diseño/Análisis

### Colección de datos

Se usó el script *get_gse_ids.py* con el txid 6239

```python
nohup python ../../bin/get_geo_ids.py -e diegocar@lcg.unam.mx \
-a 34677fdcfd2f0659a7f9ee05ab6e44704f09 -t 6239 -o $PWD/cElegansSpaceGSEsIds.txt \
--format &
```

Usamos el script *get_geo_metadata.py* para obtener metadatos relacionados con los GSEs obtenidos en la consulta.

```python
nohup python ../bin/get_geo_metadata.py -i ../data/cElegansSpaceGSEsIds.txt \
-o $PWD/cElegansGEOMetadata.tsv &
```

Usaremos los metadatos para seleccionar los datos que sean relevantes para el estudio y los clasificaremos de acuerdo a la condición a la que corresponden.

Descargaremos los datos y los procesaremos con un script para hacer normalización por cuantiles

### Análisis de Datos

Compararemos los perfiles de expresión en cada condición e identificaremos genes o grupos de genes con más cambio

Haremos un análisis de la anotación biológica haciendo un mapeo de los genes con su Gene Ontology


## Pregunta/Hipótesis/Objetivo

Con este trabajo nos interesamos en conocer cuáles son los efectos de la microgravedad y el vuelo espacial en la expresión génica. 

Nosotros creemos que habrá una gran variedad de funciones afectadas por la microgravedad, en particular esperamos encontrar cambios en genes que regulen las dinámicas del citoesqueleto.

Con este trabajo pretendemos generar conocimiento acerca de los sistemas afectados por el vuelo espacial usando como modelo a C. elegans.

## Resultados
Reportaremos nuestros avances en [nuestro repositorio de GitHub](https://github.com/diego-carc/SpaceWorms.git)

## Conclusión