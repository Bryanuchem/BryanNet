import { useState } from "react";
import {
  Box,
  Button,
  Stack,
} from "@mui/material";

import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAlt";

import PageHeader from "../../components/common/PageHeader";

import MaintenanceModeCard from "../../components/settings/system/MaintenanceModeCard";
import BackupRestoreCard from "../../components/settings/system/BackupRestoreCard";
import SystemHealthCard from "../../components/settings/system/SystemHealthCard";

const initialSettings = {
  maintenanceMode: false,
  maintenanceMessage:
    "The system is currently undergoing scheduled maintenance. Please try again later.",
  allowAdminAccess: true,

  automaticBackups: true,
  backupFrequency: "Daily",
  lastBackup: "Today, 02:00 AM",

  platformVersion: "1.0.0",
  databaseStatus: "Healthy",
  storageUsage: "42%",
  backgroundServices: "Running",
};

export default function System() {
  const [settings, setSettings] = useState(initialSettings);

  const handleChange = (field, value) => {
    setSettings((previous) => ({
      ...previous,
      [field]: value,
    }));
  };

  const handleReset = () => {
    setSettings(initialSettings);
  };

  const handleSave = () => {
    // Placeholder
    console.log("Saving System Settings", settings);
  };

  return (
    <Box>
      <PageHeader
        title="System Settings"
        subtitle="Configure maintenance, backup and overall system health settings."
        actions={
          <Stack direction="row" spacing={2}>
            <Button
              variant="outlined"
              startIcon={<RestartAltRoundedIcon />}
              onClick={handleReset}
            >
              Reset
            </Button>

            <Button
              variant="contained"
              startIcon={<SaveRoundedIcon />}
              onClick={handleSave}
            >
              Save Changes
            </Button>
          </Stack>
        }
      />

      <Stack spacing={3}>
        <MaintenanceModeCard
          settings={settings}
          onChange={handleChange}
        />

        <BackupRestoreCard
          settings={settings}
          onChange={handleChange}
        />

        <SystemHealthCard
          settings={settings}
          onChange={handleChange}
        />
      </Stack>
    </Box>
  );
}