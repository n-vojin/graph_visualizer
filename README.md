# graph_visualizer

Project for SOK subject

Contributors:

- Nemanja Vojinović R2 34/2023



Aplikacija za učitavanje data sourca, njegovo parsiranje i vizuelizaciju u vidu grafa sa čvorovima i vezama.

### Instalacija

##### 1. Nakon podešavanja virtuelnog okruženja potrebno je instalirati requiremente:

pip install Django

pip install setuptools

pip install jinja2

pip install jsonpickle



##### 2. Zatim u terminalu pokrenuti skripte po sledećem redosledu

1. RemoveEggs.sh   -briše sve installirane projekt plugine iz projekta

2. Install script.ps1   -instalira sve projekt plugine

3. Server start script.ps1   -pravi migracije i pokreće server



Moguće je ne instalirati plugine (osim "core" plugina) i aplikacija će i dalje raditi (naravno neće imati punu funkcionalnost)



Aplikacija obuhvata po jedan "loader" i "visualizer" plugin, ali je napravljena da podrži proširenja u vidu novih plugina, po potrebi, sa relativno malo dopisivanja koda.






