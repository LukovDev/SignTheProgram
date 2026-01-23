#
# sign_program.py - Создаёт код для подписывания программы сертификатом.
#


# Импортируем:
import os
import json


# Загружаем файл конфигурации:
with open("build/config.json", "r+", encoding="utf-8") as f:
    config = json.load(f)


# Подписываем программу:
def sign_program(config: dict) -> None:
    signtool = "build\\tools\\signtool.exe"
    outdir  = "build/out/"
    if not os.path.isdir(outdir): os.mkdir(outdir)

    out_file = os.path.join(outdir, config["common-name"])
    password = f"/p {config['password']}" if config["password"] else ""

    flags = [
        "/t http://timestamp.digicert.com",
        f"/f {out_file}.pfx",
        f"/fd {config['fd']}",
        f"\"{config['target-program']}\""
    ]

    # Подписываем программу:
    os.system(f"{signtool} sign {password if password else ''} {' '.join(flags)}")


# Если скрипт запускают:
if __name__ == "__main__":
    sign_program(config)
