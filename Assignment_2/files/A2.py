import scipy.ndimage as img
import numpy as np

def makeBinary(input_filename, output_filename = 'out.bin'):
    #Options for the FFT
    Fs=1800000 
    T_line=0.005
    
    #Read input image
    image = img.imread(input_filename)

    # Set FFT size to be double the image size so that the edge of the spectrum stays clear
    # preventing some bandfilter artifacts
    NFFT = 2*image.shape[1]

    # Repeat image lines until each one comes often enough to reach the desired line time
    repetitions = int(np.ceil(T_line * Fs / NFFT))
    ffts = ((np.repeat(image[:, :, 0], repetitions, axis=0) / 16.)**2.) / 256.

    # Embed image in center bins of the FFT
    fftall = np.zeros((ffts.shape[0], NFFT))
    startbin = int(NFFT/4)
    fftall[:, startbin:(startbin+image.shape[1])] = ffts


    # Generate random phase vectors for the FFT bins, this is important to prevent high peaks in the output
    # The phases won't be visible in the spectrum
    phases = 2*np.pi*np.random.rand(*fftall.shape)
    rffts = fftall * np.exp(1j*phases)

    # Perform the FFT per image line, then concatenate them to form the final signal
    timedata = np.fft.ifft(np.fft.ifftshift(rffts, axes=1), axis=1) /np.sqrt(float(NFFT))
    linear = timedata.flatten()
    linear = linear / np.max(np.abs(linear))

    # Match the requirements
    res = np.zeros(2*linear.size, dtype=np.float32)		
    res[0::2], res[1::2] = np.real(linear), np.imag(linear)				 
	
    #Get the Output
    res.tofile(output_filename)
    
    return


# Create the Signals
makeBinary('signal_kreis.png','signal_kreis.bin')
makeBinary('physec.png','physec.bin')
