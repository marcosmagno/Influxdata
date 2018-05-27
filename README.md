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
Change the configuration file (conf)
bind: **COMPUTER_IP**

> hbmqtt -c conf -d

* Publisher (data generator and publisher)  
> python3 publisher.py --server-ip "**Server IP**" --topic "**Topic_publisher**"

* Publisher (data generator and publisher)  
> python3 publisher.py 