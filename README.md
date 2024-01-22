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

## In development
- Throw a try catch in to weed out any files that aren't .mat.
- Rewrite the code to take more traces without recalculating for previous traces.

## Questions
Contact trippekaris@gmail.com with questions.
