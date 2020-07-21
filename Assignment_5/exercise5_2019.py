import xarray
import numpy as np
import matplotlib.pyplot as plt



#----------------------------------------------
# ------- Hints and Remarks
# You receive a set of CSI data from the VPoR container setup.
# The set consists of 40 different challenges and 100 repetitions per challenge. The actual challenges are not included,
# only the CSI data.
# The CSI data of a single measurement is a vector of length 6,156. This vector can be divided into single channels of
# length 114. Each single channel belongs to one spatial frequency at a specific center frequency. Some pre-processing
# algorithms are performed on individual channels and you will have to iterate through all 54 channels of length 114.
#
# The complete CSI data is stored in a matrix of shape (4000, 6156). All measurement that belong to a single challenge
# are stored in order, i.e.
# data[0,:] is the spectrum of the first measurement of the first challenge
# data[1,:] is the spectrum of the second measurement of the first challenge
# data[99,:] is the spectrum of the last measurement of the first challenge
# data[100,:] is the spectrum of the first measurement of the second challenge


# ---------------------------------------------
# ------- Helper Functions
# You don't have to add anything here

def load_data():
    """
    Loads a set of CSI data from a VPoR experiment
    :return:
    """
    return np.load('csi_dataset.npy')


def compute_euclidean_distance(vector_a, vector_b):
    """
    Computes the euclidean distance between two vectors of arbitrary length
    :param vector_a:
    :param vector_b:
    :return:
    """
    return np.linalg.norm(vector_a - vector_b)


def plot_intra_inter_histograms(intra_data, inter_data, title, filename):
    """
    Plots and stores a figures that shows the distribution of intra and inter distances
    :param intra_data:
    :param inter_data:
    :param title:
    :param filename:
    :return:
    """
    fig, ax = plt.subplots()
    width = 3.487 * 3
    height = width / 1.618
    fig.set_size_inches(width, height)
    fig.subplots_adjust(left=.10, bottom=.14, right=.95, top=.93)
    ax.hist(intra_data, weights=np.ones(len(intra_data)) / len(intra_data), label='Intra Distances')
    ax.hist(inter_data, weights=np.ones(len(inter_data)) / len(inter_data), label='Inter Distances')
    ax.legend()
    plt.title(title)
    fig.show()
    plt.savefig(filename + '.png')


def print_overlap(intra_overlap, inter_overlap, prepproc_string):
    print(prepproc_string)
    print("  {:.2f}% of all intra distance are larger than the smallest inter distance".format(intra_overlap*100))
    print("  {:.2f}% of all inter distance are smaller than the largest intra distance".format(inter_overlap*100))


# ---------------------------------------------
# ------- Worker Functions
# Complete functions here

def standardize_per_channel(data):
    """
    Standardize each channel of 114 CSI values of each measurement individually. Do this by subtracting the mean value of the
    channel from each point and divide it by the channels' variance.
    Make sure to return a copy of data instead of modifying data directly.
    Hint: Use vectorization for performance, i.e., perform the standardization for the first channel of all measurements
          at the same time. You can calculate the mean and variance with numpy function along an axis.
    :param data:
    :return:
    """
    print("standardize_per_channel...")
   
    data_copy = data.copy()
    new_data = []
	
    for measurement in data_copy: 
	#get channels
	channels=np.array(np.split(measurement, len(measurement)/114)) 
	# copied new data in 1D Array
	new_data.append([ ((chan-mean)/var).flatten() for chan,mean,var in zip(channels, channels.mean(axis=1), channels.var(axis=1)) ])
    
    print('sucessful.')
    return np.array(new_data)


def euclidean_norm_per_channel(data):
    """
    Normalize each channel of 114 CSI values of each measurement individually. Do this by dividing each point of the
    channel by the length of the channel's vector.
    Make sure to return a copy of data instead of modifying data directly.
    Hint: One way to compute the length of the vector is to use compute_euclidean_distance(vector_a, np.zeros_like(vector_a)).
          This is the distance to the null vector or simple the vector length.

    :param data:
    :return:
    """
    
    print("euclidean_norm_per_channel...")
    data_copy = data.copy()
    new_data = []
    # len of vector
    l = lambda vector_a: compute_euclidean_distance(vector_a, np.zeros_like(vector_a))
	
    for measurement in data_copy: 
	channels=np.array(np.split(measurement, len(measurement)/114))
	new_data.append([ (chan/l(chan)).flatten() for chan in channels ])


    print('sucessful.')
    return np.array(new_data)

	
    
 

    
def compute_intra_distance(data, num_challenges):
    """
    Computes the intra distances for all challenges in the data set. The first measurement of each challenge is
    defined as the reference. To compute the intra distances, take the measurement and compute the euclidean distance
    to all following measurements that belong to same challenge.
    Put all intra distance of all challenges into a single one-dimensional numpy vector.
    Hint: for calculating the euclidean distance you may use: compute_euclidean_distance(x, y)
    :param data:
    :param num_challenges:
    :return: numpy vector containing all intra distances
    """

    print("compute_intra_distance...")
    data_copy = data.copy()

    challenges = np.split(data_copy, num_challenges)
    intra_distances = [compute_euclidean_distance(challenge[0],measurement) 
                       for challenge in challenges
                       for measurement in challenge[1:]]
    
    print('sucessful.')
    return np.array(intra_distances)


def compute_inter_distance(data, num_challenges):
    """
    Computes a sub-set of all possible inter distance. To keep the number of inter distances low use only the first
    measurement of each challenge. Compute the distances for all possible combinations of this sub-set of measurements.
    Put all inter distance of all challenges into a single one-dimensional numpy vector. 
    Hint: Make sure that you do not compute the same sane inter-distance twice.
    	  For calculating the euclidean distance you may use: compute_euclidean_distance(x, y)
    :param data:
    :param num_challenges:
    :return: numpy vector containing all inter distances
    """

    print("compute_inter_distance...")
    data_copy = data.copy()

    challenges = np.split(data_copy, num_challenges)
    inter_distances = [compute_euclidean_distance(chall[0],measurement)
                       for i,chall in enumerate(challenges)
                       for j,subchall in enumerate(challenges)
                       if subchall is not chall
                       for measurement in subchall[0 if i<j else 1:]]

    print('sucessful.')
    return np.array(inter_distances)


# ---------------------------------------------
# ------- Further Functions
# You don't have to change anything here

def standardize_per_freq_bin(data):
    """
    Standardize the spectrum bin by bin, i.e., each of the 6,156 points of the spectrum are standardized over all
    measurements of all challenges.
    Make sure to return a copy of data instead of modifying data directly.
    :param data:
    :return:
    """
    new_data = data.copy()
    new_data = (new_data - new_data.mean(axis=0)) / new_data.var(axis=0)
    return new_data


def overlap_intra(intra_data, inter_data):
    """
    Compute the percentage of intra distances that are larger than the minimal inter distance.
    Return the percentage as a value between 0.0 and 1.0.
    :param intra_data:
    :param inter_data:
    :return:
    """
    return (intra_data > inter_data.min()).sum() / intra_data.size

def overlap_inter(intra_data, inter_data):
    """
    Compute the percentage of inter distances that are smaller than the largest intra distance.
    Return the percentage as a value between 0.0 and 1.0.
    :param intra_data:
    :param inter_data:
    :return:
    """
    return (inter_data < intra_data.max()).sum() / inter_data.size


# ---------------------------------------------
# ------- Program Execution
# You don't have to change anything here

if __name__ == '__main__':
    # Load CSI data
    data = load_data()
    num_exp = 40

    # Perform preprocessing
    std_data = standardize_per_channel(data)
    norm_data = euclidean_norm_per_channel(data)
    std_freq_data = standardize_per_freq_bin(data)
    #std_both = standardize_per_freq_bin(std_data)

    # Compute distances
    inter_dist = compute_inter_distance(data, num_exp)
    intra_dist = compute_intra_distance(data, num_exp)

    std_inter_dist = compute_inter_distance(std_data, num_exp)
    std_intra_dist = compute_intra_distance(std_data, num_exp)

    norm_inter_dist = compute_inter_distance(norm_data, num_exp)
    norm_intra_dist = compute_intra_distance(norm_data, num_exp)

    std_freq_inter_dist = compute_inter_distance(std_freq_data, num_exp)
    std_freq_intra_dist = compute_intra_distance(std_freq_data, num_exp)

    # Compute overlap
    inter_overlap_perc = overlap_inter(intra_dist, inter_dist)
    intra_overlap_perc = overlap_intra(intra_dist, inter_dist)

    std_inter_overlap_perc = overlap_inter(std_intra_dist, std_inter_dist)
    std_intra_overlap_perc = overlap_intra(std_intra_dist, std_inter_dist)

    norm_inter_overlap_perc = overlap_inter(norm_intra_dist, norm_inter_dist)
    norm_intra_overlap_perc = overlap_intra(norm_intra_dist, norm_inter_dist)

    std_freq_inter_overlap_perc = overlap_inter(std_freq_intra_dist, std_freq_inter_dist)
    std_freq_intra_overlap_perc = overlap_intra(std_freq_intra_dist, std_freq_inter_dist)

    # Plot histograms
    plot_intra_inter_histograms(intra_dist, inter_dist, 'No Preprocessing', 'no_preprocessing')
    plot_intra_inter_histograms(std_intra_dist, std_inter_dist, 'Standardization Per Channel', 'std_channel')
    plot_intra_inter_histograms(norm_intra_dist, norm_inter_dist, 'Euclidean Normalization per Channel',
                                'euclid_norm_channel')
    plot_intra_inter_histograms(norm_intra_dist, std_freq_inter_dist, 'Standardization Per Frequency Bin',
                                'std_freq_bin')

    # Print overlap
    print_overlap(intra_overlap_perc, inter_overlap_perc, 'No Preprocessing')
    print_overlap(std_intra_overlap_perc, std_inter_overlap_perc, 'Standardization Per Channel')
    print_overlap(norm_intra_overlap_perc, norm_inter_overlap_perc, 'Euclidean Normalization per Channel')
    print_overlap(std_freq_intra_overlap_perc, std_freq_inter_overlap_perc, 'Standardization Per Frequency Bin')


    raw_input('Press ENTER to exit...')
