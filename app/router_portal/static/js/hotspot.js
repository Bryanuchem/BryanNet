/*
==========================================================
BryanNet Router Portal
RouterOS Compatibility Helpers
==========================================================
*/

"use strict";

/*
==========================================================
Hotspot Module
==========================================================
*/

const Hotspot = (() => {

    /*
    ==========================================================
    Configuration
    ==========================================================
    */

    const CONFIG = {

        loginUrl: "",

        redirectUrl: "",

        chapId: "",

        chapChallenge: "",

        error: ""

    };

    /*
    ==========================================================
    Initialization
    ==========================================================
    */

    function initialize(config = {}) {

        Object.assign(

            CONFIG,

            config

        );

    }

    /*
    ==========================================================
    CHAP Detection
    ==========================================================
    */

    function isChapEnabled() {

        return (

            CONFIG.chapId !== "" &&

            CONFIG.chapChallenge !== ""

        );

    }

    /*
    ==========================================================
    Form Preparation

    Phase 4:
    Do NOT hash the password yet.

    The backend still authenticates using the
    plaintext password.

    RouterOS login occurs in a later phase.
    ==========================================================
    */

    function prepareForm(form) {

        if (!form) {

            return;

        }

        /*
        Placeholder for future RouterOS integration.

        Future phases will:

            1. Authenticate BryanNet
            2. Receive success
            3. Generate CHAP response
            4. Login to RouterOS
        */

    }

    /*
    ==========================================================
    Future CHAP Helpers
    ==========================================================
    */

    function getChapInformation() {

        return {

            enabled: isChapEnabled(),

            chapId: CONFIG.chapId,

            chapChallenge: CONFIG.chapChallenge

        };

    }

    /*
    ==========================================================
    Error Handling
    ==========================================================
    */

    function parseError(message) {

        if (!message) {

            return "";

        }

        const error =

            message.toLowerCase();

        if (

            error.includes("invalid")

        ) {

            return "Incorrect username or password.";

        }

        if (

            error.includes("expired")

        ) {

            return "Your subscription has expired.";

        }

        if (

            error.includes("limit")

        ) {

            return "Device limit reached.";

        }

        if (

            error.includes("simultaneous")

        ) {

            return "Maximum concurrent sessions reached.";

        }

        if (

            error.includes("disabled")

        ) {

            return "Your account has been disabled.";

        }

        return message;

    }

    /*
    ==========================================================
    Initial Error Display
    ==========================================================
    */

    function showInitialError() {

        if (!CONFIG.error) {

            return;

        }

        const status = document.getElementById(

            "statusMessage"

        );

        if (

            !status ||

            typeof Validation ===

                "undefined"

        ) {

            return;

        }

        Validation.showStatus(

            status,

            parseError(

                CONFIG.error

            ),

            "error"

        );

    }

    /*
    ==========================================================
    Configuration
    ==========================================================
    */

    function getConfiguration() {

        return {

            ...CONFIG

        };

    }

    /*
    ==========================================================
    Public API
    ==========================================================
    */

    return {

        initialize,

        prepareForm,

        isChapEnabled,

        getChapInformation,

        parseError,

        showInitialError,

        getConfiguration

    };

})();

/*
==========================================================
Freeze Module
==========================================================
*/

Object.freeze(

    Hotspot

);