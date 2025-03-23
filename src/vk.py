import ctypes


def press_key(vk_code):
    scan_code = ctypes.windll.user32.MapVirtualKeyA(vk_code, 0)
    ctypes.windll.user32.keybd_event(vk_code, scan_code, 0, 0)


def release_key(vk_code):
    scan_code = ctypes.windll.user32.MapVirtualKeyA(vk_code, 0)
    ctypes.windll.user32.keybd_event(vk_code, scan_code, 0x0002, 0)
