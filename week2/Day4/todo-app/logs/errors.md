# Application Error Logs

## saveToStorage
- Cause: Invalid key or LocalStorage quota exceeded
- Handling: Error caught and logged
- Impact: App continues running

## loadFromStorage
- Cause: Corrupted JSON
- Handling: Reset to empty array
- Impact: Data loss prevented from crashing UI

![A screenshot image of error (loading from local storage)](Images/loading_storage.png)

## formSubmit
- Cause: Empty todo input
- Handling: Validation + user alert

![A screenshot image of error, caused because of submiting any empty form(task input)](Images/form_submit.png)

## renderTodos
- Cause: Invalid todo object structure
- Handling: Error logged, rendering skipped

![A screenshot image of rendering error, caused because of invalid structure](Images/render_todo.png)

![A screenshot image of rendering error, caused because of invalid declaration](Images/render2.png)
