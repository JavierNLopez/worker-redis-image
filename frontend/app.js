const API = "http://44.214.240.84:8000";

const imageInput = document.getElementById("imageInput");
const uploadBox = document.getElementById("uploadBox");
const tasksContainer = document.getElementById("tasks");
const logsContainer = document.getElementById("logs");


// =======================
// DRAG & DROP
// =======================

uploadBox.addEventListener("dragover", (e) => {

    e.preventDefault();

    uploadBox.classList.add("dragging");
});

uploadBox.addEventListener("dragleave", () => {

    uploadBox.classList.remove("dragging");
});


uploadBox.addEventListener("drop", async (e) => {

    e.preventDefault();

    uploadBox.classList.remove("dragging");

    const files = e.dataTransfer.files;

    uploadImage(files);
});


// =======================
// SUBIR IMÁGENES
// =======================

async function uploadImage(customFiles = null) {

    const files = customFiles || imageInput.files;

    if (!files.length) {

        alert("Selecciona imágenes");

        return;
    }

    for (const file of files) {

        if (!file.type.startsWith("image/")) {
            continue;
        }

        const formData = new FormData();

        formData.append("file", file);

        const response = await fetch(`${API}/upload`, {

            method: "POST",

            body: formData
        });

        const data = await response.json();

        createTaskCard(data.task_id);
    }
}


// =======================
// CREAR TARJETA
// =======================

function createTaskCard(taskId) {

    const card = document.createElement("div");

    card.className = "task-card";

    card.id = taskId;

    card.innerHTML = `

        <h3>${taskId}</h3>

        <div class="progress">

            <div class="progress-bar" id="bar-${taskId}"></div>

        </div>

        <p id="status-${taskId}">
            ⏳ En cola...
        </p>

        <div class="images-grid" id="images-${taskId}"></div>
    `;

    tasksContainer.prepend(card);

    monitorTask(taskId);
}


// =======================
// MONITOREAR ESTADO
// =======================

function monitorTask(taskId) {

    const interval = setInterval(async () => {

        try {

            const response = await fetch(`${API}/status/${taskId}`);

            const data = await response.json();

            const statusText = document.getElementById(`status-${taskId}`);

            const progressBar = document.getElementById(`bar-${taskId}`);

            if (data.status === "queued") {

                progressBar.style.width = "20%";

                statusText.innerHTML = "⏳ En cola...";
            }

            if (data.status === "processing") {

                progressBar.style.width = "60%";

                statusText.innerHTML = "⚙️ Procesando...";
            }

            if (data.status === "completed") {

                clearInterval(interval);

                progressBar.style.width = "100%";

                statusText.innerHTML = "✅ Completado";

                document.getElementById(`images-${taskId}`).innerHTML = `

                    <div class="image-card">
                        <h4>Resize</h4>
                        <img src="${API}/processed/${data.resized}">
                    </div>

                    <div class="image-card">
                        <h4>Thumbnail</h4>
                        <img src="${API}/processed/${data.thumbnail}">
                    </div>

                    <div class="image-card">
                        <h4>Grayscale</h4>
                        <img src="${API}/processed/${data.grayscale}">
                    </div>

                    <div class="image-card">
                        <h4>PNG</h4>
                        <img src="${API}/processed/${data.png}">
                    </div>

                    <div class="image-card">
                        <h4>Blur</h4>
                        <img src="${API}/processed/${data.blur}">
                    </div>
                `;
            }

        } catch (err) {

            console.log(err);
        }

    }, 1000);
}


// =======================
// DASHBOARD
// =======================

async function loadDashboard() {

    try {

        const response = await fetch(`${API}/dashboard`);

        const data = await response.json();

        document.getElementById("workers").innerText = data.workers;

        document.getElementById("queued").innerText = data.queued;

        document.getElementById("completed").innerText = data.completed;

        logsContainer.innerHTML = "";

        data.logs.forEach(log => {

            const div = document.createElement("div");

            div.className = "log";

            div.innerText = log;

            logsContainer.prepend(div);
        });

    } catch (err) {

        console.log(err);
    }
}


setInterval(loadDashboard, 1000);

loadDashboard();
