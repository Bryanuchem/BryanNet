import { useState } from "react";

import MoreVertIcon from "@mui/icons-material/MoreVert";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import LockResetOutlinedIcon from "@mui/icons-material/LockResetOutlined";
import ToggleOnOutlinedIcon from "@mui/icons-material/ToggleOnOutlined";
import DeleteOutlineOutlinedIcon from "@mui/icons-material/DeleteOutlineOutlined";

import {
    Avatar,
    Box,
    Chip,
    CircularProgress,
    IconButton,
    ListItemIcon,
    ListItemText,
    Menu,
    MenuItem,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TablePagination,
    TableRow,
    Typography,
} from "@mui/material";

const administrators = [
    {
        id: 1,
        name: "Bryan Uche",
        username: "bryan",
        email: "bryan@bryannet.com",
        phone: "+234 801 234 5678",
        role: "Super Administrator",
        status: "Active",
        created: "10 Jan 2026",
        lastLogin: "2 mins ago",
    },
    {
        id: 2,
        name: "Mary Johnson",
        username: "mary",
        email: "mary@bryannet.com",
        phone: "+234 803 456 7890",
        role: "Administrator",
        status: "Active",
        created: "15 Jan 2026",
        lastLogin: "Yesterday",
    },
    {
        id: 3,
        name: "John Doe",
        username: "john",
        email: "john@bryannet.com",
        phone: "+234 805 987 6543",
        role: "Support",
        status: "Inactive",
        created: "20 Jan 2026",
        lastLogin: "Never",
    },
];

export default function AdminUsersTable({
    onViewAdministrator,
    onEditAdministrator,
    onDeleteAdministrator,
    onToggleAdministrator,
    onResetPassword,
    loading = false,
}) {
    const [anchorEl, setAnchorEl] =
        useState(null);

    const [selectedAdmin, setSelectedAdmin] =
        useState(null);

    const [page, setPage] = useState(0);

    const [rowsPerPage, setRowsPerPage] =
        useState(10);

    const open = Boolean(anchorEl);

    const handleOpenMenu = (
        event,
        administrator
    ) => {
        event.stopPropagation();

        setAnchorEl(event.currentTarget);
        setSelectedAdmin(administrator);
    };

    const handleCloseMenu = () => {
        setAnchorEl(null);
    };

    if (loading) {
        return (
            <Paper
                elevation={0}
                sx={{
                    border: 1,
                    borderColor: "divider",
                    borderRadius: 2,
                    p: 8,
                    textAlign: "center",
                }}
            >
                <CircularProgress />

                <Typography
                    sx={{ mt: 2 }}
                    color="text.secondary"
                >
                    Loading administrators...
                </Typography>
            </Paper>
        );
    }

    const paginatedAdministrators =
        administrators.slice(
            page * rowsPerPage,
            page * rowsPerPage +
                rowsPerPage
        );

    return (
        <>
            <Paper
                elevation={0}
                sx={{
                    border: 1,
                    borderColor: "divider",
                    borderRadius: 2,
                    overflow: "hidden",
                }}
            >
                <TableContainer>
                    <Table stickyHeader>
                        <TableHead>
                            <TableRow>
                                <TableCell sx={{ fontWeight: 700 }}>
                                    Name
                                </TableCell>

                                <TableCell sx={{ fontWeight: 700 }}>
                                    Username
                                </TableCell>

                                <TableCell sx={{ fontWeight: 700 }}>
                                    Email
                                </TableCell>

                                <TableCell sx={{ fontWeight: 700 }}>
                                    Role
                                </TableCell>

                                <TableCell sx={{ fontWeight: 700 }}>
                                    Status
                                </TableCell>

                                <TableCell sx={{ fontWeight: 700 }}>
                                    Last Login
                                </TableCell>

                                <TableCell
                                    align="right"
                                    sx={{ fontWeight: 700 }}
                                >
                                    Actions
                                </TableCell>
                            </TableRow>
                        </TableHead>

                        <TableBody>
                            {paginatedAdministrators.map(
                                (admin) => (
                                    <TableRow
                                        key={
                                            admin.id
                                        }
                                        hover
                                        onClick={() =>
                                            onViewAdministrator?.(
                                                admin
                                            )
                                        }
                                        sx={{
                                            cursor:
                                                "pointer",
                                            "& td": {
                                                py: 2,
                                            },
                                        }}
                                    >
                                    <TableCell>
                                        <Box
                                            sx={{
                                                display: "flex",
                                                alignItems: "center",
                                                gap: 2,
                                                minWidth: 260,
                                            }}
                                        >
                                            <Avatar
                                                sx={{
                                                    width: 40,
                                                    height: 40,
                                                    flexShrink: 0,
                                                }}
                                            >
                                                {admin.name.charAt(0)}
                                            </Avatar>

                                            <Typography
                                                fontWeight={600}
                                                noWrap
                                            >
                                                {admin.name}
                                            </Typography>
                                        </Box>
                                    </TableCell>
                                    
                                        <TableCell>
                                            {
                                                admin.username
                                            }
                                        </TableCell>

                                        <TableCell>
                                            {
                                                admin.email
                                            }
                                        </TableCell>

                                        <TableCell>
                                            {admin.role}
                                        </TableCell>

                                        <TableCell>
                                            <Chip
                                                label={
                                                    admin.status
                                                }
                                                size="small"
                                                color={
                                                    admin.status ===
                                                    "Active"
                                                        ? "success"
                                                        : "default"
                                                }
                                                variant="outlined"
                                            />
                                        </TableCell>

                                        <TableCell>
                                            {
                                                admin.lastLogin
                                            }
                                        </TableCell>

                                        <TableCell
                                            align="right"
                                            onClick={(
                                                event
                                            ) =>
                                                event.stopPropagation()
                                            }
                                        >
                                            <IconButton
                                                size="small"
                                                onClick={(
                                                    event
                                                ) =>
                                                    handleOpenMenu(
                                                        event,
                                                        admin
                                                    )
                                                }
                                            >
                                                <MoreVertIcon />
                                            </IconButton>
                                        </TableCell>
                                    </TableRow>
                                )
                            )}

                            {paginatedAdministrators.length ===
                            0 && (
                                <TableRow>
                                    <TableCell
                                        colSpan={7}
                                        align="center"
                                        sx={{
                                            py: 8,
                                        }}
                                    >
                                        <Typography
                                            variant="h6"
                                            gutterBottom
                                        >
                                            No administrators found
                                        </Typography>

                                        <Typography color="text.secondary">
                                            Try adjusting your
                                            search or filters.
                                        </Typography>
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>

                <TablePagination
                    component="div"
                    count={
                        administrators.length
                    }
                    page={page}
                    rowsPerPage={
                        rowsPerPage
                    }
                    rowsPerPageOptions={[
                        10,
                        25,
                        50,
                    ]}
                    onPageChange={(
                        _,
                        newPage
                    ) =>
                        setPage(newPage)
                    }
                    onRowsPerPageChange={(
                        event
                    ) => {
                        setRowsPerPage(
                            parseInt(
                                event.target
                                    .value,
                                10
                            )
                        );

                        setPage(0);
                    }}
                />
            </Paper>

            <Menu
                anchorEl={anchorEl}
                open={open}
                onClose={handleCloseMenu}
            >
                <MenuItem
                    onClick={() => {
                        handleCloseMenu();

                        onViewAdministrator?.(
                            selectedAdmin
                        );
                    }}
                >
                    <ListItemIcon>
                        <VisibilityOutlinedIcon fontSize="small" />
                    </ListItemIcon>

                    <ListItemText>
                        View
                    </ListItemText>
                </MenuItem>

                <MenuItem
                    onClick={() => {
                        handleCloseMenu();

                        onEditAdministrator?.(
                            selectedAdmin
                        );
                    }}
                >
                    <ListItemIcon>
                        <EditOutlinedIcon fontSize="small" />
                    </ListItemIcon>

                    <ListItemText>
                        Edit
                    </ListItemText>
                </MenuItem>

                <MenuItem
                    onClick={() => {
                        handleCloseMenu();

                        onResetPassword?.(
                            selectedAdmin
                        );
                    }}
                >
                    <ListItemIcon>
                        <LockResetOutlinedIcon fontSize="small" />
                    </ListItemIcon>

                    <ListItemText>
                        Reset Password
                    </ListItemText>
                </MenuItem>

                <MenuItem
                    onClick={() => {
                        handleCloseMenu();

                        onToggleAdministrator?.(
                            selectedAdmin
                        );
                    }}
                >
                    <ListItemIcon>
                        <ToggleOnOutlinedIcon fontSize="small" />
                    </ListItemIcon>

                    <ListItemText>
                        {selectedAdmin?.status ===
                        "Active"
                            ? "Deactivate"
                            : "Activate"}
                    </ListItemText>
                </MenuItem>

                <MenuItem
                    onClick={() => {
                        handleCloseMenu();

                        onDeleteAdministrator?.(
                            selectedAdmin
                        );
                    }}
                >
                    <ListItemIcon>
                        <DeleteOutlineOutlinedIcon
                            fontSize="small"
                            color="error"
                        />
                    </ListItemIcon>

                    <ListItemText
                        primaryTypographyProps={{
                            color: "error",
                        }}
                    >
                        Delete
                    </ListItemText>
                </MenuItem>
            </Menu>
        </>
    );
}                            