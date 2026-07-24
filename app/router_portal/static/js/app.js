/*
==========================================================
BryanNet Router Portal
Application Bootstrap
==========================================================
*/

"use strict";

/*
==========================================================
Application
==========================================================
*/

const App = (() => {

    /*
    ==========================================================
    DOM Elements
    ==========================================================
    */

    let form;

    let usernameInput;

    let passwordInput;

    let loginButton;

    let statusMessage;

    /*
    ==========================================================
    Cache Elements
    ==========================================================
    */

    function cacheDom() {

        form = document.getElementById(
            "router-login-form"
        );

        usernameInput = document.getElementById(
            "username"
        );

        passwordInput = document.getElementById(
            "password"
        );

        statusMessage = document.getElementById(
            "statusMessage"
        );

        loginButton = form?.querySelector(
            'button[type="submit"]'
        );

    }

    /*
    ==========================================================
    Live Validation
    ==========================================================
    */

    function registerInputValidation() {

        usernameInput.addEventListener(

            "input",

            () => {

                Validation.clearInputState(
                    usernameInput
                );

                Validation.hideStatus(
                    statusMessage
                );

            }

        );

        passwordInput.addEventListener(

            "input",

            () => {

                Validation.clearInputState(
                    passwordInput
                );

                Validation.hideStatus(
                    statusMessage
                );

            }

        );

    }

    /*
    ==========================================================
    Submit
    ==========================================================
    */

    function handleSubmit(event) {

        Validation.hideStatus(
            statusMessage
        );

        Validation.clearFormState(
            form
        );

        const username =
            usernameInput.value;

        const password =
            passwordInput.value;

        const validation =
            Validation.validateForm(

                username,

                password

            );

        if (!validation.valid) {

            event.preventDefault();

            if (

                validation.message
                    .toLowerCase()
                    .includes(
                        "username"
                    )

            ) {

                Validation.setInputInvalid(
                    usernameInput
                );

            }

            else {

                Validation.setInputInvalid(
                    passwordInput
                );

            }

            Validation.showStatus(

                statusMessage,

                validation.message,

                "error"

            );

            Animations.shake(
                form
            );

            return;

        }

        Validation.setInputValid(
            usernameInput
        );

        Validation.setInputValid(
            passwordInput
        );

        Validation.setLoading(

            loginButton,

            true

        );

        Animations.pulse(
            loginButton
        );

        /*
        =======================================================
        CHAP Preparation

        hotspot.js will hash the password when RouterOS
        provides CHAP parameters.

        No RouterOS login occurs here.

        We simply allow the browser to continue submitting
        to /portal/login.
        =======================================================
        */

        if (

            typeof Hotspot !==
            "undefined"

        ) {

            Hotspot.prepareForm(
                form
            );

        }

        /*
        Browser continues normal POST.
        Do not preventDefault().
        */

    }

    /*
    ==========================================================
    Register Events
    ==========================================================
    */

    function registerEvents() {

        form.addEventListener(

            "submit",

            handleSubmit

        );

        registerInputValidation();

    }

    /*
    ==========================================================
    Startup
    ==========================================================
    */

    function initialize() {

        cacheDom();

        if (

            !form ||

            !usernameInput ||

            !passwordInput ||

            !loginButton ||

            !statusMessage

        ) {

            console.error(

                "BryanNet Portal initialization failed."

            );

            return;

        }

        registerEvents();

        if (

            typeof Hotspot !==
            "undefined"

        ) {

            Hotspot.initialize();

            Hotspot.showInitialError();

        }

    }

    /*
    ==========================================================
    Public API
    ==========================================================
    */

    return {

        initialize

    };

})();

/*
==========================================================
DOM Ready
==========================================================
*/

document.addEventListener(

    "DOMContentLoaded",

    () => {

        App.initialize();

    }

);

/*
==========================================================
Freeze Module
==========================================================
*/

Object.freeze(
    App
);