#!/usr/bin/env python3
"""
Virtual BLE Loopback Bridge
Simulates a zero-dependency local socket bridge connecting Mobile KMP clients with IoT Mock Peripherals.
"""
import asyncio
import json
import logging
from typing import Dict, Any, Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VirtualBLEBridge")

class VirtualBLEBridge:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.subscriptions = {}
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info(f"Virtual BLE Bridge listening on {self.host}:{self.port}")
        return self

    async def broadcast_notification(self, characteristic_uuid: str, payload: Dict[str, Any]):
        message = json.dumps({
            "type": "NOTIFICATION",
            "characteristic": characteristic_uuid,
            "data": payload
        })
        logger.debug(f"Broadcasting notification: {message}")
        return len(message)

    async def stop(self):
        self.is_running = False
        logger.info("Virtual BLE Bridge stopped.")

if __name__ == "__main__":
    bridge = VirtualBLEBridge()
    asyncio.run(bridge.start())
