import winreg
import os
import time
from collections import deque
from typing import Any
 
 
# root
HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
 
# key path
PREMIUM_PATH = r'Software\PremiumSoft'
CLSID_PATH = r'Software\Classes\CLSID'
 
 
def get_sub_keys(root: Any, reg_path: str) -> list:
    """This function will retrieve a list of sub-keys under the path
    of `root` + `reg_path`.
 
    Args:
        root(Any): Root registry.
        reg_path(str): The relative specific path under the root registry.
 
    Returns:
        The list of sub-keys.
    """
    key_result = winreg.OpenKeyEx(root, reg_path)
    i: int = 0
    sub_keys_list: list = list()
 
    while True:
        try:
            sub_keys = winreg.EnumKey(key_result, i)
            sub_keys_list.append(sub_keys)
            i += 1
        except Exception as e:
            break
    
    return sub_keys_list
 
 
def get_all_keys(root: Any, key_path: str) -> list:
    """Get the list of absolute path of all entries under the
    specified path through the deque.
 
    Args:
        root(Any): Root registry.
        key_path(str): The relative specific path under the root registry.
 
    Returns:
        A list of all entries under the keys.
    """
    all_keys_list: list = list()
 
    qeque = deque()
    qeque.append(key_path)
 
    while len(qeque) != 0:
        sub_key_path = qeque.popleft()
 
        for item in get_sub_keys(root, sub_key_path):
            item_path = os.path.join(sub_key_path, item)
 
            if len(get_sub_keys(root, item_path)) != 0:
                qeque.append(item_path)
                all_keys_list.append(item_path)
            else:
                all_keys_list.append(item_path)
    
    return all_keys_list
 
 
def main():
    """The entry function to be executed.
 
    Returns:
        None
    """
    clsid_all_keys_list = get_all_keys(HKEY_CURRENT_USER, CLSID_PATH)
    premium_all_keys_list = get_all_keys(HKEY_CURRENT_USER, PREMIUM_PATH)
    premium_sub_keys_list = [os.path.join(PREMIUM_PATH, item) for item in get_sub_keys(HKEY_CURRENT_USER, PREMIUM_PATH)]
    print(f"premium_sub_keys_list: {premium_sub_keys_list}")
 
    for clsid_item in clsid_all_keys_list:
        if "Info" in clsid_item:
            clsid_item_prefix = os.path.dirname(clsid_item)
            print(f"# Info item: {clsid_item}")
            winreg.DeleteKeyEx(HKEY_CURRENT_USER, clsid_item)
            winreg.DeleteKeyEx(HKEY_CURRENT_USER, clsid_item_prefix)
    
    # The outermost folder is not deleted.
    for premium_item in reversed(premium_all_keys_list):
        if "Servers" in premium_item:
            print(f"Tips: Servers => {premium_item} will not be deleted.")
            pass
        elif premium_item in premium_sub_keys_list:
            print(f"Tips: Servers => {premium_item} will not be deleted.")
            pass
        else:
            winreg.DeleteKeyEx(HKEY_CURRENT_USER, premium_item)
 
 
if __name__ == "__main__":
    print("Start to delete registry...")
    main()
    print("Task done.", "Windows will closed after 5 seconds...", sep="\n")
 
    for i in range(5):
        time.sleep(1)
        print("*" * (i + 1))
