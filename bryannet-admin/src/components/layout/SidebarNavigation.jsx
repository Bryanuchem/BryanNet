import {
    Box,
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Tooltip,
    Typography,
} from "@mui/material";

import { NavLink } from "react-router-dom";

import navigation from "../../config/navigation";
import { useLayout } from "../../context/LayoutContext";

export default function SidebarNavigation() {

    const { sidebarCollapsed } = useLayout();

    const groups = navigation.reduce((acc, item) => {

        if (!acc[item.section]) {
            acc[item.section] = [];
        }

        acc[item.section].push(item);

        return acc;

    }, {});

    return (

        <Box
            sx={{
                flex: 1,
                overflowY: "auto",
                px: sidebarCollapsed ? 1 : 2,
                py: 2,
            }}
        >

            {Object.entries(groups).map(([section, items]) => (

                <Box
                    key={section}
                    sx={{
                        mb: sidebarCollapsed ? 1 : 3,
                    }}
                >

                    {!sidebarCollapsed && (

                        <Typography
                            sx={{
                                px: 2,
                                mb: 1,
                                fontSize: ".72rem",
                                fontWeight: 700,
                                color: "#94A3B8",
                                letterSpacing: 1,
                                textTransform: "uppercase",
                            }}
                        >
                            {section}
                        </Typography>

                    )}

                    <List disablePadding>

                        {items.map((item) => {

                            const Icon = item.icon;

                            const button = (

                                <ListItemButton
                                    key={item.path}
                                    component={NavLink}
                                    to={item.path}
                                    sx={{

                                        position: "relative",

                                        minHeight: 48,

                                        mb: .5,

                                        px: sidebarCollapsed ? 0 : 2,

                                        justifyContent:
                                            sidebarCollapsed
                                                ? "center"
                                                : "flex-start",

                                        borderRadius: 3,

                                        color: "#CBD5E1",

                                        transition:
                                            "all .2s ease",

                                        "&::before": {

                                            content: '""',

                                            position: "absolute",

                                            left: 0,

                                            top: 8,

                                            bottom: 8,

                                            width: 4,

                                            borderRadius: "0 4px 4px 0",

                                            bgcolor: "#2563EB",

                                            opacity: 0,

                                            transition:
                                                "opacity .2s ease",

                                        },

                                        "& .MuiListItemIcon-root": {

                                            color: "inherit",

                                            minWidth:
                                                sidebarCollapsed
                                                    ? 0
                                                    : 40,

                                            mr:
                                                sidebarCollapsed
                                                    ? 0
                                                    : 1,

                                            justifyContent:
                                                "center",

                                            transition:
                                                "all .2s ease",

                                        },

                                        "&:hover": {

                                            bgcolor:
                                                "rgba(255,255,255,.06)",

                                            color:
                                                "#FFFFFF",

                                            transform:
                                                "translateX(2px)",

                                        },

                                        "&.active": {

                                            bgcolor:
                                                "rgba(37,99,235,.15)",

                                            color:
                                                "#FFFFFF",

                                        },

                                        "&.active::before": {

                                            opacity: 1,

                                        },

                                        "&.active .MuiListItemIcon-root": {

                                            color:
                                                "#60A5FA",

                                        },

                                    }}
                                >

                                    <ListItemIcon>

                                        <Icon />

                                    </ListItemIcon>

                                    {!sidebarCollapsed && (

                                        <ListItemText
                                            primary={item.label}
                                            primaryTypographyProps={{
                                                fontSize:
                                                    ".95rem",
                                                fontWeight:
                                                    500,
                                            }}
                                        />

                                    )}

                                </ListItemButton>

                            );

                            return sidebarCollapsed ? (

                                <Tooltip
                                    key={item.path}
                                    title={item.label}
                                    placement="right"
                                    arrow
                                >
                                    {button}
                                </Tooltip>

                            ) : (

                                <Box key={item.path}>

                                    {button}

                                </Box>

                            );

                        })}

                    </List>

                </Box>

            ))}

        </Box>

    );

}