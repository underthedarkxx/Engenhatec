from backend.extensions import db, bcrypt
from backend.models.user import User
from backend import create_app

app = create_app()

def is_valid_bcrypt_hash(pw: str) -> bool:
    """
    Verifica se uma senha é um hash bcrypt válido.
    """
    if not isinstance(pw, str):
        return False
    if len(pw) != 60:
        return False
    return pw.startswith(("$2a$", "$2b$", "$2y$"))

def reset_users(senha_padrao: str = "SenhaSegura123!"):
    print("🔄 Resetando usuários...")

    # Remove todos os usuários existentes
    User.query.delete()
    db.session.commit()

    usuarios = [
        {"username": "usuario_assinante", "email": "assinante@exemplo.com", "is_subscribed": True},
        {"username": "usuario_comum", "email": "comum@exemplo.com", "is_subscribed": False},
    ]

    for u in usuarios:
        user = User(**u)
        user.set_password(senha_padrao)
        db.session.add(user)
        print(f"✅ Usuário criado: {u['username']} (senha: {senha_padrao})")

    db.session.commit()
    print("✔ Usuários resetados com sucesso.")

def verificar_corrigir_senhas(senha_corrigida: str = "SenhaSegura123!"):
    print("\n🔍 Verificando senhas...")

    users = User.query.all()
    atualizados = 0

    for user in users:
        if not is_valid_bcrypt_hash(user.password):
            print(f"[!] Senha inválida para usuário: {user.username}")
            user.password = bcrypt.generate_password_hash(senha_corrigida).decode("utf-8")
            atualizados += 1
            print(f"--> Senha atualizada para {user.username} (nova senha: {senha_corrigida})")

    if atualizados > 0:
        db.session.commit()
        print(f"\n✔ {atualizados} senha(s) corrigida(s).")
    else:
        print("✔ Todas as senhas estão válidas.")

if __name__ == "__main__":
    with app.app_context():
        reset_users()
        verificar_corrigir_senhas()

