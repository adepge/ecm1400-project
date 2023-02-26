## ACQUA system
An air-quality monitoring program with a text-based interface, written in Python. 

Project was submitted as coursework for the class ECM1400: Programming (September-December 2022) at The University of Exeter (BSc Computer Science)

![image](https://user-images.githubusercontent.com/53652096/221433962-ebbe7372-7372-4b72-96c0-4da3bc1e96d3.png)

___

### Module Information

#### Pollution Reporting Module

This module performs several time-aggregation operations on three monitoring station datasets. The user can choose the dataset, interval and pollutant for most of these operations to generate lists of the requested data. 


#### Mobility Intelligence Module

This module uses image processing on a colour-coded roadmap image to perform several pixel-mapping operations and detect connected components displayed in the image. An image is generated from the post-processed data according to the specification details. 

#### Realtime Monitoring Module

This module allows the user to grab data from the LondonAir API using its AirQuality API. The user can change the input parameters, provided they are able to provide a suitable [site code](https://github.com/lewisp6/london-air/blob/HEAD/site_codes.md) and corresponding species code (for the air quality monitoring station). The user can change the period of time to pull data from the API by changing the start and end date. The data can be shown in a text-based table or graph. This implementation makes the system compatible with console environments. 

More information on each of the modules can be found in the coursework specification.

