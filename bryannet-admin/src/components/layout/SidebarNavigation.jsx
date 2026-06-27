import {
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText,
} from "@mui/material";

import { NavLink } from "react-router-dom";

import navigation from "../../config/navigation";

function SidebarNavigation() {
    return (
        <List
            sx={{
                px: 1,
                py: 1,
                flexGrow: 1,
            }}
        >
            {navigation.map((item) => {
                const Icon = item.icon;

                return (
                    <ListItemButton
                        key={item.path}
                        component={NavLink}
                        to={item.path}
                        end={item.path === "/"}
                        sx={{
                            color: "white",
                            borderRadius: 2,
                            mb: 0.5,
                            textDecoration: "none",

                            "&.active": {
                                bgcolor: "primary.main",
                                color: "white",
                            },

                            "&.active:hover": {
                                bgcolor: "primary.dark",
                            },

                            "&:hover": {
                                bgcolor: "rgba(255,255,255,0.08)",
                            },
                        }}
                    >
                        <ListItemIcon
                            sx={{
                                color: "inherit",
                                minWidth: 40,
                            }}
                        >
                            <Icon />
                        </ListItemIcon>

                        <ListItemText primary={item.label} />
                    </ListItemButton>
                );
            })}
        </List>
    );
}

export default SidebarNavigation;