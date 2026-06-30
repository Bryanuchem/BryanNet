import { useState } from "react";
import {
  Box,
  Button,
  Stack,
} from "@mui/material";

import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAlt";

import PageHeader from "../../components/common/PageHeader";

import BillingDefaultsCard from "../../components/settings/billing/BillingDefaultsCard";
import InvoiceSettingsCard from "../../components/settings/billing/InvoiceSettingsCard";
import TaxConfigurationCard from "../../components/settings/billing/TaxConfigurationCard";

const initialSettings = {
  currency: "NGN",
  billingCycle: "Monthly",
  gracePeriod: "7 Days",
  defaultDueDays: 30,

  invoicePrefix: "INV",
  nextInvoiceNumber: 1001,
  automaticInvoiceGeneration: true,
  includeCompanyLogo: true,

  enableTax: false,
  taxName: "VAT",
  taxRate: 7.5,
  taxIncludedInPrices: false,
};

export default function Billing() {
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
    console.log("Saving Billing Settings", settings);
  };

  return (
    <Box>
      <PageHeader
        title="Billing Settings"
        subtitle="Configure default billing, invoicing and tax settings for the BryanNet ISP Platform."
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
        <BillingDefaultsCard
          settings={settings}
          onChange={handleChange}
        />

        <InvoiceSettingsCard
          settings={settings}
          onChange={handleChange}
        />

        <TaxConfigurationCard
          settings={settings}
          onChange={handleChange}
        />
      </Stack>
    </Box>
  );
}