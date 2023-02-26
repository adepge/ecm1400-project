from skimage import io 
import numpy as np
import utils

io.use_plugin('matplotlib')



def find_red_pixels(map_filename:str, upper_threshold=100, lower_threshold=50) -> np.ndarray:
    """
    Finds all red pixels and generates a binary image file
    Red is RGB-value defined by these thresholds: (R > 100, G < 50, B < 50)

    Arguments:
        map_filename (str): Path to image file
        upper_threshold (int): default = 100
        lower_threshold (int): default = 50
    Outputs:
        map-red-pixels.jpg: binary image file (saved in ./data/)
    Returns:
        map_array (np.ndarray): 2D array representing image file
    """



    map_array = io.imread(map_filename)                                     # Reads image file into 2D Numpy array
    map_array = map_array[:,:,:3] * 255                                     # Retains first three values of each pixel (removes alpha channel) and scales RGB channels to 0-255
    red_pixels = np.where(  (map_array[:,:,0] > upper_threshold) &          # Identifies red pixels based on RGB values
                            (map_array[:,:,1] < lower_threshold) & 
                            (map_array[:,:,2] < lower_threshold)   )
    map_array[red_pixels] = [255, 255, 255]                                 # Marks red pixels white
    map_array[np.any(map_array != [255, 255, 255], axis=2)] = [0, 0, 0]     # Marks non-white (non-red) pixels black
    map_array = map_array.astype(np.uint8)                                  # Converts array into unsigned 8-bit integers (0-255) from signed 32-bit floating point number
    io.imsave('data/map-red-pixels.jpg', map_array)                         # Outputs jpg file of marked pixels
    print('File saved as: ./data/map-red-pixels.jpg')
    return map_array


def find_cyan_pixels(map_filename:str, upper_threshold=100, lower_threshold=50) -> np.ndarray:
    """
    Finds all cyan pixels and generates a binary image file
    Cyan is RGB-value defined by these thresholds: (R < 50, G > 100, G > 100)

    Arguments:
        map_filename (str): Path to image file
        upper_threshold (int): default = 100
        lower_threshold (int): default = 50
    Outputs:
        map-cyan-pixels.jpg: binary image file (saved in ./data/)
    Returns:
        map_array (np.ndarray): 2D array representing image file
    """
    map_array = io.imread(map_filename)
    map_array = map_array[:,:,:3] * 255        
    cyan_pixels = np.where( (map_array[:,:,0] < lower_threshold) &          # Identifies cyan pixels based on RGB values
                            (map_array[:,:,1] > upper_threshold) & 
                            (map_array[:,:,2] > upper_threshold)   )                            
    map_array[cyan_pixels] = [255, 255, 255]                                # Marks cyan pixels white
    map_array[np.any(map_array != [255, 255, 255], axis=2)] = [0, 0, 0] 
    map_array = map_array.astype(np.uint8)      
    io.imsave('data/map-cyan-pixels.jpg', map_array)
    print('File saved as: ./data/map-cyan-pixels.jpg')
    return map_array

def detect_connected_components(IMG:str)-> np.ndarray:
    """
    Finds all 8-neighbour connected components, returns 2D array with components, and generates text file with component data.
    Uses a modified version of Algorithm 1 to detect connected components (as per specification) with the following changes:
        
        - Each argument (e.g P(x,y)) is arranged in order of iteration: (y,x) where y,x = m,n = s,t
            - Specifically: y,m,s iterates in the first dimension (vertical) and x,n,t in the second dimension (horizontal)
        - p(y,x) is a pavement pixel when RGB-channel values exceed threshold > 200: Compensates for jpg lossy compression
        - MARK(y,x) = R, when set as visited: R is the counter for each connected region/component, where R > 0:
        - end while condition: when Q is empty, R = R + 1

    Arguments:
        IMG (str): Path to image file
    Outputs:
        cc-output-2a.txt: text file with number of connected components and corresponding pixel size (saved in ./data/)
    Returns:
        MARK (np.ndarray): 2D array representing connected components
    """
    from skimage import io 
    
    image = io.imread(IMG)
    image = np.copy(image)
    threshold = np.where(   (image[:,:,0] > 200) &          # Threshold values for pixels due to jpg lossy compression
                            (image[:,:,1] > 200) & 
                            (image[:,:,2] > 200)   )
    image[threshold] = [255,255,255]                        # Sets all pixels above threshold values as pavement pixels (value = 255)
    i,j,_ = image.shape
    MARK = np.zeros((i,j))

    
    R = 1                                                                       # R (Region counter)
    Q = np.empty(0)
    print("Computing results... (this may take some time)")
    for y in range(i):                                                          # Scans image from top to bottom (y value)
        for x in range(j):                                                      # In each row, scans from left to right (x value)
            if np.any(image[y,x] == [255,255,255]) == True and MARK[y,x] == 0:
                MARK[y,x] = R                                                   
                coordinates = [y,x]
                Q = np.append(Q, coordinates)
                Q = Q.reshape(-1,2)                 # Arranges Q in y,x pairs
                while np.size(Q) > 0:               # while Q is not empty do
                    m,n = Q[0]                                                                                                  # Finds y,x values of neighbours of Q(m,n)
                    neighbours = [      [min(m+1,i-1),   max(n-1,0)], [min(m+1,i-1),   n],  [min(m+1,i-1),  min(n+1,j-1)],      #   [:] [:] [:]    | Key:
                                        [m           ,   max(n-1,0)],                       [m           ,  min(n+1,j-1)],      #   [:]  Q  [:]    |  Q  - pixel (m,n)
                                        [max(m-1,0)  ,   max(n-1,0)], [max(m-1,0)  ,   n],  [max(m-1,0)  ,  min(n+1,j-1)]   ]   #   [:] [:] [:]    | [:] - eight-connected neighbour           
                    for pixel in neighbours:                                                                                    # max() and min() used in case of upper and lower bounds (edge of image)                            
                        s,t = pixel     
                        s,t = int(s),int(t)         # converts (s,t) from float to integer                                        
                        if np.any(image[s,t] == [255,255,255]) == True and MARK[s,t] == 0:
                            MARK[s,t] = R
                            coordinates = [s,t]
                            Q = np.append(Q, coordinates)
                            Q = Q.reshape(-1,2)
                    Q = np.delete(Q, 0, axis = 0)   # remove first item q(m,n) from Q
                else:
                    R = R + 1                       # Over each pass in the loop where Q is empty, increment region counter
    R = int(np.max(MARK))
    component_array = MARK.flatten().tolist()       # Flattens 2D array -> 1D, makes it suitable for countvalue function (see utils.py)
    with open('data/cc-output-2a.txt','w') as f:
        for index in range(1,R+1):                  # For each region, count number of pixels
            occurrence = utils.countvalue(component_array, index)
            f.write(f"Connected component {index}, number of pixels = {occurrence} \n")
        f.write(f"Total number of connected components = {R}")
    print('File saved as: ./data/cc-output-2a.txt')
    return MARK   

def detect_connected_components_sorted(MARK:np.ndarray):
    """
    Procedure which lists and sorts connected components from input 2D array MARK, generates text file with connected components ordered by pixel size.
    Generates image file of the top two largest

    Arguments:
        MARK (np.ndarray): 2D array representing connected components
    Outputs:
        cc-output-2b.txt: text file with connected components listed in decreasing order of pixel size (saved in ./data/)
        cc-top-2.jpg: binary image file of top two largest connected components (saved in ./data/)
    """
    R = int(np.max(MARK))                                                           # Total number of regions = Max value in MARK
    cdict = {}
    component_array = MARK.flatten().tolist()
    print('Sorting through connected components...')
    for index in range(1,R+1):
        occurrence = utils.countvalue(component_array, index)
        cdict.update({index:occurrence})                                            # Saves each connected component and its pixel size in dictionary (cdict)
    oc_array = utils.sorted(list(cdict.values()))                                   # Sorts pixel sizes in ascending order
    oc_array.reverse()                                                              # Reverses order of pixel sizes; now in descending order
    with open('data/cc-output-2b.txt','w') as f:
        for item in oc_array:
            index_key = [k for k,value in cdict.items() if value == item]           # For every pixel size, find connected component(s) associated with it
            for key in index_key:
                f.write(f"Connected component {key}, number of pixels = {item} \n")
        f.write(f"Total number of connected components = {R}")
    print('File saved as: ./data/cc-output-2b.txt')

    region1 = [k for k,value in cdict.items() if value == oc_array[0]]              # Finds largest connected component
    region2 = [k for k,value in cdict.items() if value == oc_array[1]]              # Finds second largest connected component
    MARK[np.where((MARK != region1) & (MARK != region2))] = [0]                     # Marks all pixels not in largest two components black
    MARK[np.where((MARK == region1) & (MARK == region2))] = [255]                   # Marks all pixels in largest two components white
    io.imsave('data/cc-top-2.jpg', MARK)
    print('File saved as: ./data/cc-top-2.jpg')


