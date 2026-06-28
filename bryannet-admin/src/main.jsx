import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

import { QueryClientProvider } from "@tanstack/react-query";

import App from "./App";

import theme from "./styles/theme";

import queryClient from "./api/queryClient";

import { AuthProvider } from "./context/AuthContext";
import { LayoutProvider } from "./context/LayoutContext";

import "./index.css";

ReactDOM.createRoot(
    document.getElementById("root")
).render(

    <React.StrictMode>

        <QueryClientProvider client={queryClient}>

            <ThemeProvider theme={theme}>

                <CssBaseline />

                <BrowserRouter>

                    <AuthProvider>

                        <LayoutProvider>

                            <App />

                        </LayoutProvider>

                    </AuthProvider>

                </BrowserRouter>

            </ThemeProvider>

        </QueryClientProvider>

    </React.StrictMode>

);