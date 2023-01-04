# analysis-of-bacterial-colonies

This program (**ColonyCalculation**) was created to help analyze the data collected from **SphereFlash** software. 
The anti-bacteria test is conducted according to JIS Z 2801:2010 standard.
This program's functions include calculating the average number of colonies in each sample and calculating the antibacterial activity (%). Moreover, when the count of colonies < 1, this program can automatically take it as 1 in accordance with the standard requirements.

### Note: 
The plate ID when using **SphereFlash** ==**MUST**== follow this example: YYYYMMDD-A-B-C-D, where the 8 digits before first hyphen represent time, then "A" means the type of bacteria (e.g., "EC" represents E.Coli). "B" is the name of your sample. "C" is the dilution ratio (commonly 1 or 10, other values are also accepted), and D is the sequence number of the parallel samples (1,2,3,...). So the ID should be named: (YYYYMMDD)-(Bacterial name)-(sample name)-(dilution ratio)-(sequence number of parallel samples). For U0 and Ut samples, please use "U0" or "Ut" for "B". The name of plate ID is very important, the program can't normally operate with incorrect plate ID! The users are suggested to find examples of plate ID  by opening the "ExportedData.xlsx" in program's "examples" folder . 



## How to use this program
The use of this program is so easy.
1. Download all v1.0.1 files (including *.z01, *.z02 and *.zip files) from "Releases" and unzip. Open the "ColonyCalculation.exe"
2. Click ... button to select an Excel file (*.xlsx or *.xls) created by **SphereFlash** software. Its default name is "ExportedData.xlsx". We provide an example file in the "examples" folder
3. According to Part 5.6(b) in standard, the films on test pieces may have varied areas. Remember to fill in the value of film side length (cm)
4. Press "start" button, and the program can generate a new Excel file containing the average colony count of each sample, the actibacterial activity of each sample, the dilution factor, etc.

### Note: 
We used the 50-μL-linear mode for bacteria spiral, but the standard required 1 mL. So we multiply the number of viable bacteria by 20 (Part 5.7). And the U-value in generated file means the common logarithm (log10) of viable bacteria.
