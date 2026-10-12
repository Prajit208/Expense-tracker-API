const API="https://expense-tracker-backend-bice-five.vercel.app"


// * Helper function 
async function apiFetch(path, options={}){ // ! options defaulted as empty obejct fot GET routes
    const token=localStorage.getItem('token');

    const response= await fetch(API+path,{
        method:options.method,
        headers:{...options.headers, "Authorization":"Bearer "+token},
        body:options.body
    })  
    if(response.status===401){
        localStorage.removeItem('token') // ! return to login if token expires
        window.location.href='login.html'
    }
    return response;
}
