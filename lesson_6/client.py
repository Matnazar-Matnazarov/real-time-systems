#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real vaqt chat mijoz dasturi
Serverga ulanadi va real vaqt rejimida xabar almashadi.
"""

import socket
import threading
import sys

# Server sozlamalari
HOST = '127.0.0.1'
PORT = 12345

def receive(client):
    """
    Serverdan kelayotgan xabarlarni qabul qilish va ekranga chiqarish
    Args:
        client: Mijoz socket obyekti
    """
    while True:
        try:
            # Serverdan xabar olish
            message = client.recv(1024).decode('utf-8')
            
            if message == "NICK":
                # Server nickname so'rayapti
                nickname = input("Nickingizni kiriting: ").strip()
                if not nickname:
                    nickname = f"User_{id(client)}"
                client.send(nickname.encode('utf-8'))
                continue
            
            if message == "NICK_EXISTS":
                # Bu nickname allaqachon mavjud
                print("❌ Bu nickname allaqachon ishlatilmoqda. Boshqa nickname tanlang.")
                client.close()
                sys.exit(1)
            
            if message:
                # Oddiy xabar - ekranga chiqarish
                print(message)
            
        except ConnectionAbortedError:
            print("\n❌ Server bilan aloqa uzildi!")
            break
        except ConnectionResetError:
            print("\n❌ Server ulanishni yopdi!")
            break
        except Exception as e:
            print(f"\n❌ Xatolik: {e}")
            break
    
    client.close()
    sys.exit(0)

def write(client, nickname):
    """
    Serverga xabar yuborish
    Args:
        client: Mijoz socket obyekti
        nickname: Foydalanuvchi nomi
    """
    while True:
        try:
            # Foydalanuvchidan xabar olish
            message = input('')
            
            # Xabar yuborish
            if message.strip():
                formatted_message = f"{nickname}: {message}"
                client.send(formatted_message.encode('utf-8'))
            
        except EOFError:
            # Ctrl+D bosilganda
            print("\n👋 Chatdan chiqyapsiz...")
            break
        except KeyboardInterrupt:
            # Ctrl+C bosilganda
            print("\n👋 Chatdan chiqyapsiz...")
            break
        except Exception as e:
            print(f"\n❌ Xatolik: {e}")
            break
    
    try:
        client.close()
    except:
        pass
    sys.exit(0)

def main():
    """Asosiy funksiya"""
    print("=" * 60)
    print("💬 Real vaqt chat mijoz dasturi")
    print("=" * 60)
    print(f"🔗 Serverga ulanmoqda: {HOST}:{PORT}...")
    print("=" * 60)
    
    try:
        # Serverga ulanish
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        
        print("✅ Serverga muvaffaqiyatli ulandi!\n")
        
        # Serverdan "NICK" xabarini kutish
        nickname = None
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                nickname = input("Nickingizni kiriting: ").strip()
                if not nickname:
                    nickname = f"User_{id(client)}"
                client.send(nickname.encode('utf-8'))
                
                # Serverdan javob kutish
                response = client.recv(1024).decode('utf-8')
                if response == "NICK_EXISTS":
                    print("❌ Bu nickname allaqachon ishlatilmoqda. Boshqa nickname tanlang.")
                    client.close()
                    sys.exit(1)
                
                print(f"✅ Nickname: {nickname}")
                print("💬 Xabar yuborishni boshlang (chiqish uchun Ctrl+C):\n")
            else:
                # Agar "NICK" emas, boshqa xabar bo'lsa
                print(f"📨 {message}")
        except Exception as e:
            print(f"❌ Nickname olishda xatolik: {e}")
            client.close()
            sys.exit(1)
        
        # Xabarlarni qabul qilish uchun thread
        receive_thread = threading.Thread(target=receive, args=(client,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # Xabar yuborish (asosiy thread)
        write(client, nickname if nickname else "User")
        
    except ConnectionRefusedError:
        print("❌ Serverga ulanib bo'lmadi!")
        print("💡 Server ishga tushirilganligini tekshiring: python server.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Chatdan chiqyapsiz...")
        try:
            client.close()
        except:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        try:
            client.close()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()

