import { useMemo, useState } from "react";
import {
  Box,
  Button,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import LogoutIcon from "@mui/icons-material/Logout";

import PageHeader from "../../components/common/PageHeader";

import LoginSessionsFilters from "../../components/admin/login-sessions/LoginSessionsFilters";
import LoginSessionsTable from "../../components/admin/login-sessions/LoginSessionsTable";
import SessionDetailsDialog from "../../components/admin/login-sessions/SessionDetailsDialog";

const initialSessions = [
  {
    id: 1,
    user: "Bryan",
    device: "Desktop",
    browser: "Chrome",
    operatingSystem: "Windows 11",
    ipAddress: "192.168.1.15",
    location: "Owa-Oyibu, Delta",
    loginTime: "30 Jun 2026 08:15",
    lastActivity: "2 mins ago",
    status: "Online",
  },
  {
    id: 2,
    user: "Mary",
    device: "Laptop",
    browser: "Edge",
    operatingSystem: "Windows 11",
    ipAddress: "192.168.1.18",
    location: "Asaba, Delta",
    loginTime: "30 Jun 2026 08:42",
    lastActivity: "10 mins ago",
    status: "Idle",
  },
  {
    id: 3,
    user: "Peter",
    device: "Android",
    browser: "Chrome",
    operatingSystem: "Android 15",
    ipAddress: "192.168.1.25",
    location: "Benin City",
    loginTime: "30 Jun 2026 09:20",
    lastActivity: "25 mins ago",
    status: "Offline",
  },
  {
    id: 4,
    user: "Grace",
    device: "MacBook",
    browser: "Safari",
    operatingSystem: "macOS",
    ipAddress: "192.168.1.32",
    location: "Warri, Delta",
    loginTime: "30 Jun 2026 09:50",
    lastActivity: "1 min ago",
    status: "Online",
  },
];

export default function LoginSessions() {
  const [sessions] = useState(initialSessions);

  const [search, setSearch] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [selectedDevice, setSelectedDevice] = useState("");
  const [selectedBrowser, setSelectedBrowser] = useState("");

  const [selectedSession, setSelectedSession] = useState(null);

  const filteredSessions = useMemo(() => {
    return sessions.filter((session) => {
      const matchesSearch =
        search === "" ||
        session.user.toLowerCase().includes(search.toLowerCase()) ||
        session.ipAddress.includes(search);

      const matchesStatus =
        selectedStatus === "" ||
        session.status === selectedStatus;

      const matchesDevice =
        selectedDevice === "" ||
        session.device === selectedDevice;

      const matchesBrowser =
        selectedBrowser === "" ||
        session.browser === selectedBrowser;

      return (
        matchesSearch &&
        matchesStatus &&
        matchesDevice &&
        matchesBrowser
      );
    });
  }, [
    sessions,
    search,
    selectedStatus,
    selectedDevice,
    selectedBrowser,
  ]);

  return (
    <Box>
      <PageHeader
        title="Login Sessions"
        subtitle="Monitor and manage active administrator sessions."
        actions={
          <Stack direction="row" spacing={2}>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
            >
              Refresh
            </Button>

            <Button
              variant="contained"
              color="error"
              startIcon={<LogoutIcon />}
            >
              Terminate All
            </Button>
          </Stack>
        }
      />

      <Stack spacing={3}>
        <LoginSessionsFilters
          search={search}
          onSearchChange={setSearch}
        />

        <Stack direction="row" spacing={2}>
          <TextField
            select
            label="Status"
            value={selectedStatus}
            onChange={(e) =>
              setSelectedStatus(e.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Online">Online</MenuItem>
            <MenuItem value="Idle">Idle</MenuItem>
            <MenuItem value="Offline">Offline</MenuItem>
          </TextField>

          <TextField
            select
            label="Device"
            value={selectedDevice}
            onChange={(e) =>
              setSelectedDevice(e.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Desktop">Desktop</MenuItem>
            <MenuItem value="Laptop">Laptop</MenuItem>
            <MenuItem value="Android">Android</MenuItem>
            <MenuItem value="MacBook">MacBook</MenuItem>
          </TextField>

          <TextField
            select
            label="Browser"
            value={selectedBrowser}
            onChange={(e) =>
              setSelectedBrowser(e.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Chrome">Chrome</MenuItem>
            <MenuItem value="Edge">Edge</MenuItem>
            <MenuItem value="Safari">Safari</MenuItem>
          </TextField>
        </Stack>

        <LoginSessionsTable
          sessions={filteredSessions}
          onView={setSelectedSession}
        />
      </Stack>

      <SessionDetailsDialog
        open={Boolean(selectedSession)}
        session={selectedSession}
        onClose={() => setSelectedSession(null)}
      />
    </Box>
  );
}