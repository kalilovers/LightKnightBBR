import os
import shutil
import platform
import subprocess
from colorama import init, Fore, Style

def logo():
    logo_path = "/etc/logo.sh"
    try:
        subprocess.run(["bash", "-c", logo_path], check=True)
    except subprocess.CalledProcessError as e:
        return e

    return None

if os.geteuid() != 0:
    print("\033[91mThis script must be run as root. Please use sudo -i.\033[0m")
    sys.exit(1)

def show_main_menu():
    os.system("clear")
    logo()
    print("\033[93m  \033[1m  \nV 1.1  \033[0m")
    print("\033[92m  \nSpecial thanks to the Queen  \033[0m")
    print("\033[96m  \nView the project on GitHub: https://github.com/kalilovers  \033[0m")
    print("\033[91m  \nLightKnight Simple Script For Simple and Stable BBR  \033[0m")
    print("\033[94m  1.  \033[97m  BBR Fq  \033[0m")
    print("\033[94m  2.  \033[97m  BBR Fq_Codel (Recommend - Especially For IPSec And Local TUNS)  \033[0m")
    print("\033[94m  3.  \033[97m  Restore Default BBR/Settings  \033[0m")
    print("\033[94m  4.  \033[97m  Speed Test  \033[0m")
    print("\033[94m  0.  \033[97m  Exit  \033[0m")

def show_fq_menu():
    print("\033[96m  \nFq  \033[0m")
    print("\033[94m  1.  \033[97m  Delete Old File Then Setup (Backup)  \033[0m")
    print("\033[94m  2.  \033[97m  Setup Without Delete  \033[0m")
    print("\033[94m  0.  \033[97m  Back  \033[0m")

def show_fq_codel_menu():
    print("\033[96m  \nFq_Codel  \033[0m")
    print("\033[94m  1.  \033[97m  Delete Old File Then Setup (Backup)  \033[0m")
    print("\033[94m  2.  \033[97m  Setup Without Delete  \033[0m")
    print("\033[94m  0.  \033[97m  Back  \033[0m")

def show_speed_test_menu():
    print("\033[96m  \nSpeed Test  \033[0m")
    print("\033[94m  1.  \033[97m  Bench Method1  \033[0m")
    print("\033[94m  2.  \033[97m  Bench Method2  \033[0m")
    print("\033[94m  3.  \033[97m  Iperf3 (Between 2 Server)  \033[0m")
    print("\033[94m  4.  \033[97m  Speedtest Ookla  \033[0m")
    print("\033[94m  0.  \033[97m  Back  \033[0m")

def show_iperf_menu():
    print("\033[96m  \nChoose which one you are:  \033[0m")
    print("\033[94m  1.  \033[97m  Client (iran or...)  \033[0m")
    print("\033[94m  2.  \033[97m  Server (Kharej/Traget or...)  \033[0m")
    print("\033[94m  0.  \033[97m  Back  \033[0m")

def prompt_restart():
    while True:
        choice = input("\033[93m  The mission was successfully completed. Do you want to restart? (Requi\033[91m) Yes or No:   \033[0m").lower()
        if choice in ['n', 'no']:
            break
        elif choice in ['y', 'yes']:
            os.system("reboot")
            break
        else:
            print("\033[91m  Please enter Yes or No.  \033[0m")

def check_kernel_and_os():
    print("\033[96m Checking the compatibility of operating system and kernel...\033[0m")
    try:
        with open("/etc/os-release", "r") as f:
            lines = f.readlines()
        distro = ""
        for line in lines:
            if line.startswith("ID="):
                distro = line.strip().split("=")[1].strip('"').lower()
                break
    except FileNotFoundError:
        try:
            distro_info = platform.linux_distribution()
            distro = distro_info[0].lower()
        except AttributeError:
            distro = ""

    if distro not in ['ubuntu', 'debian']:
        print("\033[96m The operating system is not supported. Only Ubuntu and Debian are supported.\033[0m")
        return False

    kernel_version = platform.release()
    version_numbers = kernel_version.split(".")
    try:
        kernel_major = int(version_numbers[0])
        kernel_minor = int(version_numbers[1])
    except (IndexError, ValueError):
        print(f"Kernel version {kernel_version} could not be detected.")
        return False

    if kernel_major > 4 or (kernel_major == 4 and kernel_minor >= 9):
        print(f"The kernel version is compatible with BBR.")
        return True
    else:
        print(f"Kernel version {kernel_version} is not supported. Requires version 4.9 or higher.")
        return False

import os
import shutil
import subprocess

def install_required_packages():
    print("\033[93mChecking and installing required packages...\033[0m")
    required_packages = ['iproute2', 'iptables']
    missing_packages = []
    for package in required_packages:
        result = subprocess.run(['dpkg', '-s', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            missing_packages.append(package)
    if missing_packages:
        print(f"\033[93mThe following packages are not installed and are being installed: {', '.join(missing_packages)}\033[0m")
        subprocess.run(['apt', 'update'])
        subprocess.run(['apt', 'install', '-y'] + missing_packages)
    else:
        print("\033[92mAll required packages are installed.\033[0m")
    return True

def activate_ecn():
    print("\033[93mActivating ECN...\033[0m")
    try:
        with open("/proc/sys/net/ipv4/tcp_ecn", "r") as f:
            ecn_status = f.read().strip()
        if ecn_status == "1":
            print("\033[92mECN is already active.\033[0m")
            return True
    except:
        pass

    try:
        with open("/etc/sysctl.conf", "a") as f:
            f.write("\n# Enable ECN\n")
            f.write("net.ipv4.tcp_ecn = 1\n")
        subprocess.run(['sysctl', '-p'])
        print("\033[92mECN Activated successfully.\033[0m")
        return True
    except Exception as e:
        print(f"\033[91mECN activation error: {e}\033[0m")
        return False
    
def setup_qdisc(algorithm):
    print("\033[93mSetting the queuing algorithm...\033[0m")
    try:
        interfaces = os.listdir("/sys/class/net/")
        if 'lo' in interfaces:
            interfaces.remove('lo')
        if not interfaces:
            print("\033[91mNetwork interface not found.\033[0m")
            return False
        interface = interfaces[0]
    except Exception as e:
        print(f"\033[91mError identifying the network interface: {e}\033[0m")
        return False

    try:
        subprocess.run(['tc', 'qdisc', 'replace', 'dev', interface, 'root', algorithm], check=True)
        print(f"\033[92mThe {algorithm} queuing algorithm was set on the {interface} interface.\033[0m")
        return True
    except subprocess.CalledProcessError:
        print(f"\033[91mError in setting the queuing algorithm {algorithm}.\033[0m")
        return False

def make_qdisc_persistent(algorithm):
    print("\033[93mCreating systemd service to preserve qdisc settings after reboot...\033[0m")
    service_content = f"""[Unit]
Description=Set qdisc {algorithm} on network interface
After=network.target

[Service]
Type=oneshot
ExecStart=/sbin/tc qdisc replace dev eth0 root {algorithm}
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
"""
    service_path = "/etc/systemd/system/qdisc-setup.service"
    try:
        with open(service_path, "w") as f:
            f.write(service_content)
        subprocess.run(['systemctl', 'daemon-reload'])
        subprocess.run(['systemctl', 'enable', 'qdisc-setup.service'])
        subprocess.run(['systemctl', 'start', 'qdisc-setup.service'])
        print("\033[92mThe systemd service was successfully created and activated.\033[0m")
        return True
    except Exception as e:
        print(f"\033[91mError creating systemd service: {e}\033[0m")
        return False

def configure_bbr(algorithm):
    print("\033[93mSetting up BBR...\033[0m")
    try:
        with open("/etc/sysctl.conf", "a") as f:
            f.write(f"\n# {algorithm} Light Knight\n")
            f.write(f"net.core.default_qdisc = {algorithm}\n")
            f.write("net.ipv4.tcp_congestion_control = bbr\n")
        subprocess.run(['sysctl', '-p'])
        print("\033[92mBBR settings applied.\033[0m")
    except Exception as e:
        print(f"\033[91mError in setting BBR: {e}\033[0m")
        return False

    if not setup_qdisc(algorithm):
        return False

    if not make_qdisc_persistent(algorithm):
        return False

    return True

def delete_old_file_then_setup(algorithm):
    print("\033[93mDeleting old files and setting new (+Backup)...\033[0m")
    backup_path = "/etc/sysctl.confback"
    original_path = "/etc/sysctl.conf"

    try:
        if os.path.exists(original_path):
            shutil.copy(original_path, backup_path)
            os.remove(original_path)
            print("\033[92mThe old sysctl.conf file was deleted and backed up.\033[0m")
    except Exception as e:
        print(f"\033[91mError deleting old files: {e}\033[0m")
        return False

    if configure_bbr(algorithm):
        prompt_restart()
    else:
        print("\033[91mBBR settings encountered a problem.\033[0m")
    return True

def setup_without_delete(algorithm):
    print("\033[93mSetting up without deleting old files...\033[0m")
    if configure_bbr(algorithm):
        prompt_restart()
    else:
        print("\033[91mBBR settings encountered a problem.\033[0m")
    return True

def restore():
    print("\033[93mRestoring default settings...\033[0m")
    backup_path = "/etc/sysctl.confback"
    original_path = "/etc/sysctl.conf"

    try:
        if os.path.exists(original_path):
            os.remove(original_path)
            print("\033[92mRemoved the original sysctl.conf file.\033[0m")
    except Exception as e:
        print(f"\033[91mError deleting main sysctl.conf file: {e}\033[0m")
        return False

    try:
        if os.path.exists(backup_path):
            os.rename(backup_path, original_path)
            print("\033[92mRestored sysctl.conf backup.\033[0m")
    except Exception as e:
        print(f"\033[91mError restoring sysctl.conf backup: {e}\033[0m")
        return False

    service_path = "/etc/systemd/system/qdisc-setup.service"
    try:
        if os.path.exists(service_path):
            subprocess.run(['systemctl', 'disable', 'qdisc-setup.service'])
            os.remove(service_path)
            subprocess.run(['systemctl', 'daemon-reload'])
            print("\033[92mThe systemd service related to qdisc was removed.\033[0m")
    except Exception as e:
        print(f"\033[91mError deleting service systemd: {e}\033[0m")

    try:
        subprocess.run(['tc', 'qdisc', 'delete', 'dev', 'eth0', 'root'], check=True)
        print("\033[92mDefault qdisc settings are restored.\033[0m")
    except subprocess.CalledProcessError:
        print("\033[91mDefault qdisc settings could not be reset or are not currently set.\033[0m")

    try:
        subprocess.run(['sysctl', '-p'])
        print("\033[92msysctl settings applied.\033[0m")
    except Exception as e:
        print(f"\033[91mError applying settings sysctl: {e}\033[0m")

    prompt_restart()
    return True

def run_bench_method1():
    print("\033[93mRunning Bench Method1...\033[0m")
    os.system("wget -qO- bench.sh | bash")

def run_bench_method2():
    print("\033[93mRunning Bench Method2...\033[0m")
    os.system("curl -Lso- bench.sh | bash")

def run_iperf_client():
    print("\033[93m Starting Iperf3 as client...\033[0m")
    os.system("apt update")
    os.system("apt install iperf3 -y")
    os.system("ufw allow 5201")
    server_ip = input("\033[93m What is the IP address of your target server? Enter Your Target IP: \033[0m")
    os.system(f"iperf3 -c {server_ip} -i 1 -t 10 -P 20")
    input("\033[93mThe download speed test was done. To test the upload speed, press Enter...\033[0m")
    os.system(f"iperf3 -c {server_ip} -R -i 1 -t 10 -P 20")
    input("\033[93m The upload speed test was done. To Back to the menu, press Enter...\033[0m")

def run_iperf_server():
    print("\033[93mStarting Iperf3 as server...\033[0m")
    os.system("apt update")
    os.system("apt install iperf3 -y")
    os.system("ufw allow 5201")
    print("\033[93mRun Iperf3 as server...\033[0m")
    os.system("iperf3 -s")
    input("\033[93m You are active as a server, please do not log out. If it is finished, to Back to the menu, press Enter... \033[0m")

def run_speedtest_ookla():
    print("\033[93m Downloading and running Ookla Speedtest... \033[0m")
    os.system("wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz")
    os.system("tar zxvf ookla-speedtest-1.2.0-linux-x86_64.tgz")
    server_num = input("\033[93m Enter your ookla-server number. Or press Enter to use the Amsterdam server by default: \033[0m")
    if not server_num:
        server_num = "54746"
    os.system(f"./speedtest -s {server_num}")
    input("\033[93m SpeedTest Done, please do not log out. If it is finished, to Back to the menu, press Enter... \033[0m")

def main():
    try:
        while True:
            show_main_menu()
            choice = input("\033[93m Please enter your choice: \033[0m")

            if choice == '1':
                while True:
                    show_fq_menu()
                    fq_choice = input("\033[93m Please enter your choice: \033[0m")
                    if fq_choice == '1':
                        if check_kernel_and_os():
                            install_required_packages()
                            activate_ecn()
                            delete_old_file_then_setup("fq")
                    elif fq_choice == '2':
                        if check_kernel_and_os():
                            install_required_packages()
                            activate_ecn()
                            setup_without_delete("fq")
                    elif fq_choice == '0':
                        break
                    else:
                        print("\033[91m Invalid choice, please try again.\033[0m")
            elif choice == '2':
                while True:
                    show_fq_codel_menu()
                    fq_codel_choice = input("\033[93m Please enter your choice: \033[0m")
                    if fq_codel_choice == '1':
                        if check_kernel_and_os():
                            install_required_packages()
                            activate_ecn()
                            delete_old_file_then_setup("fq_codel")
                    elif fq_codel_choice == '2':
                        if check_kernel_and_os():
                            install_required_packages()
                            activate_ecn()
                            setup_without_delete("fq_codel")
                    elif fq_codel_choice == '0':
                        break
                    else:
                        print("\033[91m Invalid choice, please try again.\033[0m")
            elif choice == '3':
                restore()
            elif choice == '4':
                while True:
                    show_speed_test_menu()
                    speed_test_choice = input("\033[93m Please enter your choice: \033[0m")
                    if speed_test_choice == '1':
                        run_bench_method1()
                    elif speed_test_choice == '2':
                        run_bench_method2()
                    elif speed_test_choice == '3':
                        while True:
                            show_iperf_menu()
                            iperf_choice = input("\033[93m Please enter your choice: \033[0m")
                            if iperf_choice == '1':
                                run_iperf_client()
                            elif iperf_choice == '2':
                                run_iperf_server()
                            elif iperf_choice == '0':
                                break
                            else:
                                print("\033[91m Invalid choice, please try again.\033[0m")
                    elif speed_test_choice == '4':
                        run_speedtest_ookla()
                    elif speed_test_choice == '0':
                        break
                    else:
                        print("\033[91m Invalid choice, please try again.\033[0m")
            elif choice == '0':
                print("\033[92m Goodbye!\033[0m")
                break
            else:
                print("\033[91m Invalid choice, please try again.\033[0m")
    except KeyboardInterrupt:
        print("\033[91m \nScript interrupted. Exiting gracefully.\033[0m")
        exit(0)

if __name__ == "__main__":
    main()
