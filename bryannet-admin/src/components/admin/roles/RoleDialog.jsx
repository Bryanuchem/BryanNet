import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import PermissionMatrix from "./PermissionMatrix";

const defaultPermissions = [
  {
    id: "dashboard",
    name: "Dashboard",
    description: "Dashboard module permissions.",
    permissions: [
      {
        id: "dashboard-view",
        name: "View Dashboard",
        description: "Allow viewing dashboard statistics.",
        enabled: true,
      },
    ],
  },
  {
    id: "customers",
    name: "Customers",
    description: "Customer management permissions.",
    permissions: [
      {
        id: "customers-view",
        name: "View Customers",
        description: "View customer information.",
        enabled: true,
      },
      {
        id: "customers-create",
        name: "Create Customers",
        description: "Create new customers.",
        enabled: true,
      },
      {
        id: "customers-edit",
        name: "Edit Customers",
        description: "Modify customer records.",
        enabled: true,
      },
      {
        id: "customers-delete",
        name: "Delete Customers",
        description: "Delete customer records.",
        enabled: false,
      },
    ],
  },
  {
    id: "plans",
    name: "Plans",
    description: "Internet plan permissions.",
    permissions: [
      {
        id: "plans-view",
        name: "View Plans",
        description: "View available plans.",
        enabled: true,
      },
      {
        id: "plans-create",
        name: "Create Plans",
        description: "Create internet plans.",
        enabled: true,
      },
      {
        id: "plans-edit",
        name: "Edit Plans",
        description: "Modify plans.",
        enabled: true,
      },
      {
        id: "plans-delete",
        name: "Delete Plans",
        description: "Delete plans.",
        enabled: false,
      },
    ],
  },
];

export default function RoleDialog({
  open,
  role,
  onClose,
}) {
  const [roleName, setRoleName] = useState("");
  const [description, setDescription] = useState("");
  const [permissions, setPermissions] = useState(defaultPermissions);

  useEffect(() => {
    if (!open) return;

    setRoleName(role?.name ?? "");
    setDescription(role?.description ?? "");
    setPermissions(defaultPermissions);
  }, [open, role]);

  const handlePermissionChange = ({
    groupId,
    permissionId,
    checked,
  }) => {
    setPermissions((previous) =>
      previous.map((group) => {
        if (group.id !== groupId) {
          return group;
        }

        return {
          ...group,
          permissions: group.permissions.map((permission) =>
            permission.id === permissionId
              ? {
                  ...permission,
                  enabled: checked,
                }
              : permission
          ),
        };
      })
    );
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="lg"
    >
      <DialogTitle>
        {role ? "Edit Role" : "Create Role"}
      </DialogTitle>

      <DialogContent dividers>
        <Stack spacing={4}>
          <Box>
            <Typography
              variant="h6"
              gutterBottom
            >
              Role Information
            </Typography>

            <Stack spacing={3}>
              <TextField
                fullWidth
                label="Role Name"
                value={roleName}
                onChange={(event) =>
                  setRoleName(event.target.value)
                }
              />

              <TextField
                fullWidth
                multiline
                minRows={3}
                label="Description"
                value={description}
                onChange={(event) =>
                  setDescription(event.target.value)
                }
              />
            </Stack>
          </Box>

          <Divider />

          <PermissionMatrix
            permissions={permissions}
            onPermissionChange={handlePermissionChange}
          />
        </Stack>
      </DialogContent>

      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={onClose}>
          Cancel
        </Button>

        <Button
          variant="contained"
          onClick={onClose}
        >
          Save Role
        </Button>
      </DialogActions>
    </Dialog>
  );
}  