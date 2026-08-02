import axios from "axios";


// Backend API URL
const API_BASE_URL = "http://localhost:8000/api";


// Create Axios instance
const apiClient = axios.create({

    baseURL: API_BASE_URL,

    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
    },

    timeout: 30000

});



// Request interceptor
apiClient.interceptors.request.use(

    (config) => {


        const token = localStorage.getItem(
            "auth_token"
        );


        if (token) {

            config.headers.Authorization =
                `Bearer ${token}`;

        }


        return config;

    },


    (error) => {

        return Promise.reject(error);

    }

);



// Response interceptor
apiClient.interceptors.response.use(

    (response) => {

        return response;

    },


    (error) => {


        if (error.response) {


            if (error.response.status === 401) {


                localStorage.removeItem(
                    "auth_token"
                );


                localStorage.removeItem(
                    "user"
                );


                window.location.href = "/login";

            }


            console.error(
                "API Error:",
                error.response.data
            );


        }


        else if (error.request) {


            console.error(
                "Server not reachable"
            );


        }


        else {


            console.error(
                "Request Error:",
                error.message
            );

        }


        return Promise.reject(error);

    }

);



export default apiClient;