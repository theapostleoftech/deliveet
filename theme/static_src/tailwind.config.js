/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'

        /**
         * Flowbite settings
         */
        "./node_modules/flowbite/**/*.js",
        "node_modules/preline/dist/*.js"
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    "50": "#fff3e6",
                    "100": "#ffe7cc",
                    "200": "#ffcf99",
                    "300": "#ffb766",
                    "400": "#ff9f33",
                    "500": "#e96800",
                    "600": "#ba5300",
                    "700": "#8c3f00",
                    "800": "#5d2a00",
                    "900": "#2f1500",
                    "950": "#180b00"
                },
                secondary: {
                    "50": "#fbeee9",
                    "100": "#f7ddd3",
                    "200": "#eebba7",
                    "300": "#e5997b",
                    "400": "#dc774f",
                    "500": "#ab4f2c",
                    "600": "#893f23",
                    "700": "#672f1a",
                    "800": "#452011",
                    "900": "#221009",
                    "950": "#110804"
                },
                tertiary: {
                    "50": "#e6e7f1",
                    "100": "#cdd0e3",
                    "200": "#9ba0c7",
                    "300": "#6971ab",
                    "400": "#37418f",
                    "500": "#191462",
                    "600": "#14104e",
                    "700": "#0f0c3b",
                    "800": "#0a0827",
                    "900": "#050414",
                    "950": "#03020a"
                },
            }
        },
        fontFamily: {
            'body': [
                'Poppins',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Helvetica Neue',
                'Arial',
                'Barlow',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
            ],
            'sans': [
                'Poppins',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Helvetica Neue',
                'Arial',
                'Barlow',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
            ]
        },
        plugins: [
            /**
             * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
             * for forms. If you don't like it or have own styling for forms,
             * comment the line below to disable '@tailwindcss/forms'.
             */
            require('flowbite/plugin'),
            require('flowbite-typography'),
            require('preline/plugin'),
        ],
    }
}
