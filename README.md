# Python Port Scanner

A fast, multi-threaded port scanner written in Python.

## Features implemented
- Multi-threaded scanning
- Banner grabbing
- Service detection
- Custom port ranges
- Output to file

## Usage

```bash
python scanner.py -t scanme.nmap.org -p 1-1000 -th 200 -o results.txt
