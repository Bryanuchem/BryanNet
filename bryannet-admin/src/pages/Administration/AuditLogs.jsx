import { useMemo, useState } from "react";
import {
  Box,
  Button,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";

import PageHeader from "../../components/common/PageHeader";

import AuditLogFilters from "../../components/admin/audit-logs/AuditLogFilters";
import AuditLogTable from "../../components/admin/audit-logs/AuditLogTable";
import AuditLogDetailsDialog from "../../components/admin/audit-logs/AuditLogDetailsDialog";

const initialLogs = [
  {
    id: 1,
    timestamp: "30 Jun 2026 10:15",
    user: "Bryan",
    module: "Customers",
    action: "Created",
    target: "John Doe",
    status: "Success",
    ipAddress: "192.168.1.15",
    description: "Created a new customer account.",
  },
  {
    id: 2,
    timestamp: "30 Jun 2026 10:28",
    user: "Mary",
    module: "Plans",
    action: "Updated",
    target: "Premium 20 Mbps",
    status: "Success",
    ipAddress: "192.168.1.18",
    description: "Updated plan pricing.",
  },
  {
    id: 3,
    timestamp: "30 Jun 2026 11:02",
    user: "Bryan",
    module: "Roles",
    action: "Updated",
    target: "Technician",
    status: "Success",
    ipAddress: "192.168.1.15",
    description: "Modified role permissions.",
  },
  {
    id: 4,
    timestamp: "30 Jun 2026 11:40",
    user: "Peter",
    module: "Subscriptions",
    action: "Suspended",
    target: "Subscription #145",
    status: "Warning",
    ipAddress: "192.168.1.22",
    description: "Suspended customer subscription.",
  },
  {
    id: 5,
    timestamp: "30 Jun 2026 12:10",
    user: "Grace",
    module: "Devices",
    action: "Deleted",
    target: "Router-014",
    status: "Failed",
    ipAddress: "192.168.1.30",
    description: "Device deletion failed.",
  },
];

export default function AuditLogs() {
  const [logs] = useState(initialLogs);

  const [search, setSearch] = useState("");
  const [selectedUser, setSelectedUser] = useState("");
  const [selectedModule, setSelectedModule] = useState("");
  const [selectedAction, setSelectedAction] = useState("");

  const [selectedLog, setSelectedLog] = useState(null);

  const filteredLogs = useMemo(() => {
    return logs.filter((log) => {
      const matchesSearch =
        search === "" ||
        log.target.toLowerCase().includes(search.toLowerCase()) ||
        log.user.toLowerCase().includes(search.toLowerCase());

      const matchesUser =
        selectedUser === "" || log.user === selectedUser;

      const matchesModule =
        selectedModule === "" || log.module === selectedModule;

      const matchesAction =
        selectedAction === "" || log.action === selectedAction;

      return (
        matchesSearch &&
        matchesUser &&
        matchesModule &&
        matchesAction
      );
    });
  }, [
    logs,
    search,
    selectedUser,
    selectedModule,
    selectedAction,
  ]);

  return (
    <Box>
      <PageHeader
        title="Audit Logs"
        subtitle="Review administrator activity across the BryanNet ISP Platform."
        actions={
          <Button
            variant="contained"
            startIcon={<RefreshIcon />}
          >
            Refresh
          </Button>
        }
      />

      <Stack spacing={3}>
        <AuditLogFilters
          search={search}
          onSearchChange={setSearch}
        />

        <Stack direction="row" spacing={2}>
          <TextField
            select
            label="User"
            value={selectedUser}
            onChange={(e) =>
              setSelectedUser(e.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Bryan">Bryan</MenuItem>
            <MenuItem value="Mary">Mary</MenuItem>
            <MenuItem value="Peter">Peter</MenuItem>
            <MenuItem value="Grace">Grace</MenuItem>
          </TextField>

          <TextField
            select
            label="Module"
            value={selectedModule}
            onChange={(e) =>
              setSelectedModule(e.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Customers">Customers</MenuItem>
            <MenuItem value="Plans">Plans</MenuItem>
            <MenuItem value="Roles">Roles</MenuItem>
            <MenuItem value="Subscriptions">
              Subscriptions
            </MenuItem>
            <MenuItem value="Devices">Devices</MenuItem>
          </TextField>

          <TextField
            select
            label="Action"
            value={selectedAction}
            onChange={(e) =>
              setSelectedAction(e.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Created">Created</MenuItem>
            <MenuItem value="Updated">Updated</MenuItem>
            <MenuItem value="Suspended">
              Suspended
            </MenuItem>
            <MenuItem value="Deleted">Deleted</MenuItem>
          </TextField>
        </Stack>

        <AuditLogTable
          logs={filteredLogs}
          onView={setSelectedLog}
        />
      </Stack>

      <AuditLogDetailsDialog
        open={Boolean(selectedLog)}
        log={selectedLog}
        onClose={() => setSelectedLog(null)}
      />
    </Box>
  );
}