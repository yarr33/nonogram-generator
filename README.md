# nonogram-generator
nonogram-generator AKA nonogen is a tool written in python that generates nonograms from a black/white image file.

you can import the file, and use the gen function as mentioned below:
```
import nonogram_generator as nog

nog.gen("path to read from", pageSize, backgroundColor, abortIfUnsolvableNonogram)
```
the generated image will be saved in the directory of the image that the program reads.
