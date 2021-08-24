
import struct
import numpy as np
import os
import h5py
import argparse
from scipy.interpolate import interp1d

def convert_to_continuos_f0(f0):
    """CONVERT F0 TO CONTINUOUS F0.

    Args:
        f0 (ndarray): original f0 sequence with the shape (T,).

    Returns:
        ndarray: continuous f0 with the shape (T,).

    """
    # get uv information as binary
    uv = np.float32(f0 != 0)

    # get start and end of f0

    if (f0 == 0).all():
        logging.warning("all of the f0 values are 0.")
        return uv, f0

    start_f0 = f0[f0 != 0][0]
    end_f0 = f0[f0 != 0][-1]

    # padding start and end of f0 sequence
    start_idx = np.where(f0 == start_f0)[0][0]
    end_idx = np.where(f0 == end_f0)[0][-1]
    f0[:start_idx] = start_f0
    f0[end_idx:] = end_f0

    # get non-zero frame index
    nz_frames = np.where(f0 != 0)[0]

    # perform linear interpolation
    f = interp1d(nz_frames, f0[nz_frames])
    cont_f0 = f(np.arange(0, f0.shape[0]))

    return uv, cont_f0

def chcek_lf0(lf0_filenames,h5_filenames):

    for i in range(len(lf0_filenames)):
        hdf5_file = h5py.File(h5_filenames[i], "r")
        feat = hdf5_file["/world"][()]
        hdf5_file.close()

        with open(lf0_filenames[i], "rb" ) as f:
            length = f.read()
        lf0 = struct.unpack( "f" * (len(length) // 4) , length )
        lf0 = np.exp(np.array(lf0))

        err = 0
        for i in range(len(lf0)):
            if lf0[i] != 0.0 :
                if lf0[i] - feat[i][1] > 1 :
                    err = 1
        if err == 1 :
            print("error :",h5_filenames[i])

    if err == 0 :
        print("lf0_check_success")

    return 0

def check_mgc(mgc_filenames,h5_filenames):
    for i in range(len(mgc_filenames)):
        hdf5_file = h5py.File(h5_filenames[i], "r")
        feat = hdf5_file["/world"][()]
        hdf5_file.close()

        with open(mgc_filenames[i], "rb" ) as f:
            length = f.read()
        mgc = struct.unpack( "f" * (len(length) // 4) , length )
        mgc = np.array(mgc).reshape(-1,25)

        #print(mgc.shape, feat.shape)

        err = 0
        for i in range(len(mgc)):
            for j in range(len(mgc[i])):
                if mgc[i][j] - feat[i][j+2] > 0.001:
                    err = 1

        if err == 1 :
            print("error :",h5_filenames[i])

    if err == 0 :
        print("mgc_check_success")

    return 0

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--lf0_dir', required=True)
    parser.add_argument('--mgc_dir', required=True)
    parser.add_argument('--out_dir', required=True)
    args = parser.parse_args()

    lf0_dir_path = args.lf0_dir
    mgc_dir_path = args.mgc_dir
    hdf5_dir_path = args.out_dir

    if not os.path.exists(lf0_dir_path):
        print("lf0_inputfile_not_found")
    if not os.path.exists(mgc_dir_path):
        print("mgc_inputfile_not_found")
    if not os.path.exists(hdf5_dir_path):
        os.makedirs(hdf5_dir_path)

    lf0_filename = []
    for filename in sorted(os.listdir(lf0_dir_path)):
        if filename.endswith(".lf0"):
            lf0_filename.append(filename)
    mgc_filename = []
    for filename in sorted(os.listdir(mgc_dir_path)):
        if filename.endswith(".mgc"):
            mgc_filename.append(filename)

    lf0_filenames = [ os.path.join(lf0_dir_path, x) for x in lf0_filename ]
    mgc_filenames = [ os.path.join(mgc_dir_path, x) for x in mgc_filename ]

    ## hdf5_gen
    for i in range(len(lf0_filenames)):
        # with open( f0_filenames[i], "rb" ) as f:
        #     length = f.read()
        # f0_frame = struct.unpack( "f" * (len(length) // 4) , length )
        with open( mgc_filenames[i], "rb" ) as f:
            length = f.read()
        mgc_frame = struct.unpack( "f" * (len(length) // 4) , length )
        with open( lf0_filenames[i], "rb" ) as f:
            length = f.read()
        lf0_frame = struct.unpack( "f" * (len(length) // 4) , length )
        #uv = [ 0.0 if x == -10**10 else 1.0 for x in f0_frame]

        f0 = np.exp(np.array(lf0_frame, dtype=np.float32))
        uv , cont_f0 = convert_to_continuos_f0(f0)

        #f0 = np.array(f0_frame).reshape(-1,1)

        cont_f0 = cont_f0.reshape(-1,1).astype(np.float32)
        mgc = np.array(mgc_frame, dtype=np.float32).reshape(-1,25)
        uv = np.array(uv, dtype=np.float32).reshape(-1,1)
        feat = np.concatenate( (uv,cont_f0,mgc), axis=1)
        # print("cont_f0 :",cont_f0.shape, cont_f0.dtype)
        # print("mgc :",mgc.shape, mgc.dtype)
        # print("uv :",uv.shape, uv.dtype)
        # print("feat :",feat.shape, feat.dtype)

        basename = os.path.basename(lf0_filenames[i]).replace("lf0","h5")
        hdf5_filename = os.path.join(hdf5_dir_path,basename)
        with h5py.File(hdf5_filename , 'w') as f :
            f['world'] = feat
            #print("write {} finished".format(hdf5_filename))
    print("write hdf5 finished")
    ## check_hdf5
    h5_filename = []
    for filename in sorted(os.listdir(hdf5_dir_path)):
        if filename.endswith(".h5"):
            h5_filename.append(filename)
    h5_filenames = [ os.path.join(hdf5_dir_path, x) for x in h5_filename ]

    chcek_lf0(lf0_filenames,h5_filenames)
    check_mgc(mgc_filenames,h5_filenames)
