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

import SystemActivityFilters from "../../components/admin/system-activity/SystemActivityFilters.jsx";
import SystemActivityTable from "../../components/admin/system-activity/SystemActivityTable";
import ActivityDetailsDialog from "../../components/admin/system-activity/ActivityDetailsDialog";

const initialActivities = [
  {
    id: 1,
    timestamp: "30 Jun 2026 10:15",
    event: "Customer Registered",
    module: "Customers",
    severity: "Info",
    status: "Success",
    source: "Customer Portal",
    description: "A new customer account was successfully created.",
  },
  {
    id: 2,
    timestamp: "30 Jun 2026 10:24",
    event: "Subscription Activated",
    module: "Subscriptions",
    severity: "Success",
    status: "Success",
    source: "Telegram Bot",
    description: "Customer subscription activated successfully.",
  },
  {
    id: 3,
    timestamp: "30 Jun 2026 10:36",
    event: "Router Synchronization",
    module: "Devices",
    severity: "Warning",
    status: "Failed",
    source: "Router Service",
    description: "Router synchronization failed due to timeout.",
  },
  {
    id: 4,
    timestamp: "30 Jun 2026 10:48",
    event: "Telegram Notification",
    module: "Notifications",
    severity: "Info",
    status: "Success",
    source: "Telegram Bot",
    description: "Notification sent successfully.",
  },
  {
    id: 5,
    timestamp: "30 Jun 2026 11:05",
    event: "Scheduled Backup",
    module: "System",
    severity: "Success",
    status: "Success",
    source: "Scheduler",
    description: "Daily system backup completed.",
  },
];

export default function SystemActivity() {
  const [activities] = useState(initialActivities);

  const [search, setSearch] = useState("");
  const [selectedSeverity, setSelectedSeverity] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [selectedModule, setSelectedModule] = useState("");

  const [selectedActivity, setSelectedActivity] = useState(null);

  const filteredActivities = useMemo(() => {
    return activities.filter((activity) => {
      const matchesSearch =
        search === "" ||
        activity.event.toLowerCase().includes(search.toLowerCase()) ||
        activity.source.toLowerCase().includes(search.toLowerCase());

      const matchesSeverity =
        selectedSeverity === "" ||
        activity.severity === selectedSeverity;

      const matchesStatus =
        selectedStatus === "" ||
        activity.status === selectedStatus;

      const matchesModule =
        selectedModule === "" ||
        activity.module === selectedModule;

      return (
        matchesSearch &&
        matchesSeverity &&
        matchesStatus &&
        matchesModule
      );
    });
  }, [
    activities,
    search,
    selectedSeverity,
    selectedStatus,
    selectedModule,
  ]);

  return (
    <Box>
      <PageHeader
        title="System Activity"
        subtitle="Monitor real-time activity across the BryanNet ISP Platform."
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
        <SystemActivityFilters
          search={search}
          onSearchChange={setSearch}
        />

        <Stack direction="row" spacing={2}>
          <TextField
            select
            label="Severity"
            value={selectedSeverity}
            onChange={(event) =>
              setSelectedSeverity(event.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Info">Info</MenuItem>
            <MenuItem value="Success">Success</MenuItem>
            <MenuItem value="Warning">Warning</MenuItem>
          </TextField>

          <TextField
            select
            label="Status"
            value={selectedStatus}
            onChange={(event) =>
              setSelectedStatus(event.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Success">Success</MenuItem>
            <MenuItem value="Failed">Failed</MenuItem>
          </TextField>

          <TextField
            select
            label="Module"
            value={selectedModule}
            onChange={(event) =>
              setSelectedModule(event.target.value)
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Customers">Customers</MenuItem>
            <MenuItem value="Subscriptions">Subscriptions</MenuItem>
            <MenuItem value="Devices">Devices</MenuItem>
            <MenuItem value="Notifications">Notifications</MenuItem>
            <MenuItem value="System">System</MenuItem>
          </TextField>
        </Stack>

        <SystemActivityTable
          activities={filteredActivities}
          onView={setSelectedActivity}
        />
      </Stack>

      <ActivityDetailsDialog
        open={Boolean(selectedActivity)}
        activity={selectedActivity}
        onClose={() => setSelectedActivity(null)}
      />
    </Box>
  );
}