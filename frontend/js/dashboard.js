
async function getAllExpense(){
    const displayEl=document.getElementById('expenses')
    try{
        const response=await apiFetch("/expenses/");
        const data = await response.json()
        displayEl.textContent=''

        data.forEach(expense => {
            const expenseDiv= document.createElement('div')
            expenseDiv.className='expense-card'
            const titleEl=document.createElement('input')
            const descEl=document.createElement('textarea')
            const amountEl=document.createElement('input')
            amountEl.type='number'
            const categoryEl=document.createElement('input')
            const dateEl=document.createElement('input')
            dateEl.type='date'
            const editEl=document.createElement('button')
            editEl.textContent="Edit"
            editEl.className='BTN'

            const deleteEl=document.createElement('button')
            deleteEl.textContent='Delete'
            deleteEl.className='BTN'


            titleEl.value=expense.title
            descEl.value=expense.description
            amountEl.value=expense.amount
            categoryEl.value=expense.category
            dateEl.value = expense.date ? expense.date.split('T')[0] : '';

            titleEl.readOnly=true
            descEl.readOnly=true
            amountEl.readOnly=true
            categoryEl.readOnly=true
            dateEl.readOnly=true

            expenseDiv.appendChild(titleEl)
            expenseDiv.appendChild(descEl)
            expenseDiv.appendChild(amountEl)
            expenseDiv.appendChild(categoryEl)
            expenseDiv.appendChild(dateEl)
            expenseDiv.appendChild(editEl)
            expenseDiv.appendChild(deleteEl)
            displayEl.appendChild(expenseDiv)

            editEl.addEventListener('click',function(){

                if (editEl.textContent==='Edit'){
                    titleEl.readOnly=false
                    descEl.readOnly=false
                    amountEl.readOnly=false
                    categoryEl.readOnly=false
                    dateEl.readOnly=false
                    editEl.textContent="Save"

                }
                else{
                updateExpense(
                    expense.id,
                    titleEl.value,
                    descEl.value,
                    Number(amountEl.value),
                    categoryEl.value,
                    dateEl.value)
                    editEl.textContent="Edit"
                }
            })

            deleteEl.addEventListener('click',function(){
                deleteExpense(expense.id)
            })
        });

        const total=data.reduce((accumulator,currentExpense)=>{
                return accumulator+currentExpense.amount;
        },0);
        
        const totalEL=document.getElementById('total')
        totalEL.textContent="Rs. "+total
        

        console.log(data)
        console.log(total)

        
    }
    catch(error){
        console.log(error)
    }
}

async function createExpense(){
    const titleEl=document.getElementById('title')
    const descEL=document.getElementById('description')
    const amountEl=document.getElementById('amount')
    const categoryEl=document.getElementById('category')
    const dateEl=document.getElementById('date')
    
    const title=titleEl.value;
    const desc=descEL.value;
    const amount=Number(amountEl.value);
    const category=categoryEl.value;
    const date=dateEl.value;

    try{
        const response= await apiFetch("/expenses/",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({
                title:title,
                description:desc,
                amount:amount,
                category:category,
                date:date
            })
        })
        const data= await response.json()
        console.log(data)
        expenseForm.reset()
        modal.classList.add('hidden')
        getAllExpense()
    }
    catch(error){
        console.log(error)
    }
}

async function updateExpense(expense_id,title,desc,amount,category,date){
    
    try{
        const response= await apiFetch("/expenses/"+expense_id,{
            method:"PUT",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({
                title:title,
                description:desc,
                amount:amount,
                category:category,
                date:date
            })
        })
        const data= await response.json()
        console.log(data)
    }
    catch(error){
        console.log(error)
    }
    
}
async function deleteExpense(expense_id){
    try{
        const response= await apiFetch("/expenses/"+expense_id,{
            method:"DELETE"
        })
        getAllExpense();
    }
    catch(error){
        console.log(error)
    }
}



const expenseForm=document.getElementById('add-expense')
expenseForm.addEventListener('submit',function(event){
    event.preventDefault();
    createExpense()
})
const modal= document.getElementById('modal')
const addbtn=document.getElementById('addexp')
addbtn.addEventListener('click',function(){
    modal.classList.toggle('hidden')
    
})

modal.addEventListener('click', function(event){
    if(event.target === modal){
        modal.classList.add('hidden')
    }
})


const logoutBtn=document.getElementById('logout')
logoutBtn.addEventListener('click',function(){
    localStorage.removeItem('token')
    window.location.href='login.html'
})