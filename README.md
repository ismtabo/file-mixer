File Mixer
====

Desktop tool code in Python3 with GTK3 to help joining input and output files from problems of UVa Online Judge.

Dependencies
----

To use this tool is needed to have installed in your machine:
- Python3
- GTK3+

This tool has been developed and tested in systems:
- Xubuntu 16.04
- Xubuntu 17.04
- Linux Lite 3.X

Instalation and usage
----

Clone the repository on your machine in any path you choose by:
```
git clone https://github.com/ismtabo/file-mixer
```

Start the tool by the command bellow:
```
python3 -m file_mixer
```

Getting started
----
To join problems' files with this tool first you have to open a problems directory by clicking the _Abrir Carpeta_ button, at the center part of the application, or selecting _Archivo/Abrir Carpeta_ at the application menu.

Next, the folder tree structure will be shown at the left part of the applicaction. To create a new problem, you should click _Nuevo_ button at the center block, this will open a entry to insert number of the problem. 

Finally, to start adding files to the new problem you should ensure to have input and output files' extensions in the list at the right part of the window. There are two list, upper shows list of inputs' extensions, and bottom one show outputs' extentions. By default they are two respectively extensions for input and output files, this are:
- `.in`
- `.ans`

This last step is important to add new files as this tools only accepts input files with valid extension, and also it looks for files with same name as input one, at its same path, but with valid output extension.

After following steps above you can add files by dragging and dropping from the tree view structure to the box at the bottom of the center part. 

When you want to save a problem, click button _Guardar_ or select _Archivo/Guardar_ at the application context, and choose destination folder for your problem. The application is going to write 3 files:
- p<problem_id>.in
- p<problem_id>.ans
- p<problem_id>.prob

First two files containts input and output for the actual problem, the third file containts information of the problem, as the number, and the list of input and output selected files with absolute paths, that can then be retrieved by the program using _Abrir Problema_ button or selecting _Archivo/Abrir Programa_ at the context menu.

### Preview of actual problem

The other two tabs of the right part of the window can be used to preview the content of input and output files. Selecting any of it you can have a quick preview of the full content of each files.

### Modifiying information about actual problem

The upper part at the center block of the window have some information about the actual problem.
- _Número de problema_: Number entry that contains the number or id of the actual problem. This can be modified by entrying a new number and then clicking _Actualizar_(refresh) button, to apply changes.
- _Número total de ficheros_: Total number of selected files (cases), only takes into account input files, as this number it is equal to the number of output files.
- _Tamaño fichero de entradas_: Size of current problem input file.
- _Tamaño fichero de respuestas_: Size of current problem output file.

### Special modifications

In case you have the number of cases of each input file at the first line of each, you can select the checkbutton _Número de casos en la primera fila_ (Number of cases at first line) to have the total number of cases at the first line of the resulting input file, appending only the following lines of each input file.

#### Sorting files of problem

You can also sort files added to the current problem by clicking either _por nombre_(by name) or _aleatoriamente_(randomly), near _Ordenar:_(Sort) label:
- _por nombre_: will short files by input filename.
- _aleatoriamente_: will shuffle file list.

#### Empty files list

Last but not least, you can empty file list by clicking _Eliminar todos_(Delete all) button, clearing problems inforation.

TODO list
----
- [ ] Translate aplication interface from Spanish
- [ ] Add self-explained and detailed output errors
- [ ] Add feedback at tasks of the tool which take much time to complete.
- [ ] Zip problem information and used files into own file format and extension.

Authors
----
- Ismael J. Taboada: [ismtabo](https://github.com/ismtabo)
