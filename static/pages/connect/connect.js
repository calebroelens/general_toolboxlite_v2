let connectRPC = async () => {
    let url = document.getElementById("url");
    let port = document.getElementById("port");
    let user = document.getElementById("user");
    let database = document.getElementById("database_choice");
    let password = document.getElementById("password");
    if(url.value && user.value && database.value && password.value){
        await Request.post(
            '/connect/login',
            JSON.stringify({
                url: url.value,
                port: port.value || false,
                user: user.value,
                database: database.value,
                password: password.value
            }),
            handleLoginSuccess,
            handleLoginFailure,
        );
    } else {
        document.getElementById("success_box").classList.add('is-hidden');
        document.getElementById("error_box").classList.remove('is-hidden');
        document.getElementById("error_header").innerText = "Missing fields"
        document.getElementById("error_text").innerHTML = "Missing fields:<ul>";
        if(!url.value){
            document.getElementById("error_text").innerHTML += "<li>URL</li>";
        }
        if(!user.value){
            document.getElementById("error_text").innerHTML += "<li>User</li>";
        }
        if(!database.value){
            document.getElementById("error_text").innerHTML += "<li>Database</li>";
        }
        if(!password.value){
            document.getElementById("error_text").innerHTML += "<li>Password</li>";
        }
        document.getElementById("error_text").innerHTML += "</ul>";
    }
};

let handleLoginSuccess = (response) => {
    document.getElementById("error_box").classList.add('is-hidden');
    document.getElementById("success_header").innerText = "Login success";
    document.getElementById("success_box").classList.remove('is-hidden');
    document.getElementById("success_text").innerHTML = `<strong>Loading applications.</strong><progress class="progress is-success m-2" max="100"></progress>`;
    setTimeout(() => {
            window.location = '/apps';
        }, 2000);
}

let handleLoginFailure = (jqXHR, textStatus, errorThrown) => {
    document.getElementById("success_box").classList.add('is-hidden');
    document.getElementById("error_box").classList.remove('is-hidden');
    document.getElementById("error_text").innerText = jqXHR.responseJSON.error || "Unknown error occurred";
    document.getElementById("error_header").innerText = errorThrown;
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("connect_rpc").addEventListener("click", connectRPC);
});