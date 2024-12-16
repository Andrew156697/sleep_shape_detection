import subprocess

def list_usb_cameras():
    try:
        # Chạy lệnh lsusb
        result = subprocess.run(['lsusb'], capture_output=True, text=True, check=True)
        
        # In ra danh sách các thiết bị USB
        print("Danh sách camera tại các cổng USB:")
        for line in result.stdout.splitlines():
            if "Camera" in line or "webcam" in line.lower():  # Tìm kiếm từ khóa "Camera" hoặc "webcam"
                print(line)
    except subprocess.CalledProcessError as e:
        print("Lỗi khi chạy lệnh:", e)
    except FileNotFoundError:
        print("Lệnh 'lsusb' không được tìm thấy. Vui lòng cài đặt usbutils.")
    except Exception as e:
        print("Đã xảy ra lỗi:", e)

if __name__ == "__main__":
    list_usb_cameras()