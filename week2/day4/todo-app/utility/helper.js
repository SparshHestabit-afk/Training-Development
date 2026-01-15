//safely saving data to local storage
function saveToLocalStorage(key, data) {
    try {
        if (!key) {
            throw new Error("LocalStorage key is required");
        }

        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        handleError('saveToLocalStorage', error);
    }
}


//safely loading data from local storage
function loadFromLocalStorage(key) {
    try {
        if (!key) {
            throw new Error("LocalStorage key is required");
        }

        const data = localStorage.getItem(key);
        
        return data ? JSON.parse(data) : [];
    } catch (error) {
        handleError('loadFromLocalStorage', error);
        return [];
    }
}

// centralizing the error handling

function handleError(source, error) {
    const errorDetails = {
        source,
        message: error.message,
        timeStamp: new Date().toISOString()
    };

    console.error("Application Error in :" , errorDetails);
}