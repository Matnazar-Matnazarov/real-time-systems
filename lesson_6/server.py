#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real vaqt chat serveri
Socket dasturlash orqali bir nechta mijozlarni qabul qiladi va xabarlarni yuboradi.
"""

import socket
import threading
from datetime import datetime

# Server sozlamalari
HOST = '127.0.0.1'   # Lokal IP (localhost)
PORT = 12345         # Port raqami

# Server soketi yaratish
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Portni qayta ishlatish
server.bind((HOST, PORT))
server.listen()

# Global o'zgaruvchilar
clients = []        # Mijozlar ro'yxati
nicknames = []      # Mijozlarning nomlari
lock = threading.Lock()  # Thread-safe operatsiyalar uchun

def get_timestamp():
    """Joriy vaqtni formatlangan ko'rinishda qaytaradi"""
    return datetime.now().strftime("%H:%M:%S")

def broadcast(message, sender_client=None):
    """
    Barcha mijozlarga xabar yuborish
    Args:
        message: Yuboriladigan xabar (bytes)
        sender_client: Xabar yuboruvchi mijoz (uni o'ziga yubormaslik uchun)
    """
    with lock:
        for client in clients:
            if client != sender_client:
                try:
                    client.send(message)
                except:
                    # Agar mijozga yuborib bo'lmasa, ro'yxatdan olib tashlash
                    if client in clients:
                        index = clients.index(client)
                        clients.remove(client)
                        if index < len(nicknames):
                            nickname = nicknames[index]
                            nicknames.remove(nickname)
                        client.close()

def handle(client):
    """
    Mijozdan kelayotgan xabarlarni qabul qilish va boshqalarga yuborish
    Args:
        client: Mijoz socket obyekti
    """
    while True:
        try:
            # Mijozdan xabar olish
            message = client.recv(1024)
            
            if not message:
                # Bo'sh xabar - mijoz ulanishni uzgan
                raise Exception("Client disconnected")
            
            # Xabarni barcha mijozlarga yuborish
            broadcast(message, sender_client=client)
            
        except Exception as e:
            # Xatolik yoki ulanish uzilgan
            try:
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames[index]
                nicknames.remove(nickname)
                
                # Boshqa mijozlarga xabar yuborish
                leave_message = f"[{get_timestamp()}] {nickname} chatdan chiqdi!".encode('utf-8')
                broadcast(leave_message)
                
                print(f"❌ {nickname} chatdan chiqdi ({len(clients)} mijoz qoldi)")
                
            except (ValueError, IndexError):
                pass
            
            try:
                client.close()
            except:
                pass
            
            break

def receive():
    """
    Yangi mijozlarni qabul qilish va ularga thread yaratish
    """
    print("=" * 60)
    print("🚀 Real vaqt chat serveri ishga tushdi")
    print("=" * 60)
    print(f"📍 Server manzili: {HOST}:{PORT}")
    print(f"⏳ Mijozlarni kutmoqda...")
    print("=" * 60)
    print("💡 To'xtatish uchun Ctrl+C bosing\n")
    
    while True:
        try:
            # Yangi mijozni qabul qilish
            client, address = server.accept()
            print(f"✅ Yangi ulanish: {address[0]}:{address[1]}")
            
            # Mijozdan nickname so'rash
            client.send("NICK".encode('utf-8'))  # Nickname so'rash signali
            nickname = client.recv(1024).decode('utf-8')
            
            # Nickname tekshirish
            if nickname in nicknames:
                client.send("NICK_EXISTS".encode('utf-8'))
                client.close()
                print(f"⚠️  Nickname '{nickname}' allaqachon mavjud, ulanish rad etildi")
                continue
            
            # Mijozni ro'yxatga qo'shish
            with lock:
                nicknames.append(nickname)
                clients.append(client)
            
            print(f"👤 {nickname} chatga qo'shildi (Jami: {len(clients)} mijoz)")
            
            # Mijozga muvaffaqiyatli ulanish haqida xabar
            welcome_message = f"[{get_timestamp()}] Serverga ulandingiz! Xush kelibsiz, {nickname}!".encode('utf-8')
            client.send(welcome_message)
            
            # Boshqa mijozlarga yangi foydalanuvchi haqida xabar
            join_message = f"[{get_timestamp()}] {nickname} chatga qo'shildi!".encode('utf-8')
            broadcast(join_message, sender_client=client)
            
            # Mijoz uchun thread yaratish
            thread = threading.Thread(target=handle, args=(client,))
            thread.daemon = True
            thread.start()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Server to'xtatilmoqda...")
            break
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            continue

if __name__ == "__main__":
    try:
        receive()
    except KeyboardInterrupt:
        print("\n\n🛑 Server to'xtatildi")
    finally:
        # Barcha ulanishlarni yopish
        print("\n📡 Barcha ulanishlar yopilmoqda...")
        for client in clients:
            try:
                client.close()
            except:
                pass
        server.close()
        print("✅ Server yopildi")

