# Adapted from ChipWhisperer's software available at http://wiki.newae.com/V4:Tutorial_B6_Breaking_AES_(Manual_CPA_Attack)
# Command line inputs: python3 Progressive_CPA.py --seed_range (lowernum_highernum) --CONTINUATION (0 if first run, 1 otherwise) --total_traces (totalnum = highernum)
# Main editor: Calvin Herbek

import numpy as np
import scipy.io as sio
import h5py
import time
import argparse

# Lookup table for number of 1's in binary numbers 0-256
HW = [bin(n).count("1") for n in range(0, 256)]

sbox = (
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16)

def intermediate(pt, keyguess):
    return sbox[pt ^ keyguess]

def process_traces(seed_range, CONTINUATION, trace_label):
    start_time = time.time()

    # Retrieve traces and plaintext from matlab format
    mat_pt = sio.loadmat('/home/ktrippe/SCA_AES/srand_progressive_code_data/pt' + seed_range + '_unique.mat')
    pt = mat_pt['pt_unique']

    with h5py.File(r'/home/ktrippe/SCA_AES/srand' + seed_range + '/traces' + seed_range + '_sync_avg.mat') as mat_traces:
        numpy_array = mat_traces['average_traces'][:]
    traces = numpy_array.T

    numtraces = np.shape(traces)[0]
    print("number of traces:")
    print(numtraces)
    numpoint = np.shape(traces)[1]

    rank = [0] * 16
    key = ["01", "11", "22", "33", "44", "55", "66", "77", "88", "99", "aa", "bb", "cc", "dd", "ee", "ff"]
    bestguess = [0] * 16

    for bnum in range(0, 4):
        cpaoutput = [0] * 256
        maxcpa = [0] * 256

        if CONTINUATION:
            print("loading sum_hxt")
            total_sum_hxt = np.load(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_hxt.npy')
            print("loading sum_h")
            total_sum_h = np.load(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_h.npy')
            print("loading sum_t")
            total_sum_t = np.load(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_t.npy')
            print("loading sum_hsq")
            total_sum_hsq = np.load(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_hsq.npy')
            print("loading sum_tsq")
            total_sum_tsq = np.load(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_tsq.npy')
            print("loading total_traces")
            total_traces = np.load(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_traces.npy')
        else:
            total_sum_hxt = np.zeros([256, numpoint])
            total_sum_h = np.zeros([256, numpoint])
            total_sum_t = np.zeros([256, numpoint])
            total_sum_hsq = np.zeros([256, numpoint])
            total_sum_tsq = np.zeros([256, numpoint])
            total_traces = np.zeros(1)

        total_traces += numtraces

        sum_t = np.zeros(numpoint)
        sum_tsq = np.zeros(numpoint)
        for tnum in range(0, numtraces):
            sum_t += traces[tnum, :]
            sum_tsq += np.square(traces[tnum, :], dtype=np.longdouble)

        for kguess in range(0, 256):
            print("Subkey %2d, hyp = %02x: " % (bnum, kguess))

            sum_hxt = np.zeros(numpoint)
            sum_h = np.zeros(numpoint)
            sum_hsq = np.zeros(numpoint)

            hyp = np.zeros(numtraces)
            for tnum in range(0, numtraces):
                hyp[tnum] = HW[intermediate(pt[tnum][bnum], kguess)]

            for tnum in range(0, numtraces):
                sum_hxt += hyp[tnum] * traces[tnum, :]
                sum_h += hyp[tnum]
                sum_hsq += np.square(hyp[tnum], dtype=np.longdouble)

            total_sum_hxt[kguess] += sum_hxt
            total_sum_h[kguess] += sum_h
            total_sum_t[kguess] += sum_t
            total_sum_hsq[kguess] += sum_hsq
            total_sum_tsq[kguess] += sum_tsq

            cpaoutput[kguess] = np.divide(
                np.multiply(total_traces, total_sum_hxt[kguess], dtype=np.longdouble) -
                np.multiply(total_sum_h[kguess], total_sum_t[kguess], dtype=np.longdouble),
                np.sqrt(
                    np.multiply(
                        np.square(total_sum_h[kguess], dtype=np.longdouble) -
                        np.multiply(total_traces, total_sum_hsq[kguess], dtype=np.longdouble),
                        np.square(total_sum_t[kguess], dtype=np.longdouble) -
                        np.multiply(total_traces, total_sum_tsq[kguess], dtype=np.longdouble),
                        dtype=np.longdouble),
                    dtype=np.longdouble),
                dtype=np.longdouble)
            maxcpa[kguess] = max(abs(cpaoutput[kguess]))

            print(maxcpa[kguess])

        maxcpa_bits = np.array([(i, val) for i, val in enumerate(maxcpa)], dtype=[('bit', 'int32'), ('decimal', 'float64')])
        maxcpa_sorted = np.sort(maxcpa_bits, order='decimal')[::-1]
        rank[bnum] = np.where(maxcpa_sorted['bit'] == int(key[bnum], 16))[0][0]

        with open(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/MSP430_CPA_plain_traces_' + str(trace_label) + '_bnum' + str(bnum) + '.txt', 'w') as file:
            file.write(r'MSP430 CPA code with ' + str(trace_label) + ' unique traces. With averaging and synchronization.\n\n')
            file.write("bnum = ")
            file.write(str(bnum))
            file.write("\n")
            file.write("Correct key byte rank: ")
            file.write(str(rank[bnum]))
            file.write("\n")
            file.write("All key byte guesses ranked: \n")
            for kguess in maxcpa_sorted:
                file.write(' '.join(map(str, kguess)) + '\n')
            file.write("\n\n")

        bestguess[bnum] = np.argmax(maxcpa)
        cparefs = np.argsort(maxcpa)[::-1]
        print("Key byte", bnum, ": ", cparefs)

        print("saving numpy arrays")
        np.save(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_hxt.npy', total_sum_hxt)
        np.save(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_h.npy', total_sum_h)
        np.save(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_t.npy', total_sum_t)
        np.save(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_hsq.npy', total_sum_hsq)
        np.save(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_sum_tsq.npy', total_sum_tsq)
        np.save(r'/home/ktrippe/SCA_AES/progressive_cpa_sync_avg/kb' + str(bnum) + '_total_traces.npy', total_traces)

    print("Best Key Guess: ")
    for b in bestguess:
        print("%02x " % b)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(r'Elapsed Time for full program: ' + str(elapsed_time) + ' seconds')

def main():
    parser = argparse.ArgumentParser(description='Process traces for side-channel analysis.')
    parser.add_argument('--seed_range', type=str, required=True, help='Seed range for the traces')
    parser.add_argument('--CONTINUATION', type=int, required=True, help='Continuation flag (0 or 1)')
    parser.add_argument('--total_traces', type=int, required=True, help='Total number of traces')

    args = parser.parse_args()

    process_traces(args.seed_range, args.CONTINUATION, args.total_traces)

if __name__ == '__main__':
    main()
