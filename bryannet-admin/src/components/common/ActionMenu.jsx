import { useState } from "react";

import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";

import MoreVertIcon from "@mui/icons-material/MoreVert";

function ActionMenu({ items = [] }) {
    const [anchorEl, setAnchorEl] = useState(null);

    const open = Boolean(anchorEl);

    const handleOpen = (event) => {
        event.stopPropagation();
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <>
            <IconButton
                size="small"
                onClick={handleOpen}
            >
                <MoreVertIcon fontSize="small" />
            </IconButton>

            <Menu
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
            >
                {items.map((item, index) => (
                    <MenuItem
                        key={index}
                        disabled={item.disabled}
                        onClick={() => {
                            handleClose();

                            if (!item.disabled && item.onClick) {
                                item.onClick();
                            }
                        }}
                    >
                        {item.icon && (
                            <ListItemIcon>
                                {item.icon}
                            </ListItemIcon>
                        )}

                        <ListItemText>
                            {item.label}
                        </ListItemText>
                    </MenuItem>
                ))}
            </Menu>
        </>
    );
}

export default ActionMenu;