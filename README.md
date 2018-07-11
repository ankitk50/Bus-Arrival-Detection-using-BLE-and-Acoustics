# Bus-Arrival-Detection-using-BLE-and-Acoustics
The project focuses on detection of arrival of a bus at a bus stop. 
## Hardware used:
1.Raspberry pi 2. Bluetooth Low energy (BLE) beacons 3. Speakers 4. LCD display
## Softwares used:
1. Raspian 2. Python
## Methodology:
1. Rasperry Pi is installed at the bus stop, keeps scanning nearby beacons installed in the buses. 
2. Once a beacon is detected, bus details are fetched from the beacon.
3. An acoustic classifier extracts an audio sample of 10 secs and determines the exact arrival of the bus.The classifier has been trained with different audio samples of the bus.
4. Once the classifier pridicts the arrival of the bus, announcement of the bus details is made on the bus stop.
## Code file
- A webpage in data_update_portal folder is used to update/view the database of the details of the bus such as the route, frequency of arrival.
-main_final_xyz is various versions of the main code running in raspberry pi. 
-MP3 and Text files were used for speech synthesis purpose.
-acoustic model is implemented in acoustic folder.
