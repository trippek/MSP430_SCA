# MSP430_SCA
This repo contains (hopefully) helpful resources to perform a side channel attack on an MSP430. This was created because an oscilloscope was used to collect power traces. The power traces were stored as .mat files and we were struggling to find SCA algorithms that took .mat files as input. 

## Where to start
The MSP430 SCA.ipynb file is well-commented and contains everything that is provided by this repo so far.

## Data
I could not upload our power trace data because it exceeded the file size limit.

## MSP430_SCA_v2 (version 2)
This version differs from the first in a few ways, some of which I included when I uploaded this file:
- Test code/manual debugging from the first version was excluded.
- Averaging was implemented so multiple traces can be used for each plaintext. Details are listed in the code.
- Power traces were filtered to cut out power spikes we think were associated with setting a flag on the MSP430 to identify encryption.
- The time it takes for the attack is printed.
### Small note after uploading v2:
Under the heading "List plaintext" I specified that there were 10 power traces saved the path to the folder where they were saved. To test the averaging function that comes later in the code, I made a new folder and copied three of the original traces five times to get a total of 15 traces in the new folder. That folder is the one in the code and the reason it lists 15 traces with five copies of each trace.

## MSP430_SCA_v3 (version 3)
This version differs from the second in a few ways:
- The plaintext is gathered from the data instead of the filename, as described in the "Plaintext" section.
- Averaging has been temporarily removed after method for gathering plaintext was changed.
- Files are organized by time they were saved on the oscilloscope to ensure proper order.
- Two levels of additional filtering are included: firstly, any invalid plaintext is filtered out. This occurs at the "Plaintext" section. Secondly, valid plaintexts with shortened power traces are filtered out at the "Additional Filtering and Conversion to Numpy Array" section. The power traces are also truncated to be the same size for the SCA algorithm section ("attack" section).

## In development
- Throw a try catch in to weed out any files that aren't .mat.
- Rewrite the code to take more traces without recalculating for previous traces.

## Questions
Contact trippekaris@gmail.com with questions.
