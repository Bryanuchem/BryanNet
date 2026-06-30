import { useState } from "react";

import {
    Divider,
    IconButton,
    ListItemIcon,
    ListItemText,
    Menu,
    MenuItem,
} from "@mui/material";

import MoreVertIcon from "@mui/icons-material/MoreVert";

function ActionMenu({

    row = null,

    items = [],

}) {

    const [

        anchorEl,

        setAnchorEl,

    ] = useState(null);

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

                {items

                    .filter(
                        (item) => !item.hidden,
                    )

                    .map((item, index) => (

                        <div key={index}>

                            <MenuItem

                                disabled={item.disabled}

                                onClick={(event) => {

                                    event.stopPropagation();

                                    handleClose();

                                    if (
                                        item.disabled ||
                                        !item.onClick
                                    ) {

                                        return;

                                    }

                                    if (
                                        row !== null &&
                                        row !== undefined
                                    ) {

                                        item.onClick(row);

                                    } else {

                                        item.onClick();

                                    }

                                }}

                                sx={{

                                    color:
                                        item.color,

                                }}

                            >

                                {item.icon && (

                                    <ListItemIcon

                                        sx={{

                                            color:
                                                item.color,

                                        }}

                                    >

                                        {item.icon}

                                    </ListItemIcon>

                                )}

                                <ListItemText>

                                    {item.label}

                                </ListItemText>

                            </MenuItem>

                            {item.divider && (

                                <Divider />

                            )}

                        </div>

                    ))}

            </Menu>

        </>

    );

}

export default ActionMenu;