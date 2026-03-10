#!/bin/bash

echo "Đang khởi động bot..."
nohup python3 main.py > logs/bot.log 2>&1 &
echo "Bot đang chạy nền!"
