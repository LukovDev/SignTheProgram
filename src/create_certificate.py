#
# create_certificate.py - Создаёт код для генерации сертификатов.
#


# Импортируем:
import os
import json


# Загружаем файл конфигурации:
with open("build/config.json", "r+", encoding="utf-8") as f:
    config = json.load(f)


# Создаём сертификат:
def create_certificate(config: dict) -> None:
    openssl = "build\\tools\\openssl.exe"
    outdir  = "build/out/"
    if not os.path.isdir(outdir): os.mkdir(outdir)

    out_file = os.path.join(outdir, config["common-name"])
    password = f"-password pass:{config['password']}"

    subject = [
        f"C={config['country']}"                  if config["country"]           else "",
        f"ST={config['state-or-region']}"         if config["state-or-region"]   else "",
        f"L={config['locality']}"                 if config["locality"]          else "",
        f"emailAddress={config['email-address']}" if config["email-address"]     else "",
        f"O={config['organization']}"             if config["organization"]      else "",
        f"OU={config['organization-unit']}"       if config["organization-unit"] else "",
        f"CN={config['common-name']}",  # Основное имя обязательно.
    ]

    flags = [
        " ".join([f for f in config["flags"]]),  # Флаги из поля флагов в конфиг файле.
        f"-config {config['openssl-config']}",
        f"-newkey {config['newkey']}",
        f"-keyout {out_file}.key",
        f"-out {out_file}.crt",
        f"-days {config['days']}",
        f"-subj \"/{'/'.join([s for s in subject if s])}\""
        # "-quiet" - Используйте этот флаг для минимального вывода openssl.
    ]

    # Создаём приватный ключ и сертификат:
    print(f"{' START GENERATING ':─^80}\n")
    os.system(f"{openssl} req {' '.join(flags)}")
    os.system(f"{openssl} pkcs12 -export -out {out_file}.pfx -inkey {out_file}.key -in {out_file}.crt {password}")
    print(f"\nDone! Output files in folder: {outdir}")


# Если скрипт запускают:
if __name__ == "__main__":
    create_certificate(config)
