from pylab import *
from rtlsdr import *
import numpy


# variables
# full frequency band
start_freq = int(75e6)
end_freq = int(1e9)

# alt frequency band
#start_freq = int(80e6)
#end_freq = int(120e6)

# rtlsdr sample rate
sample_rate = int(2.4e6)

mid_freq = int((end_freq + start_freq)/2)
width_freq = int(end_freq-start_freq)


# rtlsdr configuration
sdr = RtlSdr()
sdr.sample_rate = sample_rate
sdr.gain = 'auto'
sdr.bandwith = 500e3

#create new np array
all_samples = sdr.read_samples(256*1024)


# scan the frequency band
for new_freq in range(start_freq, end_freq, sample_rate*2):
	sdr.center_freq = new_freq + sample_rate
	samples = sdr.read_samples(256*1024)
	all_samples = numpy.concatenate((all_samples, samples))

treshold = all_samples.mean()

new_samples = sdr.read_samples(256*1024)
for new_freq in range(start_freq, end_freq, sample_rate*2):
	if (all_samples > treshold).all():
		new_samples = numpy.concatenate((new_samples, samples))

sdr.close()

# use matplotlib for PSD
psd(new_samples, NFFT=1024, Fs=width_freq/1e6, Fc=mid_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

show()

