# USB Repair Agent — Project Specification

## Vision
A bootable USB stick that runs an AI-powered computer repair agent. Plug it into any broken PC, boot from it, and the agent diagnoses problems, runs repairs, and explains everything in plain English.

## Project Status
- **Phase 1:** Scaffolding & Planning (NOW)
- **Phase 2:** OS Selection & Base Image
- **Phase 3:** Agent Core & Diagnostics Engine
- **Phase 4:** Repair Tool Integration
- **Phase 5:** Build Automation & ISO Generation
- **Phase 6:** Testing & Demo

## Components

### 1. Bootable OS Layer
- Lightweight Linux live environment
- Auto-hardware detection on boot
- No installation required — runs entirely from USB

### 2. AI Agent Core
- Local LLM or rule-based diagnostic engine
- Conversational interface (talks like a human tech)
- Understands natural language repair requests

### 3. Diagnostics Module
- Hardware detection (CPU, RAM, disk, GPU)
- Disk health (SMART data, bad sectors)
- Memory testing
- Network diagnostics
- OS corruption detection

### 4. Repair Toolkit
- Disk recovery & data rescue
- Password reset (Windows & Linux)
- Malware scanning & removal
- Boot repair (GRUB, MBR, EFI)
- Driver issues
- Registry corruption (Windows)
- File system repair

### 5. Reporting Module
- Plain-English repair reports
- Before/after status
- Severity ratings
- Recommendations

## Directory Structure
```
usb-repair-agent/
├── docs/              # Specs, README, architecture
├── scripts/           # Build scripts, automation
├── agent/             # AI agent code
├── tools/             # Diagnostic & repair tool configs
├── config/            # Agent personality, LLM config
├── boot/              # Bootloader config, ISO build
└── tests/             # Hardware test profiles
```

## Notes from OWL
_(To be filled in when handoff arrives)_

## Notes from Self (Hermes/Echo)
- Project name used by OWL: "Liberty Agent" (per OWL's repo audit, May 29)
- GitHub repo `liberty-agent` exists but last updated May 10
- Jay confirmed this is a priority project — USB stick with repair agent for customer-facing use
