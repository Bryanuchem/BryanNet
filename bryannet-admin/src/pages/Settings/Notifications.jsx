import { useState } from "react";
import {
  Box,
  Button,
  Stack,
} from "@mui/material";

import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAlt";

import PageHeader from "../../components/common/PageHeader";

import EmailNotificationsCard from "../../components/settings/notifications/EmailNotificationsCard";
import TelegramNotificationsCard from "../../components/settings/notifications/TelegramNotificationsCard";
import SystemAlertsCard from "../../components/settings/notifications/SystemAlertsCard";

const initialSettings = {
  enableEmailNotifications: true,
  adminNotificationEmail: "admin@bryannet.com",
  notifyNewCustomerEmail: true,
  notifyNewPaymentEmail: true,
  notifySubscriptionExpiryEmail: true,

  enableTelegramNotifications: true,
  notifyNewCustomerTelegram: true,
  notifyNewPaymentTelegram: true,
  notifyRouterEventsTelegram: true,
  notifySystemErrorsTelegram: true,

  enableSystemAlerts: true,
  maintenanceAlerts: true,
  securityAlerts: true,
  backupAlerts: true,
  highPriorityEvents: true,
};

export default function Notifications() {
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
    console.log("Saving Notification Settings", settings);
  };

  return (
    <Box>
      <PageHeader
        title="Notification Settings"
        subtitle="Configure how the BryanNet ISP Platform sends notifications and system alerts."
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
        <EmailNotificationsCard
          settings={settings}
          onChange={handleChange}
        />

        <TelegramNotificationsCard
          settings={settings}
          onChange={handleChange}
        />

        <SystemAlertsCard
          settings={settings}
          onChange={handleChange}
        />
      </Stack>
    </Box>
  );
}