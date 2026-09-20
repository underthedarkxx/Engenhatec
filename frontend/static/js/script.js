// --- Controle do chat e mensagens ---
const chatHeader = document.getElementById('chat-header');
const chatBody = document.getElementById('chat-body');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const messages = document.getElementById('messages');

let chatOpen = false;
let isSubscribed = false;  // Controle assinatura

if (chatHeader) {
    chatHeader.addEventListener('click', () => {
        chatOpen = !chatOpen;
        chatBody?.classList.toggle('active');
        if (chatOpen) {
            chatInput?.focus();
            if (messages) messages.scrollTop = messages.scrollHeight;
        }
    });
}

function addMessage(text, sender) {
    if (!messages) return;
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = text;
    messages.appendChild(messageElement);
    messages.scrollTop = messages.scrollHeight;
}

// --- Chat form submit com autenticação e assinatura ---
if (chatForm) {
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        const token = localStorage.getItem('access_token');
        if (!token) {
            addMessage("Você precisa estar logado para usar o chat.", 'bot');
            return;
        }

        if (!isSubscribed) {
            addMessage("⚠️ Somente assinantes podem enviar mensagens no chat.", 'bot');
            return;
        }

        addMessage(message, 'user');
        chatInput.value = '';

        try {
            const response = await fetch('/api/chat/perguntar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
                body: JSON.stringify({ pergunta: message }), // <-- chave 'pergunta' agora
            });


            const data = await response.json();

            if (response.ok) {
                addMessage(data.reply, 'bot');
            } else if (response.status === 403) {
                addMessage(data.error || "Chat disponível apenas para assinantes.", 'bot');
            } else if (response.status === 401) {
                addMessage("Sua sessão expirou. Faça login novamente.", 'bot');
                localStorage.removeItem('access_token');
                window.location.reload();
            } else {
                addMessage("Erro ao processar a mensagem.", 'bot');
            }
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            addMessage("Erro de conexão com o servidor.", 'bot');
        }
    });
}

// --- Inicialização da autenticação e UI ---
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');

    if (token) {
        try {
            const response = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            });

            if (response.ok) {
                const user = await response.json();
                isSubscribed = !!user.is_subscribed;
                
                console.log("Usuário logado:", user);

                // Exibe o username na interface
                const userGreeting = document.getElementById('user-greeting');
                if (userGreeting) {
                    userGreeting.textContent = `Olá, ${user.username}!`;
                    userGreeting.style.display = 'block';
                }

                // Exibe alerta e carrega FAQ só se assinante
            if (!isSubscribed) {
                addMessage("⚠️ Este chat está disponível apenas para assinantes.", 'bot');
            } else {
                addMessage(`✅ Bem-vindo ao chat, ${user.username}!`, 'bot');

                try {
                    const faqResponse = await fetch('/api/materials/faq', {
                        method: 'GET',
                        headers: {
                            'Authorization': 'Bearer ' + token
                        }
                    });

                    if (faqResponse.ok) {
                        const faqData = await faqResponse.json();
                        faqData.forEach(faq => {
                            addMessage(`❓ ${faq.pergunta}\n💡 ${faq.resposta}`, 'bot');
                        });
                    } else {
                        console.warn("Não foi possível carregar o FAQ de materiais.");
                    }
                } catch (faqError) {
                    console.error("Erro ao carregar FAQ:", faqError);
                }
            }

                // Controla visibilidade dos botões
                document.getElementById('login-section')?.style.setProperty('display', 'none');
                document.getElementById('register-section')?.style.setProperty('display', 'none');
                document.getElementById('logout-button')?.style.setProperty('display', 'block');
            } else {
                localStorage.removeItem('access_token');
                window.location.reload();
            }
        } catch (error) {
            console.error('Erro ao buscar dados do usuário:', error);
        }
    } else {
        document.getElementById('login-section')?.style.setProperty('display', 'block');
        document.getElementById('register-section')?.style.setProperty('display', 'block');
        document.getElementById('logout-button')?.style.setProperty('display', 'none');
    }

    // Ajusta input do chat conforme assinatura
    if (chatInput) {
        chatInput.disabled = !isSubscribed;
        chatInput.placeholder = isSubscribed
            ? "Digite sua mensagem..."
            : "Somente assinantes podem enviar mensagens.";
    }

    // Logout
    document.getElementById('logout-button')?.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.reload();
    });

    // --- Formulário de Login ---
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = loginForm.querySelector('#username').value.trim();
            const password = loginForm.querySelector('#password').value;

            if (!username || !password) {
                alert('Por favor, preencha todos os campos.');
                return;
            }

            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem('access_token', data.access_token);
                    alert(data.message || 'Login realizado com sucesso!');
                    window.location.href = '/';  // Redireciona para home
                } else {
                    alert(data.error || 'Erro no login');
                }
            } catch (error) {
                console.error('Erro no login:', error);
                alert('Erro de conexão com o servidor');
            }
        });
    }

    // --- Formulário de Registro ---
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = registerForm.querySelector('input[name="username"]').value.trim();
            const email = registerForm.querySelector('input[name="email"]').value.trim();
            const password = registerForm.querySelector('input[name="password"]').value;

            if (!username || !email || !password) {
                alert('Por favor, preencha todos os campos.');
                return;
            }

            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username, email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    alert(data.message || 'Cadastro realizado com sucesso! Agora faça login.');
                    window.location.href = '/login';  // Redireciona para rota login
                } else {
                    alert(data.error || 'Erro no registro');
                }
            } catch (error) {
                console.error('Erro no registro:', error);
                alert('Erro de conexão com o servidor');
            }
        });
    }

    // --- Carregar materiais ---
    loadMaterials();

    // Toggle detalhes dos materiais
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('toggle-details-btn')) {
            const content = e.target.closest('.material-card').querySelector('.collapsible-content');
            if (content) {
                content.classList.toggle('show');
                e.target.textContent = content.classList.contains('show') ? 'Ocultar Detalhes' : 'Ver Detalhes';
            }
        }
    });
});

// --- Funções materiais ---
async function loadMaterials() {
    try {
        const response = await fetch('/api/materials');
        if (response.ok) {
            const materials = await response.json();
            renderMaterials(materials);
        } else {
            console.error('Erro ao carregar materiais');
        }
    } catch (error) {
        console.error('Erro de conexão:', error);
    }
}

function renderMaterials(materials) {
    const materialsContainer = document.getElementById('materials-container');
    if (!materialsContainer) return;

    materialsContainer.innerHTML = materials.map(material => `
        <div class="material-card">
            <div class="material-header">
                <img src="${material.imageUrl || 'placeholder.jpg'}" alt="${material.name}">
                <h3>${material.name}</h3>
                <p class="caption">${material.caption || ''}</p>
                <button class="toggle-details-btn">Ver Detalhes</button>
            </div>
            <div class="collapsible-content">
                <p class="description">${material.description || ''}</p>
                <div class="specs-container">
                    <div class="pros">
                        <h4>Vantagens</h4>
                        <ul>${(material.pros || []).map(pro => `<li>${pro}</li>`).join('')}</ul>
                    </div>
                    <div class="cons">
                        <h4>Desvantagens</h4>
                        <ul>${(material.cons || []).map(con => `<li>${con}</li>`).join('')}</ul>
                    </div>
                </div>
                <div class="brands-section">
                    <h4>Marcas Recomendadas</h4>
                    <table class="brands-table">
                        <thead>
                            <tr>
                                <th>Posição</th>
                                <th>Marca</th>
                                <th>Avaliação</th>
                                <th>Preço</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${(material.brands || []).map(brand => `
                                <tr>
                                    <td>${brand.position}</td>
                                    <td>${brand.name}</td>
                                    <td>${brand.rating || '-'}</td>
                                    <td>${brand.priceObservation || '-'}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `).join('');
}

