const form = document.getElementById('to-do-form');
const input = document.getElementById('to-do-input');
const todoList = document.getElementById('to-do-list');

let todos = loadFromLocalStorage("todos");
renderTodos();

form.addEventListener('submit', function (event) {
    event.preventDefault();

    try {
        const text = input.value.trim();

        if (!text) {
            throw new Error("Task (Task-Content) cannot be empty");
        }

        const todo = {
            id: Date.now(),
            text,
        };

        todos.push(todo);
        saveToLocalStorage("todos", todos);
        renderTodos();
        input.value = "";
    } catch (error) {
        handleError("formSubmit", error);
        alert("Failed to add task: " + error.message + "Please try again.");
    }
});

function renderTodos() {
    try {
        todoList.innerHTML = "";

        todos.forEach((todo) => {
            if (!todo.text || !todo.id) {
                throw new Error("Invalid To-Do item");
            }

            const li = document.createElement('li');

            //Task Input
            const input = document.createElement('input');
            input.type = 'text';
            input.value = todo.text;
            input.readOnly = true;
            input.style.width = "340px";
            input.style.margin = "10px";

            //Edit Task Button
            const editButton = document.createElement('button');
            editButton.textContent = ' Edit';
            editButton.style.marginLeft = "20px";

            editButton.addEventListener("click", () => {
                try {
                    if (input.readOnly) {
                        //Switching to Edit Mode
                        input.readOnly = false;
                        input.focus();
                        editButton.textContent = "Save";
                        cancelButton.style.display = "inline-block";
                        cancelButton.style.marginLeft = "13px";
                    } else {

                        const updatedText = input.value.trim();
                        if (!updatedText) {
                            throw new Error("Task (Task-Content) cannot be empty");
                        }
                        todo.text = updatedText;
                        saveToLocalStorage("todos", todos);

                        input.readOnly = true;
                        editButton.textContent = "Edit";
                        cancelButton.style.display = "none";

                    }
                } catch (error) {
                    handleError("todoUpdate", error);
                    alert("Failed to update task: " + error.message);
                    input.value = todo.text; // Revert to old value
                }
            });

            //Cancel Task Button
            const cancelButton = document.createElement('button');
            cancelButton.textContent = 'Cancel';
            cancelButton.style.display = 'none';

            cancelButton.addEventListener('click', () => {
                try{
                    input.value = todo.text;
                    editButton.textContent = "Edit";
                    cancelButton.style.display = "none";
                } catch (error) {
                    handleError("todoCancel", error);
                }
            });

            //Delete Task Button
            const deleteButton = document.createElement('button');
            deleteButton.textContent = ' Delete';
            deleteButton.style.marginLeft = "20px";

            deleteButton.addEventListener('click', () => {
                try {
                    todos = todos.filter(t => t.id !== todo.id);
                    saveToLocalStorage("todos", todos);
                    renderTodos();
                } catch (error) {
                    handleError("todoDelete", error);
                    alert("Failed to delete task: " + error.message);
                }
            });

            //Appending Input and Delete Button
            li.append(input, editButton, cancelButton, deleteButton);
            todoList.appendChild(li);
        });
    } catch (error) {
        handleError("renderTodos", error);
        alert("Failed to Add (perform) Tasks: " + error.message + " Please try again.");
    }
}