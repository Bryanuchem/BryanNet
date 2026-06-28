import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { useLayout } from "../../context/LayoutContext";

export default function SidebarBrand() {

    const {
        sidebarCollapsed,
    } = useLayout();

    return (

        <Box
            sx={{
                height: 88,

                px: sidebarCollapsed ? 0 : 3,

                py: 2.5,

                display: "flex",

                alignItems: "center",

                justifyContent: sidebarCollapsed
                    ? "center"
                    : "flex-start",

                borderBottom:
                    "1px solid rgba(255,255,255,0.08)",

                transition: "all .25s ease",
            }}
        >

            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: sidebarCollapsed ? 0 : 2,
                }}
            >

                {/* BryanNet Logo */}

                <Box
                    sx={{
                        width: 42,
                        height: 42,

                        borderRadius: 2,

                        bgcolor: "#2563EB",

                        color: "#FFFFFF",

                        display: "flex",

                        alignItems: "center",

                        justifyContent: "center",

                        fontSize: "1.25rem",

                        fontWeight: 800,

                        letterSpacing: 0.5,

                        flexShrink: 0,

                        boxShadow:
                            "0 8px 18px rgba(37,99,235,.35)",
                    }}
                >
                    B
                </Box>

                {!sidebarCollapsed && (

                    <Box>

                        <Typography
                            variant="h6"
                            sx={{
                                color: "#FFFFFF",
                                fontWeight: 700,
                                lineHeight: 1.2,
                            }}
                        >
                            BryanNet
                        </Typography>

                        <Typography
                            sx={{
                                mt: 0.25,
                                color:
                                    "rgba(255,255,255,.65)",
                                fontSize: ".72rem",
                                textTransform:
                                    "uppercase",
                                letterSpacing: 1.2,
                            }}
                        >
                            ISP Management
                        </Typography>

                    </Box>

                )}

            </Box>

        </Box>

    );

}