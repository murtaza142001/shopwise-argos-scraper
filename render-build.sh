#!/bin/bash

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install

echo "✅ Build complete"
