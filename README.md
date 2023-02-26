## ACQUA system
An air-quality monitoring program with a text-based interface, written in Python. 

Project was submitted as coursework for the class ECM1400: Programming (September-December 2022) at The University of Exeter (BSc Computer Science)

![image](https://user-images.githubusercontent.com/53652096/221433962-ebbe7372-7372-4b72-96c0-4da3bc1e96d3.png)

___

### Module Information

#### Pollution Reporting Module

This module performs several time-aggregation operations on three monitoring station datasets. The user can choose the dataset, interval and pollutant for most of these operations to generate lists of the requested data. 


#### Mobility Intelligence Module

This module uses image processing on a colour-coded roadmap image to perform several pixel-mapping operations and detect connected components displayed in the image. An image is generated from the post-processed data according to the [specification details](https://github.com/adepge/ecm1400-project/blob/main/ecm1400-coursework/coursework-specification/ECM1400_Continuous_Assessment_2022_2.pdf). 

#### Realtime Monitoring Module

This module allows the user to grab data from the LondonAir API using its AirQuality API. The user can change the input parameters, provided they are able to provide a suitable [site code](https://github.com/lewisp6/london-air/blob/HEAD/site_codes.md) and corresponding [species code](https://github.com/adepge/ecm1400-project/blob/main/ecm1400-coursework/coursework-specification/species-codes.md) (for the air quality monitoring station). The user can change the period of time to pull data from the API by changing the start and end date. The data can be shown in a text-based table or graph. This implementation makes the system compatible with console environments. 

More information on each of the modules can be found in the [coursework specification](https://github.com/adepge/ecm1400-project/blob/main/ecm1400-coursework/coursework-specification/ECM1400_Continuous_Assessment_2022_2.pdf).

___

#### How to use (preview)

Requirements: [Anaconda](https://www.anaconda.com/) (contains the libraries needed for this program to run)

Using Anaconda Navigator, open VS Code (or any IDE that supports the libraries under Anaconda)
Download this repository and open the `/ecm1400-coursework` directory in the editor. Run `main.py` and follow instructions in the Python terminal. 

__**Warning:**__ This system is only used for testing. It is not designed for commercial use. All the code provided is as-is at the time of submission. 


___

#### __Comments__

This is the first project I've done in Python since doing IGCSE Computer Science, so it has been two years since I have obtained any relevant coding experience. Overall, reflecting on this first project, while it fulfilled most of the specification as intended, there are many improvements that could still be made - especially with the real-time monitoring module. For example, the site codes and species codes could have been iterated for the user within the system rather than resorting to manual input. The code is not consistently documented throughout, making it more difficult to read and explain some of the more complex functions. Therefore, I believe that this system is not suitable for general use.

This project is documented as a personal learning experience. 


