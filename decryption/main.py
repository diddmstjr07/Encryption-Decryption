import pyAesCrypt
import os
import flet as ft
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def main(page: ft.Page):
    def show_error(message):
        """에러 메시지 다이얼로그"""
        dlg = ft.AlertDialog(
            title=ft.Text("Alert", style=ft.TextStyle(font_family="DepartureMono")),
            content=ft.Text(message, style=ft.TextStyle(font_family="DepartureMono")),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(dlg))],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def show_success(message):
        """성공 메시지 다이얼로그"""
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

    def close_dialog_success(dialog):
        dialog.open = False
        page.update()
        page.window.close()

    def on_encrypt_click(e):
        dic = directory_field.value
        password = password_field.value
        if not dic:
            return show_error("Please type Target Directory")
        if not password:
            return show_error("Please type Password")
        try:
            page.clean()
            page.add(Progress_bar, top_margin, directory_field, password_field, decrypt_button)
            decryption(directory=dic, password=password)
            show_success("Directory Decryption Succeed")
        except Exception as error:
            show_error(f"An error occurred: {str(error)}")

    def open_directory_picker(e):
        """디렉토리 선택기 열기"""
        directory_picker.get_directory_path()

    def on_directory_result(e: ft.FilePickerResultEvent):
        if e.path:
            directory_field.value = e.path
        page.update()

    page.fonts = {
        "DepartureMono": resource_path("assets/fonts/DepartureMono-Regular.otf") 
    }

    page.theme = ft.Theme(font_family="DepartureMono")
    page.window.width = 711
    page.window.height = 255

    top_margin = ft.Container(height=10)

    directory_picker = ft.FilePicker(on_result=on_directory_result)
    page.overlay.append(directory_picker)

    # Directory field with suffix button
    directory_field = ft.TextField(
        label="Target Decryption Directory",
        multiline=False,
        text_style=ft.TextStyle(font_family="DepartureMono"),
        suffix=ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
            tooltip="Select Directory",
            on_click=open_directory_picker
        )
    )

    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        text_style=ft.TextStyle(font_family="DepartureMono")
    )
    
    decrypt_button = ft.ElevatedButton(
        content=ft.Text(
            "Decryption",
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
    
    page.add(top_margin, directory_field, password_field, decrypt_button)

def bytes_to_string(byte_data, encoding='utf-8'):
    return byte_data.decode(encoding)

def rename_file(old_name, new_name):
    if not os.path.isfile(old_name):
        raise FileNotFoundError(f"File '{old_name}' not found.")
    os.rename(old_name, new_name)
    print(f"File renamed from '{old_name}' to '{new_name}'")

def restore_file(filepath):
    with open(filepath, 'rb') as file:
        content = file.readlines()
    if content:
        filename_line = content[0]
        rest_of_content = content[1:]
        with open(filepath, 'wb') as file:
            file.writelines(rest_of_content)
    return filename_line.strip()

def decryption(directory, password):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if str(file)[-4:] != ".aes":
                continue
            en_root_direct = os.path.join(root, file)
            de_root_direct = os.path.join(root, file[:-4])
            pyAesCrypt.decryptFile(en_root_direct, de_root_direct, password)
            filename = restore_file(de_root_direct)
            rename_file(de_root_direct, os.path.join(root, bytes_to_string(filename)))
            os.remove(en_root_direct)

if __name__ == "__main__":
    ft.app(target=main)
