#!/bin/bash

echo "Starting bot..."
nohup python3 main.py > logs/bot.log 2>&1 &
echo "Bot is running in the background!"
