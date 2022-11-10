# Biggest Circle Inscribed In A Polygon

_A year project carried during my last year of "Classe préparatoire" meant to deal with Mathematics and Computer Science related topics._

## First method : based on the approximation of poles of inaccessibility

The method follows [this paper](https://arxiv.org/ftp/arxiv/papers/1212/1212.3193.pdf) which refers to [this paper](https://www.researchgate.net/publication/232984998_Poles_of_inaccessibility_A_calculation_algorithm_for_the_remotest_places_on_Earth).

Example of pole of inaccessibility    |  The method of the paper
:-------------------------:|:-------------------------:
![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/poles_example.png?raw=true)  |  ![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/poles1.png?raw=true)

## Second method : using the medial axis approximation of a polygon using Voronoi diagrams

The method follows [this paper](https://link.springer.com/article/10.1007/BF01840357) by Steven Fortune.

An example of our Fortune algorithm | A first application to a polygon with an interior | A second application to a polygon with an interior
:-------------------------:|:-------------------------:|:-------------------------:
![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/fortune1.png?raw=true) | ![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/app1.png?raw=true) | ![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/app2.png?raw=true)

An approximation of the medial axis 1 | An approximation of the medial axis 2 
:-------------------------:|:-------------------------:
![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/medial1.png?raw=true) | ![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/medial2.png?raw=true) 


## Final step : to apply theses methods to a real map (Bretagne)

The map used | The algorithm applied in every county| A zoom
:-------------------------:|:-------------------------:|:-------------------------:
![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/bretagne1.png?raw=true) | ![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/bretagne2.png?raw=true) | ![](https://github.com/Minifixio/TIPE_2021/blob/master/assets/bretagne3.png?raw=true)


