// * DOM references
const displayEl = document.getElementById('expenses')
const totalEl = document.getElementById('total')
const errorEl = document.getElementById('error')
const expenseForm = document.getElementById('add-expense')
const modal = document.getElementById('modal')
const addBtn = document.getElementById('addexp')
const logoutBtn = document.getElementById('logout')
const deleteModal=document.getElementById('delete-modal')
let expenseToDelete=null

// * Shows an error message on the page (FastAPI validation errors are arrays, so fall back to a generic message)
function showError(detail) {
  errorEl.textContent =
    typeof detail === 'string'
      ? detail
      : 'Something went wrong. Check your input.'
}

async function getAllExpense() {
  errorEl.textContent = ''
  try {
    const params = buildFilterParams()

    const response = await apiFetch('/expenses/?' + params.toString())
    const data = await response.json()
    if (!response.ok) {
      showError(data.detail)
      return
    }
    displayEl.textContent = ''

    data.forEach((expense) => {
      const card = createExpenseCard(expense)
      displayEl.appendChild(card)
    })

    const total = data.reduce((accumulator, currentExpense) => {
      return accumulator + Number(currentExpense.amount)
    }, 0)

    totalEl.textContent = 'Rs. ' + total

    console.log(data)
    console.log(total)
  } catch (error) {
    console.log(error)
    showError('Could not reach the server. Try again.')
  }
}

async function createExpense() {
  errorEl.textContent = ''
  const titleEl = document.getElementById('title')
  const descEl = document.getElementById('description')
  const amountEl = document.getElementById('amount')
  const categoryEl = document.getElementById('category')
  const dateEl = document.getElementById('date')

  const title = titleEl.value
  const description = descEl.value
  const amount = Number(amountEl.value)
  const category = categoryEl.value
  const date = dateEl.value

  try {
    const response = await apiFetch('/expenses/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: title,
        description: description,
        amount: amount,
        category: category,
        date: date,
      }),
    })
    const data = await response.json()
    if (!response.ok) {
      showError(data.detail)
      return
    }
    console.log(data)
    expenseForm.reset()
    modal.classList.add('hidden')
    getAllExpense()
  } catch (error) {
    console.log(error)
    showError('Could not reach the server. Try again.')
  }
}

async function updateExpense(
  expenseId,
  title,
  description,
  amount,
  category,
  date,
) {
  errorEl.textContent = ''
  try {
    const response = await apiFetch('/expenses/' + expenseId, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: title,
        description: description,
        amount: amount,
        category: category,
        date: date,
      }),
    })
    const data = await response.json()
    if (!response.ok) {
      showError(data.detail)
      return
    }
    console.log(data)
  } catch (error) {
    console.log(error)
    showError('Could not reach the server. Try again.')
  }
}

async function deleteExpense(expenseId) {
  errorEl.textContent = ''
  try {
    const response = await apiFetch('/expenses/' + expenseId, {
      method: 'DELETE',
    })
    if (!response.ok) {
      const data = await response.json()
      showError(data.detail)
      return
    }
    getAllExpense()
  } catch (error) {
    console.log(error)
    showError('Could not reach the server. Try again.')
  }
}

function buildFilterParams() {
  // * filter
  const titleFilter = document.getElementById('filter-search').value
  const categoryFilter = document.getElementById('filter-category').value
  const minAmountFilter = document.getElementById('filter-min').value
  const maxAmountFilter = document.getElementById('filter-max').value
  const dateFromFilter = document.getElementById('filter-from').value
  const dateToFilter = document.getElementById('filter-to').value
  const orderFilter = document.getElementById('filter-order').value
  const sortFilter = document.getElementById('filter-sort').value

  const params = new URLSearchParams()
  if (titleFilter) {
    params.append('search', titleFilter)
  }
  if (categoryFilter) {
    params.append('category', categoryFilter)
  }
  if (minAmountFilter) {
    params.append('min_amount', minAmountFilter)
  }
  if (maxAmountFilter) {
    params.append('max_amount', maxAmountFilter)
  }
  if (dateFromFilter) {
    params.append('date_from', dateFromFilter)
  }
  if (dateToFilter) {
    params.append('date_to', dateToFilter)
  }
  if (sortFilter) {
    params.append('sort_by', sortFilter)
  }
  if (orderFilter) {
    params.append('order', orderFilter)
  }

  return params
}

function createExpenseCard(expense) {
  const expenseDiv = document.createElement('div')
  expenseDiv.className = 'expense-card'

  const titleEl = document.createElement('input')
  const descEl = document.createElement('textarea')
  const amountEl = document.createElement('input')
  amountEl.type = 'number'
  const categoryEl = document.createElement('input')
  const dateEl = document.createElement('input')
  dateEl.type = 'date'
  const fields = [titleEl, descEl, amountEl, categoryEl, dateEl]

  const editEl = document.createElement('button')
  editEl.textContent = 'Edit'
  editEl.className = 'BTN'

  const deleteEl = document.createElement('button')
  deleteEl.textContent = 'Delete'
  deleteEl.className = 'BTN'

  titleEl.value = expense.title
  descEl.value = expense.description
  amountEl.value = expense.amount
  categoryEl.value = expense.category
  dateEl.value = expense.date ? expense.date.split('T')[0] : ''

  fields.forEach((field) => (field.readOnly = true))

  expenseDiv.append(...fields, editEl, deleteEl)

  // inside createExpenseCard, replace the editEl listener
editEl.addEventListener('click', async function () {
  if (editEl.textContent === 'Edit') {
    fields.forEach((field) => (field.readOnly = false))
    editEl.textContent = 'Save'
  } else {
    const ok = await updateExpense(
      expense.id,
      titleEl.value,
      descEl.value,
      Number(amountEl.value),
      categoryEl.value,
      dateEl.value,
    )
    if (ok) {
      fields.forEach((field) => (field.readOnly = true))
      editEl.textContent = 'Edit'
      getAllExpense() // 
    }
  }
})

  deleteEl.addEventListener('click', function () {
    expenseToDelete = expense.id
    deleteModal.classList.remove('hidden')
  })

  return expenseDiv
}

// * Event listeners
expenseForm.addEventListener('submit', function (event) {
  event.preventDefault()
  createExpense()
})

addBtn.addEventListener('click', function () {
  modal.classList.toggle('hidden')
})

modal.addEventListener('click', function (event) {
  if (event.target === modal) {
    modal.classList.add('hidden')
  }
})
document.getElementById('cancel-btn').addEventListener('click', function () {
  modal.classList.add('hidden')
})

logoutBtn.addEventListener('click', function () {
  localStorage.removeItem('token')
  window.location.href = 'login.html'
})


document.getElementById('apply-filters').addEventListener('click', getAllExpense)
document.getElementById('clear-filters').addEventListener('click',function(){
document.getElementById('filter-search').value = ''
document.getElementById('filter-category').value = ''
document.getElementById('filter-min').value = ''
document.getElementById('filter-max').value = ''
document.getElementById('filter-from').value = ''
document.getElementById('filter-to').value = ''
document.getElementById('filter-sort').value = 'date'
document.getElementById('filter-order').value = 'desc'
getAllExpense()
})

document.getElementById('confirm-delete').addEventListener('click',function(){
  deleteExpense(expenseToDelete)
  deleteModal.classList.add('hidden')
})

document.getElementById('cancel-delete').addEventListener('click',function(){
  deleteModal.classList.add('hidden')
})

getAllExpense()

