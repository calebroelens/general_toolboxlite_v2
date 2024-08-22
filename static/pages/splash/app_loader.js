document.addEventListener("DOMContentLoaded", () => {
    let progressBar = document.getElementById("loading_bar");
    let progressBarText = document.getElementById("loading_text");

    const progressBarSSE = new EventSource("http://localhost:8000/application_state/init");

    progressBarSSE.onopen  = () => {
        progressBarText.innerText = "SSE started..."
    };

    progressBarSSE.addEventListener("application_state_init", (event) => {
       let data = JSON.parse(event.data);
       progressBar.value = data.progress;
       console.log(data);
       if(progressBar.value === 100){
           progressBarText.innerText = "Application loaded!";
           progressBarSSE.close()
           location.href = '/apps';
       }
    });

})