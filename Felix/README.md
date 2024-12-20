

### **I) Collect Data from Sleeppad Mode 0x85 V1**

1. **Connect the Sleeppad to the Laptop** via CH340 (COM6) or UART4-M0 (OPI5B) (/dev/ttyS4).

   - **1.1 Unix Time:**
     - 4-byte Unix timestamp: The device does not have the concept of time zones, meaning it operates in timezone 0. The time value set should be the local time of the device minus the local timezone difference from 0:00:00:00 on January 1, 1970.
     - For example: If the current time is 8:00:00 on January 1, 2022, the set value will be 1641024000, and the hexadecimal representation is 0x61D00A00. In the communication protocol, the low bits come first and the high bits follow, resulting in 0x00, 0x0A, 0xD0, 0x61 (4 bytes).
     - Note: The Unix timestamp directly read by most programming languages contains the local timezone, which needs to be processed. For instance, Beijing time (UTC+8) requires adding 28800 to the local Unix timestamp.
     - You can use the tool [https://tool.ip138.com/timestamp/](https://tool.ip138.com/timestamp/) for comparison testing.

   - **1.2 Communication Format (Between Sleeppad and Server):**
     - General Data Structure:
       ```
       [header 0x7D 1 byte] + [frame type symbol 1 byte] + [frame length 2 byte] + [ID total 10 byte ASCII] + [content:data/response] + [end 0x0D]
       ```
     - The data sent by the hardware is a mixture of ASCII code and hexadecimal. Refer to the detailed description of each instruction.
     - The hardware does not have the function of data packetization, meaning the server cannot make decisions based on the number of data packets.
     - **Frame type** ranges from 0x01 to 0xFF, representing a command or content (see details below).
     - **Frame length (2 bytes)** is the length of the entire frame, including the header and end of the frame. It is represented by an unsigned 2-byte integer, with the low byte first and the high byte second.
     - **ID** is the device identifier (e.g., CNU2000001), formatted as 10 ASCII characters. Since the device ID cannot be known when connecting for the first time, when the server sends command [0x07], the device will not check the ID match, meaning the ID can be any 10-character string.

   - **1.3 Analyzing the Content in the Data Structure:**
     - **Content:**
       ```
       [serial number 1 byte] + [time 4 bytes] + [status 1 byte] + [heart rate 1 byte] + [respiration rate 1 byte] + [SDATA 2 bytes] + [PDATA 2 bytes]
       ```
     - **Serial number (1 byte):** The serial number is an unsigned 1-byte integer. It cycles from 0 to 119. If the server does not receive certain data, it can send [0x01] to request the string of data to be resent. Note: The effective memory is 120, with a 1-second interval, only supporting data readback within 2 minutes.
     - **Time (4 bytes):** The time is an unsigned integer, with the low-order bits first and the high-order bits second, representing the difference in seconds between 0:00:00:00 on January 1, 1970 UTC time and the current local time. Note: The device's clock may have a certain time error and may not exactly match the server's time.
     - **Status (1 byte):** The status per second is a 1-byte unsigned integer:
       - 0x01: Out of bed in this second.
       - 0x02: Movement in this second.
       - 0x03: Sit up in this second.
       - 0x04: Sleep in this second.
       - 0x05: Wake up in this second.
       - 0x06: Heavy object in this second.
       - 0x07: Snoring in this second.
       - 0x08: Weak breathing in this second.
     - **Heart rate (1 byte):** The heart rate is an unsigned 1-byte integer. Its real value = byte value. The value is 0 when out of bed or when it cannot be calculated.
     - **Respiration rate (1 byte):** The respiration rate is an unsigned 1-byte integer. Its real value = byte value / 10. The value is 0 when out of bed or when it cannot be calculated.
     - **SDATA (2 bytes):** SDATA is an unsigned 2-byte integer, with the low-order bits first and the high-order bits second.
     - **PDATA (2 bytes):** PDATA is an unsigned 2-byte integer, with the low-order bits first and the high-order bits second.

---

### **Important Notes:**
- Proper handling of Unix time and time zones is crucial to ensure the accuracy of data synchronization between the device and the server.
- The values in the fields such as `status`, `heart rate`, `respiration rate`, `SDATA`, and `PDATA` need to be carefully processed when decoding from raw data.

---
