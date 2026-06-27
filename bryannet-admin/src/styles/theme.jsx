import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        primary: {
            main: "#2563EB",
        },
        secondary: {
            main: "#1E293B",
        },
        background: {
            default: "#F8FAFC",
            paper: "#FFFFFF",
        },
    },
    typography: {
        fontFamily: "Arial, Helvetica, sans-serif",
    },
});

export default theme;