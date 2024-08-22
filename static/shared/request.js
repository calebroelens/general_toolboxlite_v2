/* Local ORM management */

class Request {
    static async post(url, data, success_function, error_function, contentType="application/json; charset=utf-8"){
        return await this.#_request(url, data, "POST", success_function, error_function, contentType);
    }
    static async delete(url, data, success_function, error_function, contentType="application/json; charset=utf-8"){
        return await this.#_request(url, data, "DELETE", success_function, error_function, contentType);
    }
    static async update(url, data, success_function, error_function, contentType="application/json; charset=utf-8"){
        return await this.#_request(url, data, "PUT", success_function, error_function, contentType);
    }
    static async get(url, success_function, error_function){
        return await this.#_request(url, {}, "GET", success_function, error_function,);
    }
    static async #_request(url, data, method, success_function, error_function, contentType="application/json; charset=utf-8"){
        try {
            return await $.ajax({
                url: url,
                type: method,
                data: data,
                contentType: contentType,
                error: error_function,
                success: success_function
            });
        } catch (error) {
            // Discard error
        }
        
    }
}
