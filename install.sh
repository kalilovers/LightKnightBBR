#!/bin/bash
# Official Installation Script for LightKnightBBR (Public Version)
# Version: 1.3.2 (Python Installer Optimized)
# License: MIT

set -euo pipefail
trap 'echo "Error: Script failed at line $LINENO"; exit 1' ERR

REPO_OWNER="kalilovers"
REPO_NAME="LightKnightBBR"
INSTALL_DIR="/opt/lightbbr"
SCRIPT_NAME="lbbr"
MIN_DEBIAN=10
MIN_UBUNTU=18.04

MIN_PYTHON="3.6"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=6


RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Logging functions
log_info()   { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()   { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()  { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()   { echo -e "${CYAN}[STEP]${NC} $1"; }

# Validated prompt (yes/no)
prompt_confirm() {
    local prompt="$1 [y/N]: "
    local default="N"
    local answer
    while true; do
        read -r -p "$prompt" answer
        answer=${answer:-$default}
        case "$answer" in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
            *) log_warn "Please answer yes or no." ;;
        esac
    done
}

# Validated prompt (text, with default)
prompt_text() {
    local prompt="$1"
    local default="$2"
    local input
    read -r -p "$prompt [$default]: " input
    echo "${input:-$default}"
}

# ---------------------- Core Functions ----------------------
die() {
    log_error "$1"
    exit 1
}

check_os() {
    log_step "Checking OS compatibility..."
    
    if ! [[ -f /etc/os-release ]]; then
        die "Unsupported operating system"
    fi

    source /etc/os-release
    case $ID in
        debian)
            if (( $(echo "$VERSION_ID < $MIN_DEBIAN" | bc -l) )); then
                die "Debian $VERSION_ID is not supported (Minimum: Debian $MIN_DEBIAN)"
            fi
            ;;
        ubuntu)
            if (( $(echo "$VERSION_ID < $MIN_UBUNTU" | bc -l) )); then
                die "Ubuntu $VERSION_ID is not supported (Minimum: Ubuntu $MIN_UBUNTU)"
            fi
            ;;
        *)
            die "Only Debian/Ubuntu distributions are supported"
            ;;
    esac
}

check_privileges() {
    if [[ $EUID -ne 0 ]]; then
        if ! sudo -n true 2>/dev/null; then
            log_warn "This operation requires root privileges."
            if prompt_confirm "Do you want to continue and grant sudo privileges?"; then
                sudo -v || die "Failed to get sudo privileges"
            else
                die "User declined privilege escalation."
            fi
        fi
    fi
}



#=====================================
#### Installing dependencies

install_dependencies() {
    export DEBIAN_FRONTEND=noninteractive
    export APT_LISTCHANGES_FRONTEND=none

    local PKGS=(
        curl wget sudo ed
        iproute2 iptables
        python3 python3-pip python3-venv
        jq git
    )

    log_step "Updating package lists..."
    sudo apt-get update -qq 2>/dev/null || {
    log_warn "Some package lists failed to update, continuing anyway..."
    }

    log_step "Installing required packages..."
    sudo apt-get install -y --no-install-recommends -qq \
        -o Dpkg::Options::="--force-confold" \
        -o Dpkg::Options::="--force-unsafe-io" \
        "${PKGS[@]}" 2>/dev/null || {
    log_warn "Some packages may have failed to install."
    }
#=====================================




#=====================================
#### Installing python3 packs

    log_step "Checking Python version..."
	local python_version python_major python_minor
	python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" || die "Python3 not found")
	python_major=$(python3 -c "import sys; print(sys.version_info.major)")
	python_minor=$(python3 -c "import sys; print(sys.version_info.minor)")

	if [ "$python_major" -lt 3 ]; then
		die "Python version $python_version is not supported (Minimum required: 3.9)"
	elif [ "$python_major" -eq 3 ] && [ "$python_minor" -lt 9 ]; then
		die "Python version $python_version is not supported (Minimum required: 3.9)"
	fi


    log_step "Ensuring $INSTALL_DIR exists and is writable..."
    sudo mkdir -p "$INSTALL_DIR" && sudo chmod 755 "$INSTALL_DIR"

    log_step "Installing Python packages..."

    # Detect PEP 668 (externally managed environment)
    if python3 -c "import sys; sys.exit(hasattr(sys, 'externally_managed'))"; then
        log_warn "Detected PEP 668: Python is externally managed. Using virtual environment for pip installs."
        local venv_dir="$INSTALL_DIR/venv"
        sudo python3 -m venv "$venv_dir"
        sudo -H "$venv_dir/bin/pip" install --upgrade pip
        sudo -H "$venv_dir/bin/pip" install requests packaging
        log_info "Python packages installed in virtual environment: $venv_dir"
    else
        try_pip_install() {
            python3 -m pip install --user --disable-pip-version-check --no-warn-script-location "$@" -q requests packaging
        }
        if ! try_pip_install; then
            log_warn "Retrying with aliyun mirror..."
            if ! try_pip_install -i https://mirrors.aliyun.com/pypi/simple/; then
                log_warn "Trying with --break-system-packages..."
                if ! try_pip_install --break-system-packages; then
                    log_warn "Retrying with aliyun mirror and --break-system-packages..."
                    try_pip_install --break-system-packages -i https://mirrors.aliyun.com/pypi/simple/ || \
                        die "Python package installation failed!"
                fi
            fi
        fi
    fi

    log_step "Verifying core components..."
    local critical_commands=("python3" "curl" "git" "jq")
    local missing=()
    
    for cmd in "${critical_commands[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        die "Missing critical components: ${missing[*]}"
    fi

    log_info "All critical dependencies verified!"
}

#=====================================





fetch_latest_release() {
    log_step "Fetching latest release info..."
    local api_url="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest"
    
    local release_info
    if ! release_info=$(curl -4 -fsSL --max-time 30 "$api_url" 2>/dev/null); then
    log_warn "IPv4 failed, trying IPv6..."
        release_info=$(curl -6 -fsSL --max-time 30 "$api_url" 2>/dev/null) || die "Failed to connect to GitHub"
    fi

    if ! jq -e '.assets' <<< "$release_info" >/dev/null; then
        die "Invalid GitHub API response"
    fi

    local asset_url
    asset_url=$(echo "$release_info" | jq -r '.assets[] | select(.name == "bbr.py") | .browser_download_url')
    if [[ -z "$asset_url" || "$asset_url" == "null" ]]; then
        die "Asset 'bbr.py' not found in latest release."
    fi
    echo "$asset_url"
}

setup_application() {
    log_step "Setting up LightKnightBBR..."
    
    sudo mkdir -p "$INSTALL_DIR" || die "❌ Directory creation failed"
    sudo chmod 755 "$INSTALL_DIR"

    log_step "Downloading latest release..."
    local download_url
    download_url=$(fetch_latest_release | tail -n 1 | tr -d '\r\n')
    if [[ -z "$download_url" ]]; then
        die "❌ Could not determine download URL for bbr.py"
    fi

    local temp_file
    temp_file=$(sudo mktemp -p "$INSTALL_DIR" bbr.py.XXXXXXXXXX)

    log_step "Downloading bbr.py from $download_url to $temp_file"
    if ! sudo curl -4 -fsSL --retry 3 --retry-delay 2 --max-time 60 -o "$temp_file" "$download_url"; then
        log_warn "IPv4 download failed, trying IPv6..."
        if ! sudo curl -6 -fsSL --retry 3 --retry-delay 2 --max-time 60 -o "$temp_file" "$download_url"; then
            log_error "Failed to download bbr.py from $download_url via both IPv4 and IPv6."
            sudo rm -f "$temp_file"
            die "Download of bbr.py failed. Check network connectivity and release asset URL."
        fi
    fi

    local backup_file
    if [[ -f "${INSTALL_DIR}/bbr.py" ]]; then
        if prompt_confirm "A previous version of bbr.py exists. Do you want to back it up and replace it?"; then
            backup_file="${INSTALL_DIR}/bbr.py.bak.$(date +%s)"
            sudo mv -f "${INSTALL_DIR}/bbr.py" "$backup_file" || die "❌ Backup failed"
            log_info "Backup created: $(basename \"$backup_file\")"
        else
            die "User declined to replace existing bbr.py."
        fi
    fi

    if sudo mv -f "$temp_file" "${INSTALL_DIR}/bbr.py"; then
        sudo rm -f "$temp_file"
    else
        [[ -n "$backup_file" ]] && sudo mv -f "$backup_file" "${INSTALL_DIR}/bbr.py"
        sudo rm -f "$temp_file"
        die "❌ Atomic replacement failed"
    fi

    sudo chmod 755 "${INSTALL_DIR}/bbr.py"
    sudo ln -sfT "${INSTALL_DIR}/bbr.py" "/usr/local/bin/${SCRIPT_NAME}" || die "❌ Symlink creation failed"

    sudo rm -f "${INSTALL_DIR}"/bbr.py.bak.* 2>/dev/null

    log_info "Successfully installed latest version!"
}

main() {
    check_os
    check_privileges
    install_dependencies
    setup_application

    log_info "Github : https://github.com/${REPO_OWNER}/${REPO_NAME}"
    log_info "Run With : ${SCRIPT_NAME}"
}

main
