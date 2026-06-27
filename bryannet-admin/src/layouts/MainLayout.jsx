import Box from "@mui/material/Box";

import Sidebar from "../components/layout/Sidebar";
import TopBar from "../components/layout/TopBar";

function MainLayout({ children }) {
    return (
        <Box sx={{ display: "flex", height: "100vh" }}>
            <Sidebar />

            <Box
                sx={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                }}
            >
                <TopBar />

                <Box
                    component="main"
                    sx={{
                        flex: 1,
                        p: 3,
                        bgcolor: "#F8FAFC",
                    }}
                >
                    {children}
                </Box>
            </Box>
        </Box>
    );
}

export default MainLayout;