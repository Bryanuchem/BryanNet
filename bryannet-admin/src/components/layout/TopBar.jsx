import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import {
    Avatar,
    Box,
    Divider,
    IconButton,
    Menu,
    MenuItem,
    Stack,
    Typography,
} from "@mui/material";

import {
    styled,
} from "@mui/material/styles";

import MenuRoundedIcon from "@mui/icons-material/MenuRounded";
import NotificationsNoneRoundedIcon from "@mui/icons-material/NotificationsNoneRounded";
import KeyboardArrowDownRoundedIcon from "@mui/icons-material/KeyboardArrowDownRounded";
import LogoutRoundedIcon from "@mui/icons-material/LogoutRounded";
import PersonRoundedIcon from "@mui/icons-material/PersonRounded";

import { TOPBAR_HEIGHT } from "../../config/layout";
import { useAuth } from "../../context/AuthContext";
import { useLayout } from "../../context/LayoutContext";

const pageTitles = {
    "/dashboard": "Dashboard",
    "/customers": "Customers",
    "/plans": "Plans",
    "/subscriptions": "Subscriptions",
    "/devices": "Devices",
    "/payments": "Payments",
    "/administration": "Administration",
    "/settings": "Settings",
};

const HamburgerButton = styled("span")(

    ({ open }) => ({

        position: "relative",

        width: 22,

        height: 16,

        display: "block",

        "& span": {

            position: "absolute",

            left: 0,

            width: "100%",

            height: 2.5,

            borderRadius: 999,

            backgroundColor: "#475569",

            transition:
                "transform 260ms cubic-bezier(.4,0,.2,1), opacity 180ms ease, top 260ms cubic-bezier(.4,0,.2,1)",

        },

        "& span:nth-of-type(1)": {

            top: open ? 7 : 0,

            transform: open
                ? "rotate(45deg)"
                : "rotate(0deg)",

        },

        "& span:nth-of-type(2)": {

            top: 7,

            opacity: open ? 0 : 1,

            transform: open
                ? "scaleX(0)"
                : "scaleX(1)",

        },

        "& span:nth-of-type(3)": {

            top: open ? 7 : 14,

            transform: open
                ? "rotate(-45deg)"
                : "rotate(0deg)",

        },

    }),

);

export default function TopBar() {

    const location = useLocation();

    const navigate = useNavigate();

    const {

        admin,

        logout,

    } = useAuth();

    const {

        sidebarCollapsed,

        toggleSidebar,

    } = useLayout();

    const [

        anchorEl,

        setAnchorEl,

    ] = useState(null);

    const open = Boolean(

        anchorEl,

    );

    const pageTitle =
        pageTitles[location.pathname] ??
        "BryanNet";

    const initials =
        admin?.username
            ?.charAt(0)
            ?.toUpperCase() ??
        "A";

    function handleMenuOpen(

        event,

    ) {

        setAnchorEl(

            event.currentTarget,

        );

    }

    function handleMenuClose() {

        setAnchorEl(

            null,

        );

    }

    function handleLogout() {

        handleMenuClose();

        logout();

        navigate(

            "/login",

            {

                replace: true,

            },

        );

    }

    return (

        <Box

            sx={{

                height:
                    TOPBAR_HEIGHT,

                bgcolor:
                    "#FFFFFF",

                borderBottom:
                    "1px solid #E2E8F0",

                px: 4,

                display: "flex",

                alignItems:
                    "center",

                justifyContent:
                    "space-between",

            }}

        >

            {/* ======================================================
                Left
            ====================================================== */}

            <Stack

                direction="row"

                spacing={2}

                alignItems="center"

                sx={{
                    height: "100%"
                }}

            >

                <IconButton

                    onClick={

                        toggleSidebar

                    }

                        sx={{

                            width: 48,

                            height: 48,

                            alignSelf: "center",

                            borderRadius: "50%",

                            transition:
                                "background-color .2s ease, transform .18s ease",

                            "&:hover": {

                                bgcolor: "action.hover",

                                transform: "scale(1.06)",

                            },

                            "&:active": {

                                transform: "scale(0.92)",

                            },

                        }}

                >

                    <HamburgerButton

                        open={!sidebarCollapsed}

                    >

                        <span />

                        <span />

                        <span />

                    </HamburgerButton>

                </IconButton>

                <Box>

                    <Typography

                        variant="h5"

                        sx={{

                            fontWeight: 700,

                            color:
                                "#0F172A",

                            lineHeight: 1.2,

                        }}

                    >

                        {pageTitle}

                    </Typography>

                    <Typography

                        sx={{

                            mt: 0.5,

                            fontSize: "0.85rem",

                            color: "#64748B",

                            whiteSpace: "nowrap",

                            overflow: "hidden",

                            textOverflow: "ellipsis",

                        }}

                    >

                        BryanNet ISP Management Platform

                    </Typography>

                </Box>

            </Stack>

            {/* ======================================================
                Right
            ====================================================== */}

            <Stack

                direction="row"

                spacing={2}

                alignItems="center"

            >

                <IconButton

                    sx={{

                        width: 48,

                        height: 48,

                        borderRadius:
                            "50%",

                        transition:
                            "background-color .2s ease, transform .18s ease",

                        "&:hover": {

                            bgcolor:
                                "action.hover",

                            transform:
                                "scale(1.06)",

                        },

                        "&:active": {

                            transform:
                                "scale(0.92)",

                        },

                    }}

                >

                    <NotificationsNoneRoundedIcon />

                </IconButton>

                <Divider

                    orientation="vertical"

                    flexItem

                />

                <Stack

                    direction="row"

                    spacing={1.5}

                    alignItems="center"

                    onClick={

                        handleMenuOpen

                    }

                    sx={{

                        cursor:
                            "pointer",

                        px: 1,

                        py: 0.5,

                        borderRadius: 2,

                        transition:
                            "background-color .2s ease",

                        "&:hover": {

                            bgcolor:
                                "action.hover",

                        },

                    }}

                >

                    <Avatar

                        sx={{

                            width: 40,

                            height: 40,

                            bgcolor:
                                "#2563EB",

                            fontWeight: 700,

                        }}

                    >

                        {initials}

                    </Avatar>

                    <Box>

                        <Typography

                            sx={{

                                fontWeight: 600,

                                color:
                                    "#0F172A",

                                lineHeight: 1.2,

                            }}

                        >

                            {admin?.username ??
                                "Administrator"}

                        </Typography>

                        <Typography

                            sx={{

                                fontSize:
                                    "0.8rem",

                                color:
                                    "#64748B",

                            }}

                        >

                            {admin?.role?.replace(
                                "_",
                                " ",
                            ) ??
                                "SUPER ADMIN"}

                        </Typography>

                    </Box>

                    <KeyboardArrowDownRoundedIcon

                        sx={{

                            color:
                                "#64748B",

                            transition:
                                "transform .2s ease",

                            transform:

                                open

                                    ? "rotate(180deg)"

                                    : "rotate(0deg)",

                        }}

                    />

                </Stack>

            </Stack>

            <Menu

                anchorEl={

                    anchorEl

                }

                open={

                    open

                }

                onClose={

                    handleMenuClose

                }

                PaperProps={{

                    elevation: 4,

                    sx: {

                        mt: 1,

                        minWidth: 220,

                        borderRadius: 3,

                    },

                }}

            >

                <MenuItem

                    disabled

                >

                    <PersonRoundedIcon

                        sx={{

                            mr: 1.5,

                        }}

                    />

                    My Profile

                </MenuItem>

                <Divider />

                <MenuItem

                    onClick={

                        handleLogout

                    }

                >

                    <LogoutRoundedIcon

                        sx={{

                            mr: 1.5,

                        }}

                    />

                    Logout

                </MenuItem>

            </Menu>

        </Box>

    );

}