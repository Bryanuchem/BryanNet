import { useMemo, useState } from "react";
import {
  Box,
  Button,
  Grid,
  InputAdornment,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import SearchIcon from "@mui/icons-material/Search";

import PageHeader from "../../components/common/PageHeader";
import RoleCard from "../../components/admin/roles/RoleCard";
import RoleDialog from "../../components/admin/roles/RoleDialog";
import AssignUsersDialog from "../../components/admin/roles/AssignUsersDialog";
import DeleteRoleDialog from "../../components/admin/roles/DeleteRoleDialog";

const initialRoles = [
  {
    id: 1,
    name: "Super Admin",
    description: "Full access to every feature in the platform.",
    assignedUsers: 1,
    permissionCount: 42,
    updatedAt: "Today",
  },
  {
    id: 2,
    name: "Administrator",
    description: "Manages customers, plans, subscriptions and devices.",
    assignedUsers: 3,
    permissionCount: 34,
    updatedAt: "Yesterday",
  },
  {
    id: 3,
    name: "Support",
    description: "Provides customer support and troubleshooting.",
    assignedUsers: 5,
    permissionCount: 20,
    updatedAt: "2 days ago",
  },
  {
    id: 4,
    name: "Technician",
    description: "Handles installations and field operations.",
    assignedUsers: 4,
    permissionCount: 18,
    updatedAt: "3 days ago",
  },
  {
    id: 5,
    name: "Finance",
    description: "Access to billing, payments and reports.",
    assignedUsers: 2,
    permissionCount: 16,
    updatedAt: "1 week ago",
  },
];

export default function RolesPermissions() {
  const [roles] = useState(initialRoles);

  const [search, setSearch] = useState("");
  const [selectedRole, setSelectedRole] = useState(null);

  const [dialogType, setDialogType] = useState(null);

  const filteredRoles = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return roles;
    }

    return roles.filter(
      (role) =>
        role.name.toLowerCase().includes(query) ||
        role.description.toLowerCase().includes(query)
    );
  }, [roles, search]);

  const handleCreateRole = () => {
    setSelectedRole(null);
    setDialogType("role");
  };

  const handleEditRole = (role) => {
    setSelectedRole(role);
    setDialogType("role");
  };

  const handleAssignUsers = (role) => {
    setSelectedRole(role);
    setDialogType("assign-users");
  };

  const handleDeleteRole = (role) => {
    setSelectedRole(role);
    setDialogType("delete");
  };

  const handleCloseDialogs = () => {
    setDialogType(null);
    setSelectedRole(null);
  };

  return (
    <Box>
      <PageHeader
        title="Roles & Permissions"
        subtitle="Create administrator roles and manage permissions across the BryanNet ISP Platform."
        actions={
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateRole}
          >
            Create Role
          </Button>
        }
      />

      <Stack spacing={3}>
        <TextField
          fullWidth
          placeholder="Search roles..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />

        <Grid container spacing={3}>
          {filteredRoles.map((role) => (
            <Grid
              key={role.id}
              size={{
                xs: 12,
                md: 6,
                lg: 4,
              }}
            >
              <RoleCard
                role={role}
                onEdit={() => handleEditRole(role)}
                onAssignUsers={() => handleAssignUsers(role)}
                onDelete={() => handleDeleteRole(role)}
              />
            </Grid>
          ))}
        </Grid>

        {filteredRoles.length === 0 && (
          <Box
            sx={{
              py: 8,
              textAlign: "center",
            }}
          >
            <Typography variant="h6" gutterBottom>
              No roles found
            </Typography>

            <Typography color="text.secondary">
              Try adjusting your search or create a new role.
            </Typography>
          </Box>
        )}
      </Stack>

      <RoleDialog
        open={dialogType === "role"}
        role={selectedRole}
        onClose={handleCloseDialogs}
      />

      <AssignUsersDialog
        open={dialogType === "assign-users"}
        role={selectedRole}
        onClose={handleCloseDialogs}
      />

      <DeleteRoleDialog
        open={dialogType === "delete"}
        role={selectedRole}
        onClose={handleCloseDialogs}
      />
    </Box>
  );
}