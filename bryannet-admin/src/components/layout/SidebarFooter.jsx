import {
    Avatar,
    Box,
    Divider,
    Stack,
    Tooltip,
    Typography,
} from "@mui/material";

import { useAuth } from "../../context/AuthContext";
import { useLayout } from "../../context/LayoutContext";

export default function SidebarFooter() {

    const { admin } = useAuth();

    const {
        sidebarCollapsed,
    } = useLayout();

    const initials =
        admin?.username?.charAt(0)?.toUpperCase() ?? "A";

    return (

        <Box>

            <Divider
                sx={{
                    borderColor:
                        "rgba(255,255,255,.08)",
                }}
            />

            <Box
                sx={{
                    p: 2,
                    display: "flex",
                    justifyContent: "center",
                    transition: "all .25s ease",
                }}
            >

                <Tooltip
                    title={
                        <>
                            <Typography
                                fontWeight={600}
                            >
                                {admin?.username ??
                                    "Administrator"}
                            </Typography>

                            <Typography
                                variant="body2"
                            >
                                {admin?.role?.replace(
                                    "_",
                                    " "
                                ) ??
                                    "SUPER ADMIN"}
                            </Typography>
                        </>
                    }
                    placement="right"
                    arrow
                >

                    <Stack
                        direction="row"
                        spacing={
                            sidebarCollapsed
                                ? 0
                                : 2
                        }
                        alignItems="center"
                        sx={{
                            width: "100%",
                            justifyContent:
                                sidebarCollapsed
                                    ? "center"
                                    : "flex-start",
                            cursor: "default",
                        }}
                    >

                        <Avatar
                            sx={{
                                width: 44,
                                height: 44,
                                bgcolor: "#2563EB",
                                fontWeight: 700,
                                fontSize: "1rem",
                                flexShrink: 0,
                            }}
                        >
                            {initials}
                        </Avatar>

                        {!sidebarCollapsed && (

                            <Box
                                sx={{
                                    overflow: "hidden",
                                }}
                            >

                                <Typography
                                    sx={{
                                        color: "#FFFFFF",
                                        fontWeight: 600,
                                        fontSize:
                                            ".95rem",
                                        whiteSpace:
                                            "nowrap",
                                        overflow:
                                            "hidden",
                                        textOverflow:
                                            "ellipsis",
                                    }}
                                >
                                    {admin?.username ??
                                        "Administrator"}
                                </Typography>

                                <Typography
                                    sx={{
                                        color:
                                            "#94A3B8",
                                        fontSize:
                                            ".78rem",
                                        letterSpacing:
                                            .8,
                                        textTransform:
                                            "uppercase",
                                    }}
                                >
                                    {admin?.role?.replace(
                                        "_",
                                        " "
                                    ) ??
                                        "SUPER ADMIN"}
                                </Typography>

                            </Box>

                        )}

                    </Stack>

                </Tooltip>

            </Box>

        </Box>

    );

}