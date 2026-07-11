import {
    Box,
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Tooltip,
    Typography,
} from "@mui/material";

import {
    useMemo,
    useState,
} from "react";

import {
    NavLink,
    useLocation,
} from "react-router-dom";

import navigation from "../../config/navigation";
import { useLayout } from "../../context/LayoutContext";

import {useCurrentPermissions} from "../../hooks/useCurrentPermissions"

import SidebarExpandableItem from "./SidebarExpandableItem";

export default function SidebarNavigation() {

    const { sidebarCollapsed } = useLayout();

    const {

        hasPermission,

    } = useCurrentPermissions();    

    const location = useLocation();

    const [expandedItems, setExpandedItems] = useState({});

    const groups = useMemo(() => {

        const filteredNavigation =

            navigation

                .map((item) => {

                    // -------------------------------------
                    // Expandable Items
                    // -------------------------------------

                    if (

                        item.children

                    ) {

                        const children =

                            item.children.filter(

                                (child) =>

                                    !child.permission ||

                                    hasPermission(

                                        child.permission,

                                    ),

                            );

                        if (

                            children.length === 0

                        ) {

                            return null;

                        }

                        return {

                            ...item,

                            children,

                        };

                    }

                    // -------------------------------------
                    // Normal Items
                    // -------------------------------------

                    if (

                        item.permission &&

                        !hasPermission(

                            item.permission,

                        )

                    ) {

                        return null;

                    }

                    return item;

                })

                .filter(Boolean);

        return filteredNavigation.reduce(

            (

                acc,

                item,

            ) => {

                if (

                    !acc[item.section]

                ) {

                    acc[item.section] = [];

                }

                acc[item.section].push(

                    item,

                );

                return acc;

            },

            {},

        );

    }, [

        hasPermission,

    ]);

    const toggleItem = (label) => {

        setExpandedItems((prev) => ({

            ...prev,

            [label]: !prev[label],

        }));

    };

    const isExpanded = (item) => {

        if (!item.children) {
            return false;
        }

        const routeMatch = item.children.some((child) =>
            location.pathname.startsWith(child.path)
        );

        return routeMatch || expandedItems[item.label];

    };

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

                            if (item.children) {

                                return (

                                    <SidebarExpandableItem
                                        key={item.label}
                                        icon={Icon}
                                        label={item.label}
                                        open={isExpanded(item)}
                                        onToggle={() =>
                                            toggleItem(item.label)
                                        }
                                        childrenItems={item.children}
                                        sidebarCollapsed={sidebarCollapsed}
                                    />

                                );

                            }

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
                                                fontSize: ".95rem",
                                                fontWeight: 500,
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