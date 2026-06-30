import { useMemo, useState } from "react";

import {
  Avatar,
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  InputAdornment,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";

const administrators = [
  {
    id: 1,
    name: "Bryan Uche",
    email: "bryan@bryannet.com",
  },
  {
    id: 2,
    name: "Mary Johnson",
    email: "mary@bryannet.com",
  },
  {
    id: 3,
    name: "John Doe",
    email: "john@bryannet.com",
  },
  {
    id: 4,
    name: "Peter Williams",
    email: "peter@bryannet.com",
  },
  {
    id: 5,
    name: "Grace Adams",
    email: "grace@bryannet.com",
  },
];

export default function AssignUsersDialog({
  open,
  role,
  onClose,
}) {
  const [search, setSearch] = useState("");

  const filteredUsers = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return administrators;
    }

    return administrators.filter(
      (user) =>
        user.name.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query)
    );
  }, [search]);

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
    >
      <DialogTitle>
        Assign Users
      </DialogTitle>

      <DialogContent dividers>
        <Stack spacing={3}>
          <Box>
            <Typography variant="body1">
              Role
            </Typography>

            <Chip
              sx={{ mt: 1 }}
              color="primary"
              label={role?.name ?? "New Role"}
            />
          </Box>

          <TextField
            fullWidth
            placeholder="Search administrators..."
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />

          <Divider />

          <List disablePadding>
            {filteredUsers.map((user) => (
              <ListItem
                key={user.id}
                secondaryAction={
                  <Button variant="outlined">
                    Assign
                  </Button>
                }
              >
                <ListItemAvatar>
                  <Avatar>
                    {user.name.charAt(0)}
                  </Avatar>
                </ListItemAvatar>

                <ListItemText
                  primary={user.name}
                  secondary={user.email}
                />
              </ListItem>
            ))}

            {filteredUsers.length === 0 && (
              <Box
                sx={{
                  py: 6,
                  textAlign: "center",
                }}
              >
                <Typography color="text.secondary">
                  No administrators found.
                </Typography>
              </Box>
            )}
          </List>
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
}