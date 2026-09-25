# src/modulo03/notifier.py
class EmailService:
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        # En la vida real, aquí habría código de SMTP o API HTTP externa
        print(f"Enviando correo a {recipient}...")
        return True
