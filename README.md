
<p align="center" dir="ltr">
  <a href="/README.md">English</a> &nbsp; | &nbsp; <a href="/README.per.md">فارسی</a>
</p>


<br>


# LightKnightBBR Script V1.5.3 - for Fine-Tuned Setup :
- **Congestion Control:** <CODE>BBR</CODE>, <CODE>HYBLA</CODE>, <CODE>CUBIC</CODE>
- **Qdisc algorithms:** <CODE>FQ</CODE>, <CODE>FQ_CODEL</CODE>, <CODE>CAKE</CODE>
- **Optimizes TCP, UDP (via Qdisc algorithms), and more**
- **SpeedTest, Backup/Restore settings, and more options**
- **Robust installer:**
  - Automatic dependency installation (curl, git, jq, python3, etc.)
  - Handles PEP 668 (externally managed Python) by using a virtual environment for Python packages
  - Improved CLI UX: color-coded logging, validated prompts, and error handling
  - Safe privilege escalation and atomic file operations
  - Reliable asset download with error handling


<br>




----------------------------------------------------------------

<div align="left">
  <details>
    <summary><strong>Changelog</strong></summary>
    

<br>**V 1.5.2 :**

- From now on, see the changes in the release section.

**V 1.5 :**

- Appearance changes - outgoing messages
- Adding some optimization parameters to reduce network load without reducing standard security, suitable for a wide range of applications
- Improving the script and improving the performance of optimizers
- Ookla Speedtest optimization

**V 1.4 :**

- **New :**
- New Tcp Congestion Control : Hybla and Cubic
- Status option: displays the current Qdisk and Congestion Control algorithm of the operating system. (For the correct display, it is necessary to reboot the system after every change and configuration and check again)
- **Changed items :**
- Menu categories have changed :
- Option CakePlus > BBR Base > BBR + Cake
- Each of the Congestion Controls will have the possibility of activation with three types of Qdisk : FQ_CODE, FQ, CAKE.
- Appearance changes
- Improved performance

**V 1.3:**

- Optimization in the configuration of algorithms
- Algorithms will be applied only in the main interfaces to avoid further processing and reverse optimization.
- Optimization: fixing the detection problem and... in some operating systems.
- The performance of the recovery option was optimized. Be sure to restore and then reboot before applying the new settings.

**V 1.2:**
- Cake algorithm was added as an advanced Qos algorithm in combination with BBR:

**Cake will be used as a professional Qos algorithm in the queuing layer (Qdisc) and it will manage traffic queuing in the best possible way and minimize jitter and delay.
And BBR will be used in the congestion control layer as Tcp Congestion Control and provides the most optimal data transmission speed without causing congestion in TCP traffic.**
- In both installation modes, the original file is backed up.
- Improvements in the option to restore settings.
- Improvements in ecn applications
- Improvements in applying the algorithm
- Qos-qdisk algorithm will be applied on different interfaces, such as when the IP6 interface is separate.
- Improvements in installing packages
- Improvements in running speed test and...

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


**A project to configure BBR , HYBLA , CUBIC with three algorithms FQ , FQ_CODEL , CAKE and SpeedTest**

**BBR,HYBLA,CUBIC:**
- Full configuration
- Backup and restore applied settings

**Speed ​​test:**

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
    

- **Recommended OS:** Ubuntu 20.04+ (22+ preferred), Debian 10+ (11/12+ preferred)
- **Supported OS:** Ubuntu 18+, Debian 10+
- **Run as root or with sudo.**
- **Reboot required to apply changes.**
- **For best results, use matching algorithms on both ends of a tunnel.**
  </details>
</div>


------------------------------------------------------------------------------------------
If you need other features, or encounter any issues, please open an issue on GitHub.
------------


## Installation

Run the installer as root or with sudo:

```
bash <(curl -fsSL https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/install.sh)
```

The installer will:
- Check OS compatibility (Debian/Ubuntu)
- Install all required dependencies automatically
- Handle modern Python environments (PEP 668)
- Download and install the latest version of LightKnightBBR
- Provide robust, color-coded logging and validated prompts

## Usage

Run the script:

```
lbbr
```

To uninstall:

```
lbbr --uninstall
```

<br><br>


**❤️ special thanks to :**
 - https://github.com/Azumi67
 - https://t.me/OPIran_official
