let socket;

const wssProtocol = window.location.protocol = "https://" ? "ws://" : "wss://"
const host = window.location.host

function setupWebSocket(channel) {
    socket = new WebSocket(`${wssProtocol}${host}/ws/${channel}`);

    socket.onmessage = (event) => {
        const messagesContainer = document.getElementById("messages");
        // messagesContainer.innerHTML += `<div>${event.data}</div>`;
        messagesContainer.innerHTML += `
        <li>
            <div class="d-flex flex-row justify-content-end mb-4">
                <div class="p-3 me-3 border message">
                    <p class="small mb-0">
                        <strong>Você:</strong><br><br>
                        ${event.data}
                    </p>
                </div>
            </div>
        </li>
        `
    };

    socket.onclose = (event) => {
        //console.error("WebSocket closed unexpectedly:", event);
        console.log('Switching to channel')
        // Pode ser útil adicionar lógica de reconexão aqui se necessário
    };
}

// function sendMessage() {
//     const messageInput = document.getElementById("message-input");
//     const message = messageInput.value;
//     socket.send(message);
//     messageInput.value = "";
// }

const submit = document.getElementById('message-submit')

// Click no botão
submit.addEventListener('click', (event) => {
    event.preventDefault()
    const input = document.getElementById('message-input')
    socket.send(input.value)
    input.value = ''
})

// Tecla enter
submit.onkeydown = function (e) {
    if (e.keyCode == 13) {
        e.preventDefault()
        const input = document.getElementById('message-input')
        socket.send(input.value)
        input.value = ''
    }
}

function switchChannel(channel) {
    if (socket) {
        socket.close();
    }

    setupWebSocket(channel);

    // Notify the server about the channel switch
    socket.onopen = () => {
        socket.send(`Switching to channel ${channel}`);
    };
}

// Inicializa o WebSocket com o canal inicial
setupWebSocket("chatbot");
