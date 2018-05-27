Virturian Challenge
============================
### Dependencies
#### Publisher and Subscriber
> python 3.4+

### Usage
1. Clone the repository
> git clone https://github.com/marcosmagno/Influxdata.git

2. Run
* HBMQTT (Server):  
Change the configuration file (conf). **computer_ip** default is 127.0.0.1.
bind: **computer_ip**

> hbmqtt -c conf -d

* Publisher (data generator and publisher) 
**server_ip** and **topic_publisher** default to 127.0.0.1 and sensor/temperatura, respectively. 
> python3 publisher.py

* Subscriber (data generator and publisher) 
**server_ip** and **topic_publisher** default to 127.0.0.1 and sensor/temperatura, respectively. 
> python3 subscriber.py --server-ip "**server_ip**" --topic "**topic_publisher**"
