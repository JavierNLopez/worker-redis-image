const API_URL =
"http://44.214.240.84:8000"

const dropZone =
document.getElementById("dropZone")

const fileInput =
document.getElementById("fileInput")

const tasksContainer =
document.getElementById("tasks")


// ======================
// DRAG & DROP
// ======================

dropZone.addEventListener(
    "dragover",
    (e)=>{

        e.preventDefault()

        dropZone.classList.add(
            "dragover"
        )
    }
)

dropZone.addEventListener(
    "dragleave",
    ()=>{

        dropZone.classList.remove(
            "dragover"
        )
    }
)

dropZone.addEventListener(
    "drop",
    (e)=>{

        e.preventDefault()

        dropZone.classList.remove(
            "dragover"
        )

        fileInput.files =
        e.dataTransfer.files
    }
)


// ======================
// UPLOAD IMAGE
// ======================

async function uploadImage(){

    const file =
    fileInput.files[0]

    if(!file){

        alert(
            "Selecciona una imagen"
        )

        return
    }

    const formData =
    new FormData()

    formData.append(
        "file",
        file
    )

    try{

        const response =
        await fetch(
            `${API_URL}/upload`,
            {
                method:"POST",
                body:formData
            }
        )

        const data =
        await response.json()

        createTaskCard(
            data.task_id
        )

        listenTask(
            data.task_id
        )

        saveTask(
            data.task_id
        )

    }catch(error){

        console.error(error)

        alert(
            "Error conectando backend"
        )
    }
}


// ======================
// TASK CARD
// ======================

function createTaskCard(taskId){

    const card =
    document.createElement("div")

    card.className =
    "task"

    card.id = taskId

    card.innerHTML = `
        <h3>
            📦 Tarea ${taskId}
        </h3>

        <div class="
            status loading
        ">
            Estado: pending
        </div>
    `

    tasksContainer.prepend(card)
}


// ======================
// SSE
// ======================

function listenTask(taskId){

    const eventSource =
    new EventSource(
        `${API_URL}/events/${taskId}`
    )

    eventSource.onmessage =
    (event)=>{

        const data =
        JSON.parse(event.data)

        const card =
        document.getElementById(taskId)

        const statusDiv =
        card.querySelector(".status")

        statusDiv.innerHTML =
        `Estado: ${data.status}`

        // PROCESSING

        if(
            data.status ===
            "processing"
        ){

            statusDiv.className =
            "status loading"
        }

        // COMPLETED

        if(
            data.status ===
            "completed"
        ){

            statusDiv.className =
            "status completed"

            card.innerHTML += `
                <img
                src="
                ${API_URL}
                ${data.image_url}
                ">

                <br>

                <a
                href="
                ${API_URL}
                ${data.image_url}
                "
                target="_blank"
                >

                    <button>
                        Descargar
                    </button>

                </a>
            `

            eventSource.close()
        }

        // ERROR

        if(
            data.status ===
            "error"
        ){

            statusDiv.className =
            "status error"

            card.innerHTML += `
                <p>
                    Error:
                    ${data.message}
                </p>
            `

            eventSource.close()
        }
    }
}


// ======================
// DASHBOARD
// ======================

async function loadDashboard(){

    try{

        const response =
        await fetch(
            `${API_URL}/dashboard`
        )

        const data =
        await response.json()

        document.getElementById(
            "workersCount"
        ).innerText =
        data.workers.length

        document.getElementById(
            "pendingJobs"
        ).innerText =
        data.pending_jobs

        document.getElementById(
            "completedJobs"
        ).innerText =
        data.completed_jobs

    }catch(error){

        console.error(error)
    }
}

setInterval(
    loadDashboard,
    2000
)

loadDashboard()


// ======================
// LOCAL STORAGE
// ======================

function saveTask(taskId){

    const tasks =
    JSON.parse(
        localStorage.getItem(
            "tasks"
        ) || "[]"
    )

    tasks.push(taskId)

    localStorage.setItem(
        "tasks",
        JSON.stringify(tasks)
    )
}
