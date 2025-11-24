const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const inputArea = document.getElementById('input-area');

// State
let step = 0;
const answers = {
    niche: '',
    subject: '',
    goal: ''
};

// Get lead_id from URL
const urlParams = new URLSearchParams(window.location.search);
const leadId = urlParams.get('lead_id') || 'unknown';

// Initial greeting
window.addEventListener('load', () => {
    setTimeout(() => {
        addBotMessage('Qual o seu nicho? (ex: Médico infantil)');
    }, 500);
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message
    addUserMessage(message);
    userInput.value = '';

    // Process based on step
    if (step === 0) {
        answers.niche = message;
        step++;
        setTimeout(() => addBotMessage('Qual é o assunto específico?'), 500);
    } else if (step === 1) {
        answers.subject = message;
        step++;
        setTimeout(() => addBotMessage('Qual é o objetivo do vídeo? (engajamento, seguidores, leads, vendas…)'), 500);
    } else if (step === 2) {
        answers.goal = message;
        step++;
        // Hide input
        inputArea.classList.add('hidden');

        // Show loading and call API
        const loadingId = addLoadingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: `Nicho: ${answers.niche}. Assunto: ${answers.subject}. Objetivo: ${answers.goal}`,
                    assunto: answers.subject,
                    objetivo: answers.goal,
                    session_id: null // New session
                })
            });

            const data = await response.json();
            removeLoadingIndicator(loadingId);

            if (data.content && data.content.messages && data.content.messages.length > 0) {
                const botResponse = data.content.messages[0].text;
                addBotMessageWithCopy(botResponse);

                // Start Black Friday sequence after 3 seconds
                setTimeout(startBlackFridaySequence, 3000);
            } else {
                addBotMessage('Desculpe, ocorreu um erro ao gerar sua resposta.');
            }

        } catch (error) {
            removeLoadingIndicator(loadingId);
            addBotMessage('Erro de conexão. Tente novamente mais tarde.');
            console.error(error);
        }
    }
});

function addUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'message user';
    div.textContent = text;
    chatMessages.appendChild(div);
    scrollToBottom();
}

function addBotMessage(text) {
    const div = document.createElement('div');
    div.className = 'message bot';
    div.innerHTML = formatText(text);
    chatMessages.appendChild(div);
    scrollToBottom();
}

function addBotMessageWithCopy(text) {
    const div = document.createElement('div');
    div.className = 'message bot';
    div.innerHTML = formatText(text);

    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        Copiar resposta
    `;

    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                Copiado!
            `;
            setTimeout(() => {
                copyBtn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                    Copiar resposta
                `;
            }, 2000);
        });
    });

    div.appendChild(copyBtn);
    chatMessages.appendChild(div);
    scrollToBottom();
}

function addLoadingIndicator() {
    const div = document.createElement('div');
    div.className = 'typing-indicator';
    div.id = 'loading-' + Date.now();
    div.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
    chatMessages.appendChild(div);
    scrollToBottom();
    return div.id;
}

function removeLoadingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatText(text) {
    // Simple formatting for line breaks and bold
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

function startBlackFridaySequence() {
    const messages = [
        "Vou fazer a maior BLACK FRIDAY de todas...",
        "Com todos meus treinamentos vitalícios + bônus que NUNCA fiz antes...",
        "Mas eu não vou liberar isso aqui, só num grupo secreto do WhatsApp...",
        "se cadastre para a blackfriday agora mesmo"
    ];

    let delay = 0;

    messages.forEach((msg, index) => {
        setTimeout(() => {
            addBotMessage(msg);
            if (index === messages.length - 1) {
                addCTAButton();
            }
        }, delay);
        delay += 1500; // 1.5s between messages
    });
}

function addCTAButton() {
    const div = document.createElement('div');
    div.style.padding = '0 20px 20px 20px';

    const btn = document.createElement('a');
    btn.className = 'cta-btn';
    btn.href = `https://segueadii.com.br/m-bf-25/?utm_source=ia_roteiros&lead_id=${leadId}`;
    btn.textContent = 'CADASTRAR';
    btn.target = '_blank';

    div.appendChild(btn);
    chatMessages.appendChild(div);
    scrollToBottom();
}
