/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './node_modules/flowbite/**/*.js'
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: {
                    "50": "#fff7ed",
                    "100": "#ffedd5",
                    "200": "#fed7aa",
                    "300": "#fdba74",
                    "400": "#fb923c",
                    "500": "#f97316",
                    "600": "#ea580c",
                    "700": "#c2410c",
                    "800": "#9a3412",
                    "900": "#7c2d12",
                    "950": "#431407"
                }
            }
        },
        fontFamily: {
            'body': [
                'Inter',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Roboto',
                'Helvetica Neue',
                'Arial',
                'Noto Sans',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
                'Noto Color Emoji'
            ],
            'sans': [
                'Inter',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Roboto',
                'Helvetica Neue',
                'Arial',
                'Noto Sans',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
                'Noto Color Emoji'
            ]
        }
    },
    plugins:
        [
            require('flowbite/plugin', 'daisyui'),
            // require('daisyui'),
        ],

    daisyui:
        {
            themes: ["autumn"], // false: only light + dark | true: all themes | array: specific themes like this ["light", "dark", "cupcake"]
            darkTheme:
                "dark", // name of one of the included themes for dark mode
            base:
                true, // applies background color and foreground color for root element by default
            styled:
                true, // include daisyUI colors and design decisions for all components
            utils:
                true, // adds responsive and modifier utility classes
            prefix:
                "", // prefix for daisyUI classnames (components, modifiers and responsive class names. Not colors)
            logs:
                true, // Shows info about daisyUI version and used config in the console when building your CSS
            themeRoot:
                ":root", // The element that receives theme color CSS variables
        }
    ,
}