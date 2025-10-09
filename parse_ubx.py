import struct
import sys
from typing import Dict, Any, Optional

class UBXParser:
    def __init__(self):
        # UBX message header constants
        self.UBX_SYNC1 = 0xB5
        self.UBX_SYNC2 = 0x62
        
        # Common UBX message types
        self.message_types = {
            (0x01, 0x07): "NAV-PVT",
            (0x01, 0x35): "NAV-SAT",
            (0x01, 0x02): "NAV-POSLLH",
            (0x01, 0x06): "NAV-SOL",
            (0x01, 0x12): "NAV-VELNED",
            (0x05, 0x01): "ACK-ACK",
            (0x05, 0x00): "ACK-NAK",
        }
    
    def calculate_checksum(self, data: bytes) -> tuple:
        """Calculate Fletcher checksum for UBX message"""
        ck_a = 0
        ck_b = 0
        for byte in data:
            ck_a = (ck_a + byte) & 0xFF
            ck_b = (ck_b + ck_a) & 0xFF
        return ck_a, ck_b
    
    def parse_nav_pvt(self, payload: bytes) -> Dict[str, Any]:
        """Parse NAV-PVT message"""
        if len(payload) < 92:
            return {"error": "Payload too short for NAV-PVT"}
        
        data = struct.unpack('<LHBBBBBBLLLLLLLLLLLLLHHHHHHHHBBBBBBBB', payload[:92])
        
        return {
            "iTOW": data[0],
            "year": data[1],
            "month": data[2],
            "day": data[3],
            "hour": data[4],
            "minute": data[5],
            "second": data[6],
            "valid": data[7],
            "tAcc": data[8],
            "nano": data[9],
            "fixType": data[10],
            "flags": data[11],
            "numSV": data[13],
            "lon": data[14] * 1e-7,  # degrees
            "lat": data[15] * 1e-7,  # degrees
            "height": data[16] / 1000.0,  # meters
            "hMSL": data[17] / 1000.0,  # meters
            "hAcc": data[18] / 1000.0,  # meters
            "vAcc": data[19] / 1000.0,  # meters
            "velN": data[20] / 1000.0,  # m/s
            "velE": data[21] / 1000.0,  # m/s
            "velD": data[22] / 1000.0,  # m/s
            "gSpeed": data[23] / 1000.0,  # m/s
            "headMot": data[24] * 1e-5,  # degrees
            "sAcc": data[25] / 1000.0,  # m/s
            "headAcc": data[26] * 1e-5,  # degrees
            "pDOP": data[27] * 0.01
        }
    
    def parse_message(self, message: bytes) -> Optional[Dict[str, Any]]:
        """Parse a complete UBX message"""
        if len(message) < 8:
            return None
        
        # Check sync bytes
        if message[0] != self.UBX_SYNC1 or message[1] != self.UBX_SYNC2:
            return None
        
        msg_class = message[2]
        msg_id = message[3]
        length = struct.unpack('<H', message[4:6])[0]
        
        if len(message) < 8 + length:
            return None
        
        payload = message[6:6+length]
        checksum = message[6+length:8+length]
        
        # Verify checksum
        calc_ck_a, calc_ck_b = self.calculate_checksum(message[2:6+length])
        if len(checksum) != 2 or checksum[0] != calc_ck_a or checksum[1] != calc_ck_b:
            return {"error": "Checksum mismatch"}
        
        msg_type = self.message_types.get((msg_class, msg_id), f"Unknown-{msg_class:02X}-{msg_id:02X}")
        
        result = {
            "message_type": msg_type,
            "class": msg_class,
            "id": msg_id,
            "length": length
        }
        
        # Parse specific message types
        if (msg_class, msg_id) == (0x01, 0x07):  # NAV-PVT
            result.update(self.parse_nav_pvt(payload))
        else:
            result["payload"] = payload.hex()
        
        return result
    
    def find_ubx_messages(self, data: bytes):
        """Find and parse UBX messages in a byte stream"""
        messages = []
        i = 0
        
        while i < len(data) - 1:
            if data[i] == self.UBX_SYNC1 and data[i+1] == self.UBX_SYNC2:
                if i + 6 <= len(data):
                    length = struct.unpack('<H', data[i+4:i+6])[0]
                    msg_end = i + 8 + length
                    
                    if msg_end <= len(data):
                        message = data[i:msg_end]
                        parsed = self.parse_message(message)
                        if parsed:
                            messages.append(parsed)
                        i = msg_end
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        
        return messages

def parse_ubx_file(filename: str):
    """Parse UBX messages from a file"""
    parser = UBXParser()
    
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        
        messages = parser.find_ubx_messages(data)
        
        for msg in messages:
            print(f"Message: {msg['message_type']}")
            if msg['message_type'] == 'NAV-PVT' and 'lat' in msg:
                print(f"  Time: {msg.get('year', 0)}-{msg.get('month', 0):02d}-{msg.get('day', 0):02d} "
                      f"{msg.get('hour', 0):02d}:{msg.get('minute', 0):02d}:{msg.get('second', 0):02d}")
                print(f"  Position: {msg['lat']:.7f}°, {msg['lon']:.7f}°")
                print(f"  Height: {msg['height']:.3f}m")
                print(f"  Fix Type: {msg['fixType']}")
                print(f"  Satellites: {msg['numSV']}")
            print(f"  Length: {msg['length']} bytes")
            print()
            
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_ubx.py <ubx_file>")
        sys.exit(1)
    
    parse_ubx_file(sys.argv[1])