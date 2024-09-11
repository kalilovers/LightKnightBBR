# LightKnightBBR/SpeedTest V1.1
special thanks to : 
https://github.com/Azumi67

----------------------------------------------------------------
[English](/README.md)   |   [فارسی](/README.per.md)

<div align="left">
  <details>
    <summary><strong>Changelog</strong></summary>
    
**V 1.1 :**
- Optimized
- Checking the compatibility of the operating system and the kernel
- Making changes for modern distributions and alternative methods for older systems in Python
- Check and install required packages
- ECN (Explicit Congestion Notification) activation
- The queuing algorithm (fq or fq_codel) for the network interface and qdisk in the operating system and network cards that do not support or are not completely set due to reasons such as the old network card, etc. will be set by automatic checking by the script = **More optimization**
Also, the feedback messages have been improved so that users are better informed about the status of the execution of the steps.

  </details>
</div>

------------------------------------------------------------------------------------------

<div align="left">
  <details>
    <summary><strong>Description</strong></summary>


**A project to config BBR and run SpeedTest**

- **BBR :**
- Full config BBR settings
- Backup and restore applied settings of BBR
- Currently, 2 types of BBR without manipulation have been added.
- Other methods will be added soon (with the ability to change the shape of the traffic)

- **speedtest :**

- 2 Method For Bench.sh speedtest

- Speedtest Between 2 server With Iperf3

- Speedtest By ookla With the possibility of specifying a server

![image](https://github.com/kalilovers/LightKnightBBR/assets/30160766/d14d4917-82d3-4006-9cad-082b6aeaa40b)
  </details>
</div>

------------------------------------------------------------------------------------------

<div align="left">
  <details>
    <summary><strong>Tips</strong></summary>
    
- **My suggestion: use **fq_codel** and at least Ubuntu version 20.04 and above and Debian 10 and above (because bbrv2 is used) especially for vpn, games, calls, etc.**
- Supported operating systems » Ubuntu version 18 and above - Debian 10 and above
-  run in root user or with **sudo** 
- A **reboot** is required to apply changes to the interface
  </details>
</div>


------------------------------------------------------------------------------------------
If you need other features, or there is a problem, let me know in the issue section
------------

Run :

With Installation Python3 packages :
```
sudo apt update && sudo apt install -y python3 python3-pip && python3 <(curl -Ls https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/bbr.py --ipv4)
```
simple run :
```
python3 <(curl -Ls https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/bbr.py --ipv4)
```
