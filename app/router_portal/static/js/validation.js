/*
==========================================================
BryanNet Router Portal
Form Validation Helpers
==========================================================
*/

"use strict";

/*
==========================================================
Validation Module
==========================================================
*/

const Validation = (() => {

    /*
    ==========================================================
    Configuration
    ==========================================================
    */

    const USERNAME_MIN_LENGTH = 3;

    const PASSWORD_MIN_LENGTH = 4;

    /*
    ==========================================================
    Helpers
    ==========================================================
    */

    function trim(value) {

        return value.trim();

    }

    function isEmpty(value) {

        return trim(value) === "";

    }

    /*
    ==========================================================
    Username
    ==========================================================
    */

    function validateUsername(username) {

        const value = trim(username);

        if (isEmpty(value)) {

            return {
                valid: false,
                message: "Username is required."
            };

        }

        if (value.length < USERNAME_MIN_LENGTH) {

            return {
                valid: false,
                message: `Username must be at least ${USERNAME_MIN_LENGTH} characters.`
            };

        }

        return {
            valid: true,
            message: ""
        };

    }

    /*
    ==========================================================
    Password
    ==========================================================
    */

    function validatePassword(password) {

        const value = trim(password);

        if (isEmpty(value)) {

            return {
                valid: false,
                message: "Password is required."
            };

        }

        if (value.length < PASSWORD_MIN_LENGTH) {

            return {
                valid: false,
                message: `Password must be at least ${PASSWORD_MIN_LENGTH} characters.`
            };

        }

        return {
            valid: true,
            message: ""
        };

    }

    /*
    ==========================================================
    Entire Form
    ==========================================================
    */

    function validateForm(username, password) {

        const usernameResult = validateUsername(username);

        if (!usernameResult.valid) {

            return usernameResult;

        }

        const passwordResult = validatePassword(password);

        if (!passwordResult.valid) {

            return passwordResult;

        }

        return {

            valid: true,

            message: ""

        };

    }

    /*
    ==========================================================
    UI Helpers
    ==========================================================
    */

    function clearInputState(input) {

        if (!input) {

            return;

        }

        input.classList.remove(

            "error",

            "success"

        );

    }

    function setInputValid(input) {

        clearInputState(input);

        input.classList.add("success");

    }

    function setInputInvalid(input) {

        clearInputState(input);

        input.classList.add("error");

    }

    function clearFormState(form) {

        if (!form) {

            return;

        }

        form
            .querySelectorAll("input")
            .forEach(clearInputState);

    }

    /*
    ==========================================================
    Status Message
    ==========================================================
    */

    function showStatus(

        element,

        message,

        type = "info"

    ) {

        if (!element) {

            return;

        }

        element.className = `status-message ${type}`;

        element.textContent = message;

        element.classList.remove("hidden");

    }

    function hideStatus(element) {

        if (!element) {

            return;

        }

        element.textContent = "";

        element.className = "status-message hidden";

    }

    /*
    ==========================================================
    Loading State
    ==========================================================
    */

    function setLoading(

        button,

        loading,

        loadingText = "Connecting..."

    ) {

        if (!button) {

            return;

        }

        if (loading) {

            button.dataset.originalText = button.textContent;

            button.disabled = true;

            button.classList.add("loading");

            button.textContent = loadingText;

            return;

        }

        button.disabled = false;

        button.classList.remove("loading");

        button.textContent =

            button.dataset.originalText ||

            "Connect to Internet";

    }

    /*
    ==========================================================
    Public API
    ==========================================================
    */

    return {

        validateUsername,

        validatePassword,

        validateForm,

        setInputValid,

        setInputInvalid,

        clearInputState,

        clearFormState,

        showStatus,

        hideStatus,

        setLoading

    };

})();

/*
==========================================================
Freeze Module
==========================================================
*/

Object.freeze(Validation);