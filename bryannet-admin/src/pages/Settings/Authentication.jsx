import { useState } from "react";
import {
  Box,
  Button,
  Stack,
} from "@mui/material";

import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAlt";

import PageHeader from "../../components/common/PageHeader";

import PasswordPolicyCard from "../../components/settings/authentication/PasswordPolicyCard";
import SessionManagementCard from "../../components/settings/authentication/SessionManagementCard";
import LoginSecurityCard from "../../components/settings/authentication/LoginSecurityCard";

const initialSettings = {
  minimumPasswordLength: 8,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialCharacters: true,
  passwordExpiry: "90 Days",

  sessionTimeout: "30 Minutes",
  rememberMe: true,
  maximumConcurrentSessions: 3,
  automaticLogout: true,

  twoFactorAuthentication: false,
  maximumLoginAttempts: 5,
  lockoutDuration: "15 Minutes",
  allowPasswordReset: true,
};

export default function Authentication() {
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
    console.log("Saving Authentication Settings", settings);
  };

  return (
    <Box>
      <PageHeader
        title="Authentication Settings"
        subtitle="Configure authentication, password policies and administrator session management."
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
        <PasswordPolicyCard
          settings={settings}
          onChange={handleChange}
        />

        <SessionManagementCard
          settings={settings}
          onChange={handleChange}
        />

        <LoginSecurityCard
          settings={settings}
          onChange={handleChange}
        />
      </Stack>
    </Box>
  );
}