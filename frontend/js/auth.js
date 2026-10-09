const signupBtn=document.getElementById('signup-btn')
const loginBtn=document.getElementById('login-btn')
const errorEl=document.getElementById('error')
// ! SIGN UP
async function signUp(){
    const emailEl=document.getElementById('email')
    const email=emailEl.value;

    const passwordEl=document.getElementById('password')
    const password=passwordEl.value;

    try{
        const response= await fetch(API +"/users/",{
            method:"POST",
            headers:{'Content-Type':"application/json"},
            body:JSON.stringify({email:email,password:password})
            })
        if(!response.ok){
            const data= await response.json()
            errorEl.textContent=data.detail
            return;
        }
    }
    catch(error){
        console.log(error)
        errorEl.textContent = "Could not reach the server. Try again."
    };
    
}
// ! LOGIN
async function login(){
    const emailEl=document.getElementById('email')
    const email=emailEl.value;

    const passwordEl=document.getElementById('password')
    const password=passwordEl.value;
    
    try{
        const response= await fetch(API+"/login",{
            method:"POST",
            body: new URLSearchParams({username:email,password:password})// * URLSearchParams for request body requierd by login route
        })
        if(!response.ok){
            const data=await response.json()
            errorEl.textContent=data.detail
            return;
        }
        const data = await response.json()
        localStorage.setItem("token", data.access_token)
        console.log(data)
        window.location.href='dashboard.html'

    }
    catch(error){
        console.log(error)
        errorEl.textContent = "Could not reach the server. Try again."
    }

}
if(signupBtn){
signupBtn.addEventListener('click',function(event){
    event.preventDefault();
    signUp()
})}
if(loginBtn){
loginBtn.addEventListener('click',function(event){
    event.preventDefault();
    login()
})}

