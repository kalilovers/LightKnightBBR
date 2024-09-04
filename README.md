# LightKnightBBR/SpeedTest
Long Live The Queen , special thanks to : 
https://github.com/Azumi67

اگر به ویژگی های دیگه ای نیاز دارید در قسمت issue اطلاع بدید .
If you need other features, let me know in the issue section

**A project to install BBR and SpeedTest**



- Currently, 2 types of BBR without manipulation have been added.
- Other methods will be added soon (with the ability to change the shape of the traffic)
- **afew Method For SpeedTest added:**

**2 Method For Bench.sh**

**Speedtest Between 2 server**

**Speedtest By ookla With the possibility of specifying a server**
![image](https://github.com/kalilovers/LightKnightBBR/assets/30160766/d14d4917-82d3-4006-9cad-082b6aeaa40b)



- **Read** : In my tests, the performance of the Codel type and even the simple one (FQ) caused **less disturbance and even using +Codel+** reduced the fluctuation and problems of local tunnels especially with **IPSec** and in many other cases.

So I **strongly recommend using FQ_Codel for IPSec And Local Tunnels**

A **reboot** is required to apply changes to the interface

------------

Run :

with python3 packages :
```
sudo apt update && sudo apt install -y python3 python3-pip && python3 <(curl -Ls https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/bbr.py --ipv4)
```
simple run :
```
python3 <(curl -Ls https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/bbr.py --ipv4)
```
