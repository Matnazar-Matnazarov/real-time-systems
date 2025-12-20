#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real vaqt chat dasturi - Asosiy fayl
Bu fayl foydalanuvchiga qaysi dasturni ishga tushirishni tanlash imkonini beradi.
"""

import sys
import os

def print_menu():
    """Menu ko'rsatish"""
    print("=" * 60)
    print("💬 Real vaqt chat dasturi")
    print("=" * 60)
    print("1. Server ishga tushirish")
    print("2. Mijoz (Client) ishga tushirish")
    print("3. Chiqish")
    print("=" * 60)

def run_server():
    """Server dasturini ishga tushirish"""
    try:
        from server import receive
        receive()
    except ImportError:
        print("❌ server.py fayl topilmadi!")
    except KeyboardInterrupt:
        print("\n✅ Server to'xtatildi")

def run_client():
    """Client dasturini ishga tushirish"""
    try:
        from client import main
        main()
    except ImportError:
        print("❌ client.py fayl topilmadi!")
    except KeyboardInterrupt:
        print("\n✅ Mijoz to'xtatildi")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line argument orqali
        if sys.argv[1] == "server":
            run_server()
        elif sys.argv[1] == "client":
            run_client()
        else:
            print("❌ Noto'g'ri argument!")
            print("💡 Foydalanish: python main.py [server|client]")
    else:
        # Interaktiv menu
        while True:
            print_menu()
            choice = input("\nTanlov kiriting (1-3): ").strip()
            
            if choice == "1":
                print("\n🚀 Server ishga tushmoqda...\n")
                run_server()
                break
            elif choice == "2":
                print("\n💬 Mijoz ishga tushmoqda...\n")
                run_client()
                break
            elif choice == "3":
                print("👋 Xayr!")
                sys.exit(0)
            else:
                print("❌ Noto'g'ri tanlov! 1, 2 yoki 3 ni kiriting.\n")
