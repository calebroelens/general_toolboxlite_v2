let searchDb = async () => {
    let url = document.getElementById("url");
    let port = document.getElementById("port");
    if(url.value){
        /* Create request to backend */
        await Request.post(
            '/connect/find_databases',
            JSON.stringify({url: url.value, port: port.value || false}),
            handleSearchDbSuccess,
            handleSearchDbFailure,
        );
    }
};

let handleSearchDbSuccess = (response) => {
    console.log(response);
    let database_list = $('#database_list');
    database_list.html('');
    document.getElementById("success_text").innerHTML = `The following databases have been found:<ul>`;
    for(let db of response['databases']){
        let new_option = document.createElement('option');
        new_option.value = db;
        database_list.append(new_option);
        document.getElementById("success_text").innerHTML += `<li>${db}</li>`;
    }
    document.getElementById("error_box").classList.add('is-hidden');
    document.getElementById("success_header").innerText = "Found databases";
    document.getElementById("success_box").classList.remove('is-hidden');
    document.getElementById("success_text").innerHTML += `</ul>`;
}

let handleSearchDbFailure = (jqXHR, textStatus, errorThrown) => {
    document.getElementById("success_box").classList.add('is-hidden');
    document.getElementById("error_box").classList.remove('is-hidden');
    document.getElementById("error_text").innerText = jqXHR.responseJSON.error || "Unknown error occurred";
    document.getElementById("error_header").innerText = errorThrown;
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("search_databases").addEventListener("click", () => searchDb());
});