import pyAesCrypt
import os
import string
import random
import flet as ft
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_file_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension

def main(page: ft.Page):
    def show_alert(message):
        """경고 메시지 다이얼로그"""
        dlg = ft.AlertDialog(
            title=ft.Text("Alert", style=ft.TextStyle(font_family="DepartureMono")),
            content=ft.Text(message, style=ft.TextStyle(font_family="DepartureMono")),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(dlg))],
        )
        page.overlay.append(dlg)
        dlg.open = True
    
    def show_error(message):
        """경고 메시지 다이얼로그"""
        dlg = ft.AlertDialog(
            title=ft.Text("Error", style=ft.TextStyle(font_family="DepartureMono")),
            content=ft.Text(message, style=ft.TextStyle(font_family="DepartureMono")),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog_error(dlg))],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def show_success(message):
        """경고 메시지 다이얼로그"""
        dlg = ft.AlertDialog(
            title=ft.Text("Success", style=ft.TextStyle(font_family="DepartureMono")),
            content=ft.Text(message, style=ft.TextStyle(font_family="DepartureMono")),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog_success(dlg))],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def close_dialog_error(dialog):
        dialog.open = False
        page.update()
    
    def close_dialog_success(dialog):
        dialog.open = False
        page.update()
        page.window.close()

    def on_encrypt_click(e):
        dic = selected_directory.value
        password = password_field.value
        re_password = re_password_field.value
        if not dic:
            return show_alert("Please select Target Directory")
        if not password:
            return show_alert("Please type Password")
        if not re_password:
            return show_alert("Please type Re-Password")
        if password != re_password:
            return show_alert("Password doesn't match")
        try:
            return_data = encryption_check(dic)
            if return_data == True:
                page.clean()
                page.add(Progress_bar, top_margin, selected_directory_field, password_field, re_password_field, encrypt_button)
                encryption(directory=dic, password=password)
                show_success("Directory Encryption Succeed")
            else:
                pass
        except Exception as error:
            show_alert(f"An error occurred: {str(error)}")

    def encryption_check(directory):
        cnt = 0
        for root, dirs, files in os.walk(directory):
            for file in files:
                exten = get_file_extension(file)
                if exten == ".aes":
                    cnt += 1
        if cnt != 0:
            show_error("Please check is directory had encrypted")
            return False
        return True

    def open_directory_picker(e):
        """디렉토리 선택기 열기"""
        directory_picker.get_directory_path()

    def on_directory_result(e: ft.FilePickerResultEvent):
        if e.path:
            selected_directory.value = e.path
        page.update()

    page.fonts = {
        "DepartureMono": resource_path("assets/fonts/DepartureMono-Regular.otf") 
    }

    page.theme = ft.Theme(font_family="DepartureMono")
    page.window.width = 711
    page.window.height = 320

    top_margin = ft.Container(
        height=10
    )

    # Directory picker 설정
    selected_directory = ft.TextField(
        label="Selected Directory", 
        read_only=True, 
        text_style=ft.TextStyle(font_family="DepartureMono"),
        suffix=ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
            tooltip="Select Directory",
            on_click=open_directory_picker
        )
    )

    directory_picker = ft.FilePicker(on_result=on_directory_result)
    page.overlay.append(directory_picker)

    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        text_style=ft.TextStyle(font_family="DepartureMono")
    )
    re_password_field = ft.TextField(
        label="Re-Password",
        password=True,
        can_reveal_password=True,
        text_style=ft.TextStyle(font_family="DepartureMono")
    )
    
    encrypt_button = ft.ElevatedButton(
        content=ft.Text(
            "Encryption",
            style=ft.TextStyle(
                font_family="DepartureMono"
            )
        ),
        style=ft.ButtonStyle(
            padding=ft.Padding(300, 0, 300, 0)
        ),
        on_click=on_encrypt_click
    )

    Progress_bar = ft.ProgressBar(
        width=700,
        bgcolor="#eeeeee"
    )
    
    selected_directory_field = selected_directory

    page.add(top_margin, selected_directory_field, password_field, re_password_field, encrypt_button)

def string_to_bytes(string, encoding='utf-8'):
    return string.encode(encoding)

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def prepend_filename_to_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as file:
        content = file.readlines()
    with open(filepath, 'wb') as file:
        file.write(string_to_bytes(filename + '\n'))
        file.writelines(content)

def encryption(directory, password):
    for root, dirs, files in os.walk(directory):
        for file in files:
            root_direct = os.path.join(root, file)
            prepend_filename_to_file(filepath=root_direct)
            en_root_direct = os.path.join(root, generate_random_string())
            pyAesCrypt.encryptFile(root_direct, en_root_direct + ".aes", password)
            os.remove(root_direct)

if __name__ == "__main__":
    ft.app(target=main)
