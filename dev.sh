#!/usr/bin/env bash

# dev.sh - SubbaDev Local Development Orchestration Script
# Features: Colorful logs, auto venv detection, modular commands (setup, extract, compile, serve, dev)

set -e

# --- Color Scheme ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# --- Virtual Environment Handling ---
ensure_venv() {
    if [ ! -d "venv" ]; then
        log_warn "Virtual environment 'venv' not found. Bootstrapping a new one..."
        python3 -m venv venv
        log_success "Virtual environment created."
    fi
    
    log_info "Activating Python virtual environment..."
    source venv/bin/activate
}

# --- Subcommands ---

cmd_setup() {
    ensure_venv
    log_info "Installing / upgrading dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    log_success "Dependency installation completed."
}

cmd_extract() {
    ensure_venv
    log_info "Step 1: Extracting resume data from SubbaTaniparti.docx..."
    python build_resume.py
    
    log_info "Step 2: Programmatically bootstrapping self-hosted WOFF2 webfonts..."
    python download_fonts.py
    
    log_info "Step 3: Creating Pillow-rendered social card graphic..."
    python generate_social_card.py
    
    log_success "All extraction and asset generation complete."
}

cmd_compile() {
    ensure_venv
    log_info "Compiling Pelican site to 'output/' using local relative configurations..."
    pelican content -o output -s pelicanconf.py
    log_success "Pelican compilation complete."
}

cmd_serve() {
    ensure_venv
    log_info "Starting Pelican local development server at http://localhost:8000..."
    log_info "Press Ctrl+C to terminate the server."
    pelican -l -p 8000
}

cmd_dev() {
    ensure_venv
    # Clean and extract first
    cmd_extract
    cmd_compile
    
    log_info "Launching hot-reloading development environment (auto-regenerates on file changes)..."
    log_info "Access locally at: http://localhost:8000"
    log_info "Press Ctrl+C to terminate."
    
    # Run with auto-reload (-r) and listening server (-l)
    pelican -r -l -p 8000
}

cmd_help() {
    echo -e "SubbaDev Development Suite Orchestrator"
    echo -e "Usage: ./dev.sh [command]"
    echo -e ""
    echo -e "Available Commands:"
    echo -e "  ${CYAN}setup${NC}    Initialize virtual environment and install pip dependencies"
    echo -e "  ${CYAN}extract${NC}  Run extraction engines (parse .docx, fetch fonts, draw social card)"
    echo -e "  ${CYAN}compile${NC}  Execute Pelican build to output directory"
    echo -e "  ${CYAN}serve${NC}    Launch standard local preview webserver on port 8000"
    echo -e "  ${CYAN}dev${NC}      Run hot-reloading dev environment (extracts -> compiles -> serves with watch)"
    echo -e "  ${CYAN}help${NC}     Show this help message"
    echo -e ""
}

# --- Main Entrypoint ---

case "$1" in
    setup)
        cmd_setup
        ;;
    extract)
        cmd_extract
        ;;
    compile)
        cmd_compile
        ;;
    serve)
        cmd_serve
        ;;
    dev)
        cmd_dev
        ;;
    help|--help|-h|"")
        cmd_help
        ;;
    *)
        log_error "Unknown command: $1"
        cmd_help
        exit 1
        ;;
esac
