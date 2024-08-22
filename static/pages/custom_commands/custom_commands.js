let onClickCommand = (technical_name) => {
    let progressBar = document.getElementById("progress_bar");
    let progressBarText = document.getElementById("progress_bar_text");

    /* Start temporarily event stream */
    const progressBarSSE = new EventSource(`http://localhost:8000/custom_commands/run/${technical_name}`);

    progressBarSSE.onopen  = () => {
        progressBarText.innerText = "Command started!"
    };
    progressBarSSE.addEventListener("custom_command", (event) => {
       let data = JSON.parse(event.data);
       progressBar.value = data.progress;
       progressBar.max = data.max;
       progressBarText.innerText = data.status;
       if(progressBar.value === progressBar.max){
           progressBarText.innerText = "Command complete";
           progressBarSSE.close()
           location.href = '/custom_commands';
       }
       console.log(event.data);
    });
};

document.addEventListener("DOMContentLoaded", () => {

});