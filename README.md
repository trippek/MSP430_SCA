# MSP430_SCA
This repo contains (hopefully) helpful resources to perform a side channel attack on an MSP430. This was created because an oscilloscope was used to collect power traces. The power traces were stored as .mat files and we were struggling to find SCA algorithms that took .mat files as input. 

## Where to start
The MSP430 SCA.ipynb file is well commented and contains everything that is provided by this repo so far.

## Data
I could not upload our power trace data because it exceeded the file size limit.

## In development
- Add a feature for smmoothing out multiple power traces for the same plaintext.
- Clean up the data (we think the flag we set on the MSP430 to indicate the beginning and end of the first round of encryption might be causing some irregular power activity at the beginning and end of our traces).
- Throw a try catch in to weed out any files that aren't .mat.

## Questions
Contact trippekaris@gmail.com with questions.
