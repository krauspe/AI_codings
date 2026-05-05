#!/bin/bash
# make_ollama_offline_install.sh
# Creates an offline installable package for Ollama

set -e

# Support overriding architecture
ARCH=$(uname -m)
case "$ARCH" in
    x86_64) OLLAMA_ARCH="amd64" ;;
    aarch64|arm64) OLLAMA_ARCH="arm64" ;;
    *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

TARGET_ARCH=${1:-$OLLAMA_ARCH}

echo "Building Ollama offline installer for $TARGET_ARCH..."

# Create a temporary directory for packaging
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

OLLAMA_URL="https://ollama.com/download/ollama-linux-${TARGET_ARCH}.tgz"

echo "Downloading Ollama archive from $OLLAMA_URL..."
curl --fail --show-error --location --progress-bar -o "$TEMP_DIR/ollama-linux.tgz" "$OLLAMA_URL"

# Create the directory structure for the offline package
mkdir -p "$TEMP_DIR/ollama-offline"
mv "$TEMP_DIR/ollama-linux.tgz" "$TEMP_DIR/ollama-offline/"

echo "Creating offline install script..."
cat << 'EOF' > "$TEMP_DIR/ollama-offline/install.sh"
#!/bin/bash
# Offline installer for Ollama

set -e

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Please run as root (e.g. sudo ./install.sh)"
    exit 1
fi

echo "Installing Ollama offline..."

# Directories
OLLAMA_INSTALL_DIR="/opt/local/ollama"

echo "Creating installation directory $OLLAMA_INSTALL_DIR..."
mkdir -p "$OLLAMA_INSTALL_DIR"

echo "Extracting Ollama files to $OLLAMA_INSTALL_DIR..."
# Ollama tgz has bin/ and lib/ directories inside it
tar -xzf ollama-linux.tgz -C "$OLLAMA_INSTALL_DIR"

# Create ollama user and group
if ! id ollama >/dev/null 2>&1; then
    echo "Creating ollama user..."
    useradd -r -s /bin/false -U -m -d "$OLLAMA_INSTALL_DIR/data" ollama
fi

# Add to render/video groups if they exist (for GPU support)
if getent group render >/dev/null 2>&1; then
    usermod -a -G render ollama
fi
if getent group video >/dev/null 2>&1; then
    usermod -a -G video ollama
fi

echo "Setting up systemd service..."
cat << 'SERVICE_EOF' > /etc/systemd/system/ollama.service
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/opt/local/ollama/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/opt/local/ollama/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=default.target
SERVICE_EOF

if command -v systemctl >/dev/null; then
    echo "Starting Ollama service..."
    systemctl daemon-reload
    systemctl enable ollama
    systemctl restart ollama
    echo "Ollama installed and started successfully!"
    echo "Check its status with: systemctl status ollama"
else
    echo "systemctl not found. Ollama is installed but you must start it manually:"
    echo "sudo -u ollama /opt/local/ollama/bin/ollama serve"
fi
EOF

chmod +x "$TEMP_DIR/ollama-offline/install.sh"

FINAL_TAR="ollama-offline-${TARGET_ARCH}.tgz"
echo "Packaging everything into $FINAL_TAR..."
tar -czf "$FINAL_TAR" -C "$TEMP_DIR" ollama-offline

echo "=================================================="
echo "Done! The offline installer package is $FINAL_TAR."
echo "Transfer $FINAL_TAR to your offline machine and run:"
echo "  1. tar -xzf $FINAL_TAR"
echo "  2. cd ollama-offline"
echo "  3. sudo ./install.sh"
echo "=================================================="
