# TLDR
This base file is setup in the format so that you can declare all necessary variables to run the ExaWind Solver in one file, and by running the "ExaWind\_Base\_Transform" code you can generate the needed input files (AMR-Wind and Nalu-Wind) to run ExaWind. To use the transformation code, you MUST change the base\_file\_path variable to the location (including the name) of your base file alongside changing the output\_file\_path to indicate where you wish your output files to be saved. Both these variables are at the very top of the transformation code. Then simply run the code (I used VScode).
The base file ("Exawind\_Base\_File.yml") is divided into three sections: AMR-Wind Variables, Nalu-Wind Variables, and Extra Variables with each section being defined by a commented line with dashes:

    \#-------------------- AMR-Wind\;Variables --------------------\# \nonumber

Please DO NOT delete these section divide comments as they provide the premise for transforming the base file. The code contained in the "Nonfunctional Error Checker" folder is you guessed it, nonfunctional.

If you wish to understand more about the changes made in the ExaWind base file compared to what you are used to, please see the "Variables" section in the tutorial PDF!
