// client.js

function execute_client() {
    // Client side connection
    document.addEventListener('DOMContentLoaded', () => {
        // Connect the client who opened this web page to the Server
        const socket = io.connect("http://127.0.0.1:5001");
        let currClientId = "";

        socket.on("connect", (data) => {
        if (data) {
            currClientId = data.clientId;
            console.log(`Connected to server with Id: ${data.clientId}`);
        }
        });

        socket.on("response", (data) => {
        console.log(data);
        });

        socket.on("client_list_update", (data) => {
        const clientList = document.getElementById("client-list");
        clientList.innerHTML = "";
        data.clients.forEach((clientId, i) => {
            const listItem = document.createElement("li");
            listItem.textContent = "Client " + i + ": " + clientId;
            clientList.appendChild(listItem);
        });
        console.log("Updated connected client list shown on web page.");
        });

        socket.emit("receive-message", {
        msg: "Hello, server.",
        });
        console.log("Sent a message to the server.");

        modify_form(socket);

        socket.on("redirect_to_room1", (data) => {
            window.location.href = data; 
        });
    });
}

function modify_form(socket) {
    const room1Button = document.getElementById('button-to-room1');

    room1Button.addEventListener('click', (e) => {
        e.preventDefault();
        socket.emit("to-room1");
    });
}