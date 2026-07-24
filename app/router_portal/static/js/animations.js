/*
==========================================================
BryanNet Router Portal
Animations
==========================================================
*/

"use strict";

/*
==========================================================
Animation Module
==========================================================
*/

const Animations = (() => {

    /*
    ==========================================================
    CSS Class Helpers
    ==========================================================
    */

    function addClass(element, className) {

        if (!element) {

            return;

        }

        element.classList.add(className);

    }

    function removeClass(element, className) {

        if (!element) {

            return;

        }

        element.classList.remove(className);

    }

    /*
    ==========================================================
    Fade
    ==========================================================
    */

    function fadeIn(element) {

        if (!element) {

            return;

        }

        removeClass(element, "hidden");

        removeClass(element, "fade-out");

        addClass(element, "fade-in");

    }

    function fadeOut(element) {

        if (!element) {

            return;

        }

        removeClass(element, "fade-in");

        addClass(element, "fade-out");

        window.setTimeout(() => {

            addClass(element, "hidden");

        }, 250);

    }

    /*
    ==========================================================
    Button Pulse
    ==========================================================
    */

    function pulse(element) {

        if (!element) {

            return;

        }

        removeClass(element, "pulse");

        /*
        Restart animation
        */

        void element.offsetWidth;

        addClass(element, "pulse");

    }

    /*
    ==========================================================
    Shake
    ==========================================================
    */

    function shake(element) {

        if (!element) {

            return;

        }

        removeClass(element, "shake");

        void element.offsetWidth;

        addClass(element, "shake");

    }

    /*
    ==========================================================
    Success Animation
    ==========================================================
    */

    function success(element) {

        if (!element) {

            return;

        }

        removeClass(element, "success-pop");

        void element.offsetWidth;

        addClass(element, "success-pop");

    }

    /*
    ==========================================================
    Focus Animation
    ==========================================================
    */

    function attachInputAnimations() {

        const inputs = document.querySelectorAll(

            ".form-group input"

        );

        inputs.forEach((input) => {

            input.addEventListener(

                "focus",

                () => {

                    addClass(

                        input,

                        "input-focus"

                    );

                }

            );

            input.addEventListener(

                "blur",

                () => {

                    removeClass(

                        input,

                        "input-focus"

                    );

                }

            );

        });

    }

    /*
    ==========================================================
    Card Entrance
    ==========================================================
    */

    function animateCard() {

        const card = document.querySelector(

            ".login-card"

        );

        if (!card) {

            return;

        }

        addClass(

            card,

            "fade-in"

        );

    }

    /*
    ==========================================================
    Status Animation
    ==========================================================
    */

    function animateStatus(statusElement) {

        if (!statusElement) {

            return;

        }

        removeClass(

            statusElement,

            "fade-in"

        );

        void statusElement.offsetWidth;

        addClass(

            statusElement,

            "fade-in"

        );

    }

    /*
    ==========================================================
    Auto Initialization
    ==========================================================
    */

    function init() {

        attachInputAnimations();

        animateCard();

    }

    /*
    ==========================================================
    Public API
    ==========================================================
    */

    return {

        init,

        fadeIn,

        fadeOut,

        pulse,

        shake,

        success,

        animateStatus

    };

})();

/*
==========================================================
Initialize After DOM Ready
==========================================================
*/

document.addEventListener(

    "DOMContentLoaded",

    () => {

        Animations.init();

    }

);

/*
==========================================================
Freeze Module
==========================================================
*/

Object.freeze(Animations);