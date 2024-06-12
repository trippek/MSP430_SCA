# MATLAB files
This folder contains the MATLAB files to implement the same functionalities as the MSP430_SCA_vx.ipynb files.

## Purpose of this folder
The switch to MATLAB (or option to use MATLAB instead) was motivated by the fact that our raw data files are in .mat format already and because some of the programs we were trying to test in Python were taking days to run with very few debugging messages. It appears that MATLAB avoids long run times through limiting array size. This has caused us to restructure the code slightly through making it more modular and easier to debug.

## Overview
So far, our MATLAB code will take the raw data files directly from our SSD (which is where we are saving the data from the oscilloscope), extract the power traces and corresponding plaintexts, and synchronize and average the power traces and plaintexts. 

### File breakdown
- align_signals_SAD_conv.m: takes as input any matrix (in this case, the power trace matrix), and outputs the aligned matrix. This algorithm implements the sum of absolute differences (SAD) method.
- average_optimized.m: takes as input plaintext and power trace arrays and outputs the plaintext and power trace arrays after they have been averaged, meaning there should be a single, averaged power trace for each plaintext and no repeat plaintexts.
- plaintext.m: takes as input the directory where the raw data should be stored. Important note that the code is written with a specific assumption about the order of the data that is related to how we have chosen to collect plaintext and power traces. It must be organized by channel (ch4, ch5, then math) and organized by time within each subcategory. This was chosen for time optimization. The outputs of this file are the plaintext and power trace data. The 128-bit plaintext is represented as 16 8-bit chunks in decimal representation. This is formatted for the chipwhisperer CPA algorithm.
- main.m: This file sets the directory variable and calls the needed functions in the correct order to output the final averaged and synchronized plaintext and power traces. If you need to save intermediate results, you can run functions individually.

### Limitations
- Due to MATLAB's storage requirements, we have gotten some memory issues. So far we can resolve those by either decreasing the size of our matrix or storing previous results externally.
- We currently don't have an operating MATLAB version of the CPA algorithm, so we've been getting everything preprocessed in MATLAB and then using our Python code to run the attack.

### Timing
Our raw power trace matricies are 4628x375834. The process to go from the raw data on the SSD to averaged and synchronized matricies takes approximately 50 minutes.
