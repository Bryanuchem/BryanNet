import {
    Collapse,
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText,
} from "@mui/material";

import ExpandLessRoundedIcon from "@mui/icons-material/ExpandLessRounded";
import ExpandMoreRoundedIcon from "@mui/icons-material/ExpandMoreRounded";

import { NavLink } from "react-router-dom";

export default function SidebarExpandableItem({
    icon: Icon,
    label,
    open,
    onToggle,
    childrenItems,
    sidebarCollapsed,
}) {
    return (
        <>
            <ListItemButton
                onClick={onToggle}
                sx={{
                    position: "relative",
                    minHeight: 48,
                    mb: 0.5,
                    px: sidebarCollapsed ? 0 : 2,
                    justifyContent: sidebarCollapsed
                        ? "center"
                        : "flex-start",
                    borderRadius: 3,
                    color: "#CBD5E1",
                    transition: "all .2s ease",

                    "& .MuiListItemIcon-root": {
                        color: "inherit",
                        minWidth: sidebarCollapsed ? 0 : 40,
                        mr: sidebarCollapsed ? 0 : 1,
                        justifyContent: "center",
                    },

                    "&:hover": {
                        bgcolor: "rgba(255,255,255,.06)",
                        color: "#FFFFFF",
                    },
                }}
            >
                <ListItemIcon>
                    <Icon />
                </ListItemIcon>

                {!sidebarCollapsed && (
                    <>
                        <ListItemText
                            primary={label}
                            primaryTypographyProps={{
                                fontSize: ".95rem",
                                fontWeight: 500,
                            }}
                        />

                        {open ? (
                            <ExpandLessRoundedIcon fontSize="small" />
                        ) : (
                            <ExpandMoreRoundedIcon fontSize="small" />
                        )}
                    </>
                )}
            </ListItemButton>

            {!sidebarCollapsed && (
                <Collapse
                    in={open}
                    timeout="auto"
                    unmountOnExit
                >
                    <List disablePadding>
                        {childrenItems.map((child) => (
                            <ListItemButton
                                key={child.path}
                                component={NavLink}
                                to={child.path}
                                end={child.path === "/administration"}
                                sx={{
                                    pl: 6,
                                    minHeight: 42,
                                    borderRadius: 2,
                                    color: "#94A3B8",

                                    "&.active": {
                                        bgcolor:
                                            "rgba(37,99,235,.15)",
                                        color: "#FFFFFF",
                                    },

                                    "&:hover": {
                                        bgcolor:
                                            "rgba(255,255,255,.06)",
                                        color: "#FFFFFF",
                                    },
                                }}
                            >
                                <ListItemText
                                    primary={child.label}
                                    primaryTypographyProps={{
                                        fontSize: ".9rem",
                                    }}
                                />
                            </ListItemButton>
                        ))}
                    </List>
                </Collapse>
            )}
        </>
    );
}