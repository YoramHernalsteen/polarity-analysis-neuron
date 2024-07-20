# How to run the application

1. Open the terminal in the folder where you downloaded the application to.

![output file](docs/open_in_terminal.png)

2. If on Mac or linux then we need to make the script executable. Run 'chmod +x run.sh'. This will make sure you can run the script.

```
chmod +x run.sh
```

3. Run the actual run.sh script on Mac or Linux, run.ps1 on Windows.

```
./run.sh
```
```
./run.ps1
```

# How to use the polarity analysis app.

![Application](docs/app.png)

## Configure the input, output and analysis folders the application will use.

The input folder will be scanned to check if we need to pinpoint the centre of cells in images. Please copy the path of the input folder here.

![How to copy path of folder](docs/Copy-pathname-Finder-Mac.jpg)

The output folder is of no importance to the user. Here processed files (files with the blue dot as centre) are saved. These are used to do polarity analysis on.

The analysis folder has the results of the polarity analysis. Every input image has a csv file (same name)with the results (percentage and absolute amount of pixels) per part (topright1, topright2, bottomright1, bottomright2, bottomleft1, bottomleft2, topleft1, topleft2). A picture with a visual representation of the algorithm is also generated.

## Pinpoint the centre of the neuron

The application will ask you per file in the input folder that is not yet converted to click on the centre of the neuron. This will output a blue point on the selected place.

1. Click on the centre of the neuron
2. Press S to save, Q to quit.

![output file](docs/output.png)

## Analyse the neuron

The application will analyse the direction of the neuron and create a csv file (percentage per part) and visual representation of the analysis.

The first part is topright 1, the last part is topleft 2.

![analysis file](docs/csv.png)

![analysis file](docs/analysis.png)

## New feature Auto Analysis
This will use an algorithm to find the coordinate with the most neighbouring neuron coordinates. The program will go on and do analysis based on the results of the centre recognition algorithm. User only has to verify wether the correct center was picked.

Auto analysed files will be named like 'auto_recognition_' concatted by the original filename.
