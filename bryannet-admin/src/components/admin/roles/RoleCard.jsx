import MoreVertIcon from "@mui/icons-material/MoreVert";
import EditIcon from "@mui/icons-material/Edit";
import GroupIcon from "@mui/icons-material/Group";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import DeleteIcon from "@mui/icons-material/Delete";
import SecurityIcon from "@mui/icons-material/Security";

import {
  Box,
  Card,
  CardContent,
  Chip,
  Divider,
  IconButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Stack,
  Typography,
} from "@mui/material";
import { useState } from "react";

export default function RoleCard({
  role,
  onEdit,
  onAssignUsers,
  onDelete,
}) {
  const [anchorEl, setAnchorEl] = useState(null);

  const menuOpen = Boolean(anchorEl);

  const handleOpenMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
  };

  const handleEdit = () => {
    handleCloseMenu();
    onEdit?.();
  };

  const handleAssignUsers = () => {
    handleCloseMenu();
    onAssignUsers?.();
  };

  const handleDelete = () => {
    handleCloseMenu();
    onDelete?.();
  };

  return (
    <>
      <Card
        elevation={0}
        sx={{
          height: "100%",
          border: (theme) => `1px solid ${theme.palette.divider}`,
          borderRadius: 3,
          transition: "0.2s ease",
          "&:hover": {
            boxShadow: 3,
          },
        }}
      >
        <CardContent>
          <Stack spacing={2}>
            <Stack
              direction="row"
              justifyContent="space-between"
              alignItems="flex-start"
            >
              <Stack spacing={1}>
                <Stack direction="row" spacing={1} alignItems="center">
                  <SecurityIcon color="primary" />

                  <Typography variant="h6">
                    {role.name}
                  </Typography>
                </Stack>

                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  {role.description}
                </Typography>
              </Stack>

              <IconButton onClick={handleOpenMenu}>
                <MoreVertIcon />
              </IconButton>
            </Stack>

            <Divider />

            <Stack spacing={1.5}>
              <Box
                display="flex"
                justifyContent="space-between"
              >
                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Assigned Users
                </Typography>

                <Chip
                  size="small"
                  label={role.assignedUsers}
                />
              </Box>

              <Box
                display="flex"
                justifyContent="space-between"
              >
                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Permissions
                </Typography>

                <Chip
                  size="small"
                  color="primary"
                  label={role.permissionCount}
                />
              </Box>

              <Box
                display="flex"
                justifyContent="space-between"
              >
                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Last Updated
                </Typography>

                <Typography variant="body2">
                  {role.updatedAt}
                </Typography>
              </Box>
            </Stack>
          </Stack>
        </CardContent>
      </Card>

      <Menu
        anchorEl={anchorEl}
        open={menuOpen}
        onClose={handleCloseMenu}
      >
        <MenuItem onClick={handleEdit}>
          <ListItemIcon>
            <EditIcon fontSize="small" />
          </ListItemIcon>

          <ListItemText>Edit Role</ListItemText>
        </MenuItem>

        <MenuItem onClick={handleAssignUsers}>
          <ListItemIcon>
            <GroupIcon fontSize="small" />
          </ListItemIcon>

          <ListItemText>Assign Users</ListItemText>
        </MenuItem>

        <MenuItem disabled>
          <ListItemIcon>
            <ContentCopyIcon fontSize="small" />
          </ListItemIcon>

          <ListItemText>Duplicate Role</ListItemText>
        </MenuItem>

        <Divider />

        <MenuItem
          onClick={handleDelete}
          sx={{
            color: "error.main",
          }}
        >
          <ListItemIcon>
            <DeleteIcon
              fontSize="small"
              color="error"
            />
          </ListItemIcon>

          <ListItemText>Delete Role</ListItemText>
        </MenuItem>
      </Menu>
    </>
  );
}