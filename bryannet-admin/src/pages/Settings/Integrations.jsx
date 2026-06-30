import { useState } from "react";
import {
  Box,
  Button,
  Stack,
} from "@mui/material";

import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAlt";

import PageHeader from "../../components/common/PageHeader";

import TelegramIntegrationCard from "../../components/settings/integrations/TelegramIntegrationCard";
import MikroTikIntegrationCard from "../../components/settings/integrations/MikroTikIntegrationCard";
import PaymentGatewayCard from "../../components/settings/integrations/PaymentGatewayCard";
import SmtpSettingsCard from "../../components/settings/integrations/SmtpSettingsCard";

const initialSettings = {
  telegramEnabled: true,
  telegramBotUsername: "@BryanNetBot",
  telegramWebhookStatus: "Connected",

  mikrotikEnabled: false,
  defaultRouter: "Main Router",
  routerConnectionStatus: "Disconnected",

  paymentGatewayEnabled: false,
  paymentProvider: "Paystack",
  sandboxMode: true,
  paymentConnectionStatus: "Disconnected",

  smtpEnabled: true,
  smtpHost: "smtp.gmail.com",
  smtpPort: 587,
  smtpEncryption: "TLS",
  smtpConnectionStatus: "Connected",
};

export default function Integrations() {
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
    console.log("Saving Integration Settings", settings);
  };

  return (
    <Box>
      <PageHeader
        title="Integration Settings"
        subtitle="Configure external services used by the BryanNet ISP Platform."
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
        <TelegramIntegrationCard
          settings={settings}
          onChange={handleChange}
        />

        <MikroTikIntegrationCard
          settings={settings}
          onChange={handleChange}
        />

        <PaymentGatewayCard
          settings={settings}
          onChange={handleChange}
        />

        <SmtpSettingsCard
          settings={settings}
          onChange={handleChange}
        />
      </Stack>
    </Box>
  );
}